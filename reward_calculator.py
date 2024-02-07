class RewardCalculator:
    def __init__(self):
        pass

    def compute_reward(self, packet_loss_rate, rtt, congestion_window_size, processing_time):
    
        #Reward for low packet loss, low RTT, and high congestion window size
        reward = 1.0 - packet_loss_rate - 0.5 * rtt - 0.2 * congestion_window_size

        return reward