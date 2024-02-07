import time

class RTTCalculator:
    def __init__(self):
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def compute_rtt(self):
        if self.start_time is not None:
            rtt = time.time() - self.start_time
            return rtt
        return 0.0

    def stop_timer(self):
        rtt = self.compute_rtt()
        self.start_time = None
        return rtt