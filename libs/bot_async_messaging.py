from telegram import Bot
from telegram.utils.request import Request
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from libs.message_group import MessageInQueue, MessageGroup, message_groups, groups_need_to_be_sent, message_groups_locks
import multiprocessing
import threading
import time
import logging
import traceback

MESSAGE_PER_SECOND_LIMIT = 29
MESSAGE_PER_CHAT_LIMIT = 3

UNAUTHORIZED_ERROR_CODE = 2
BADREQUEST_ERROR_CODE = 3


class AsyncBot(Bot):

    def __init__(self, token, workers = 4, request_kwargs = None):
        counter_rlock = threading.RLock()
        self.counter_lock = threading.Condition(counter_rlock)
        self.message_queue = multiprocessing.Queue()
        self.processing = True
        self.num_workers = workers
        self.messages_per_second = 0
        self.messages_per_chat = {}
        self.workers = []
        self.group_workers = []
        if request_kwargs is None:
            request_kwargs = {}
        con_pool_size = workers + 4
        if 'con_pool_size' not in request_kwargs:
            request_kwargs['con_pool_size'] = con_pool_size
        self._request = Request(**request_kwargs)
        super(AsyncBot, self).__init__(token=token, request=self._request)
        self.start()

    def send_message(self, *args, **kwargs):
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def group_send_message(self, group, *args, **kwargs):
        message = MessageInQueue(*args, **kwargs)
        if isinstance(group, int):
            group = message_groups.get(group)
        if group is None:
            raise TypeError
        group.add_message(message)

    def sync_send_message(self, *args, **kwargs):
        return super(AsyncBot, self).send_message(*args, **kwargs)

    def actually_send_message(self, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        lock = self.counter_lock
        lock.acquire()
        try:
            while True:
                lock.acquire()
                messages_per_current_chat = self.messages_per_chat.get(chat_id)
                if messages_per_current_chat is None:
                    messages_per_current_chat = 0
                if self.messages_per_second < MESSAGE_PER_SECOND_LIMIT and messages_per_current_chat < MESSAGE_PER_CHAT_LIMIT:
                    self.messages_per_second += 1
                    self.messages_per_chat.update({chat_id : messages_per_current_chat + 1})
                    lock.release()
                    break
                lock.release()
                lock.wait()
        finally:
            try:
                lock.release()
            except RuntimeError:
                pass
        message = None
        try:
            message = super(AsyncBot, self).send_message(*args, **kwargs)
        except Unauthorized:
            release = threading.Timer(interval=1, function=self.__releasing_resourse, args=[chat_id])
            release.start()
            return UNAUTHORIZED_ERROR_CODE
        except BadRequest:
            logging.error(traceback.format_exc())
            release = threading.Timer(interval=1, function=self.__releasing_resourse, args=[chat_id])
            release.start()
            return BADREQUEST_ERROR_CODE
        except TimedOut:
            time.sleep(0.1)
            message = super(AsyncBot, self).send_message(*args, **kwargs)
        except NetworkError:
            time.sleep(0.1)
            message = super(AsyncBot, self).send_message(*args, **kwargs)
        except Exception:
            logging.error(traceback.format_exc())
        release = threading.Timer(interval=1, function=self.__releasing_resourse, args=[chat_id])
        release.start()
        return message

    def start(self):
        for i in range(0, self.num_workers):
            worker = threading.Thread(target = self.__work, args = ())
            worker.start()
            self.workers.append(worker)
            group_worker = threading.Thread(target = self.__group_work, args = ())
            group_worker.start()
            self.group_workers.append(group_worker)

    def stop(self):
        self.processing = False
        for i in range(0, self.num_workers):
            self.message_queue.put(None)
            groups_need_to_be_sent.put(None)
        for i in self.workers:
            i.join()

    def __del__(self):
        self.processing = False
        for i in range(0, self.num_workers):
            self.message_queue.put(None)
        self.message_queue.close()
        try:
            super(AsyncBot, self).__del__()
        except AttributeError:
            pass


    def __releasing_resourse(self, chat_id):
        with self.counter_lock:
            self.messages_per_second -= 1
            mes_per_chat = self.messages_per_chat.get(chat_id)
            if mes_per_chat is None:
                self.counter_lock.notify_all()
                return
            if mes_per_chat == 1:
                self.messages_per_chat.pop(chat_id)
                self.counter_lock.notify_all()
                return
            mes_per_chat -= 1
            self.messages_per_chat.update({chat_id : mes_per_chat})
            self.counter_lock.notify_all()

    def __work(self):
        message_in_queue = self.message_queue.get()
        while self.processing and message_in_queue:
            args = message_in_queue.args
            kwargs = message_in_queue.kwargs
            self.actually_send_message(*args, **kwargs)
            message_in_queue = self.message_queue.get()
            if message_in_queue is None:
                return 0
        return 0

    def __group_work(self):
        group = groups_need_to_be_sent.get()
        while self.processing and group is not None:
            while True:
                message = group.get_message()
                if message is 1:
                    group.busy = False
                    break
                if message is None:
                    group = None
                    break
                self.actually_send_message(*message.args, **message.kwargs)
            if group is not None:
                group.busy = False
            group = groups_need_to_be_sent.get()

    def check_workers(self):
        workers_alive = 0
        for worker in self.workers:
            if worker.is_alive():
                workers_alive += 1
        return workers_alive
