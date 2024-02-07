MAX_SEQ_NUM = 255  # Import the MAX_SEQ_NUM from the server.py file

class ARQProtocol:
    def __init__(self):
        self.expected_seq_num = 0
        self.received_packets = {}

    def process_packet(self, seq_num, packet_data):
        if seq_num == self.expected_seq_num:
            self.expected_seq_num = (self.expected_seq_num + 1) % (MAX_SEQ_NUM + 1)
            return packet_data
        else:
            self.received_packets[seq_num] = packet_data
            return None

    def get_ordered_packets(self):
        ordered_packets = []
        for i in range(self.expected_seq_num, self.expected_seq_num + 10):
            if i in self.received_packets:
                ordered_packets.append(self.received_packets[i])
                self.expected_seq_num = (i + 1) % (MAX_SEQ_NUM + 1)
        return ordered_packets