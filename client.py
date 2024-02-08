import socket
import os
import time
import struct
from threading import Thread
import numpy as np
from reinforcement_learning import DQNReinforcementLearning
from custom_logging import logger
from packet_loss_rate_calculator import PacketLossRateCalculator
from packet_sending_rate_calculator import PacketSendingRateCalculator
from processing_time_calculator import ProcessingTimeCalculator
from rtt_calculator import RTTCalculator
from congestion_window_controller import CongestionWindowSizeController
from reward_calculator import RewardCalculator

SERVER_IP = "10.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024
PACKET_SIZE = 1020

packet_loss_calculator = PacketLossRateCalculator()
congestion_window_controller = CongestionWindowSizeController()
processing_time_calculator = ProcessingTimeCalculator()
RTTCalculator = RTTCalculator()
Reward_calculator = RewardCalculator()
packet_sending_rate_calculator = PacketSendingRateCalculator()

def compute_metrics():
    packet_sending_rate = packet_sending_rate_calculator.compute_packet_sending_rate()
    rtt = RTTCalculator.compute_rtt()
    packet_loss_rate = packet_loss_calculator.compute_packet_loss_rate()
    congestion_window_size = congestion_window_controller.get_window_size()
    processing_time = processing_time_calculator.stop_timer()

    return packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time

def compute_reward():
    packet_loss_rate, rtt, congestion_window_size, processing_time = compute_metrics()
    return Reward_calculator.compute_reward(packet_loss_rate, rtt, congestion_window_size, processing_time)

def send_file(file_name, dqn_model):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    logger.info(f"Client started sending to {SERVER_IP}")

    try:
        with open(file_name, 'rb') as file:
            seq_num = 0
            while True:
                data = file.read(PACKET_SIZE)
                if not data:
                    break

                packet = struct.pack('B', seq_num % 256) + data
                client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))

                packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time = compute_metrics()

                state = np.array([packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time]).reshape(1, -1)
                action = dqn_model.act(state)
                reward = compute_reward()
                next_state = np.array([packet_sending_rate_calculator.compute_packet_sending_rate(), RTTCalculator.compute_rtt(),
                                       packet_loss_calculator.compute_packet_loss_rate(), congestion_window_controller.get_window_size(),
                                       processing_time_calculator.compute_processing_time()]).reshape(1, -1)
                dqn_model.train(state, action, reward, next_state, done=False)

                dqn_model.fine_tune(new_epsilon_decay=0.99, new_learning_rate=0.0005)

                seq_num += 1
                time.sleep(0.1)

    except FileNotFoundError:
        logger.error(f"File not found: {file_name}")
    except Exception as e:
        logger.error(f"Error sending file: {str(e)}")
    finally:
        client_socket.close()

def start_client(file_name, dqn_model):
    client_thread = Thread(target=send_file, args=(file_name, dqn_model))
    client_thread.start()
    logger.info(f"Client started sending to {SERVER_IP}:{SERVER_PORT}")

if __name__ == "__main__":
    try:
        file_name = "sendthis.txt"
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        dqn_model = DQNReinforcementLearning(state_size=5, action_size=10)
        start_client(file_name, dqn_model)

    except Exception as e:
        logger.error(f"Error: {str(e)}")