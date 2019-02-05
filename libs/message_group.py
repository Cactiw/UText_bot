from threading import Lock, RLock
from multiprocessing import Queue
from queue import Empty

lock = Lock()
message_groups = {}
message_groups_locks = {}
message_groups_queues = {}
groups_need_to_be_sent = Queue()


class MessageInQueue():

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class MessageGroup:

    def __init__(self):

        with lock:
            group_id_list = list(message_groups)
            print("group_id_list = ", group_id_list)
            print("message_groups =", message_groups)
            if not group_id_list:
                self.id = 0
            else:
                print(group_id_list)
                self.id = group_id_list[-1] + 1
            message_groups.update({self.id: self})
        print("creating group, id =", self.id)
        self.messages = []
        self_lock = RLock()
        message_groups_locks.update({self.id : self_lock})
        self_message_queue = Queue()
        message_groups_queues.update({self.id : self_message_queue})
        self.busy = False

    def add_message(self, message):
        self_lock = message_groups_locks.get(self.id)
        self_queue = message_groups_queues.get(self.id)
        with self_lock:
            self_queue.put(message)
            if self.busy is False:
                print("put in queue")
                groups_need_to_be_sent.put(self)
                self.busy = True
            else:
                print("already awaiting. id =", self.id, self.busy)

    def get_message(self):
        self_queue = message_groups_queues.get(self.id)
        try:
            message = self_queue.get_nowait()
        except Empty:
            message = 1
        return message

    def shedule_removal(self):
        self_queue = message_groups_queues.get(self.id)
        self_queue.append(None)

    def is_empty(self):
        self_queue = message_groups_queues.get(self.id)
        return self_queue.empty()
