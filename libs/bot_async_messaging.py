from telegram import Bot
from telegram.utils.request import Request
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import multiprocessing
import threading



class AsyncBot(Bot):

    def __init__(self, token, workers = 4, request_kwargs = None):
        self.message_queue = multiprocessing.Queue()
        self.processing = True
        self.num_workers = workers
        if request_kwargs is None:
            request_kwargs = {}
        con_pool_size = workers + 4
        if 'con_pool_size' not in request_kwargs:
            request_kwargs['con_pool_size'] = con_pool_size
        self._request = Request(**request_kwargs)
        super(AsyncBot, self).__init__(token=token, request=self._request)
        self.start()

    def stop(self):
        self.processing = False
        for i in range(0, self.num_workers):
            self.message_queue.put(None)
        #self.message_queue.close()

    def __del__(self):
        self.processing = False
        for i in range(0, self.num_workers):
            self.message_queue.put(None)
        self.message_queue.close()
        try:
            super(AsyncBot, self).__del__()
        except AttributeError:
            pass


    def send_message(self, *args, **kwargs):
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def sync_send_message(self, *args, **kwargs):
        return super(AsyncBot, self).send_message(*args, **kwargs)

    def actually_send_message(self, *args, **kwargs):
        try:
            super(AsyncBot, self).send_message(*args, **kwargs)
        except Unauthorized:
            print("Unauthorized")
        except TimedOut:
            super(AsyncBot, self).send_message(*args, **kwargs)
        except NetworkError:
            super(AsyncBot, self).send_message(*args, **kwargs)

    def start(self):
        for i in range(0, self.num_workers):
            worker = threading.Thread(target = self.__work, args = ())
            worker.start()


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


class MessageInQueue():

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs