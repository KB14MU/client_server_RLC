class CongestionWindowSizeController:
    def __init__(self, initial_size=10):
        self.window_size = initial_size

    def increase_window(self):
        # Increase the congestion window size (e.g., additive increase)
        self.window_size += 1

    def decrease_window(self):
        # Decrease the congestion window size (e.g., multiplicative decrease)
        self.window_size = max(1, self.window_size // 2)

    def get_window_size(self):
        return self.window_size