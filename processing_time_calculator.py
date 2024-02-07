import time

class ProcessingTimeCalculator:
    def __init__(self):
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            processing_time = time.time() - self.start_time
            self.start_time = None
            return processing_time
        else:
            return 0.0