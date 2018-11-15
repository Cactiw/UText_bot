import time

class MyJob:

    def __init__(self, job, when):
        self.job = job
        self.stop_time = time.time() + when


    def get_time_left(self):
        return self.stop_time - time.time()
