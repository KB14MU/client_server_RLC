class PacketLossRateCalculator:
    def __init__(self):
        self.sent_packets = set()
        self.received_packets = set()

    def track_sent_packet(self, seq_num):
        self.sent_packets.add(seq_num)

    def track_received_packet(self, seq_num):
        self.received_packets.add(seq_num)

    def compute_packet_loss_rate(self):
        if len(self.sent_packets) > 0:
            lost_packets = self.sent_packets - self.received_packets
            loss_rate = len(lost_packets) / len(self.sent_packets)
            return loss_rate
        else:
            return 0.0