import time
class PacketSendingRateCalculator:
    def __init__(self):
        self.start_time = time.time()
        self.packet_count = 0

    def update_packet_count(self):
        self.packet_count += 1

    def compute_packet_sending_rate(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time > 0:
            sending_rate = self.packet_count / elapsed_time
            return sending_rate
        else:
            return 0.0