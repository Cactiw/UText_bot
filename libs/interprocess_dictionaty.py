from multiprocessing import Queue


interprocess_queue = Queue()


class InterprocessDictionary:

    def __init__(self, id, type, data):
        self.id = id
        self.type =type
        self.data = data
