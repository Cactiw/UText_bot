import time

class MyJob:

    def __init__(self, job, when):
        self.job = job
        self.start_time = time.time()
        self.stop_time = time.time() + when


    def get_time_left(self):
        return self.stop_time - time.time()


    def get_time_spent(self):
        return time.time() - self.start_time
