import socket
import os
import numpy as np
import struct
import time
from threading import Thread, Event
from arq import ARQProtocol
from reinforcement_learning import DQNReinforcementLearning
from custom_logging import logger
from packet_loss_rate_calculator import PacketLossRateCalculator
from packet_sending_rate_calculator import PacketSendingRateCalculator
from processing_time_calculator import ProcessingTimeCalculator
from rtt_calculator import RTTCalculator
from congestion_window_controller import CongestionWindowSizeController
from reward_calculator import RewardCalculator

SERVER_IP = "0.0.0.0"
SERVER_PORT = 12345
BUFFER_SIZE = 1024
PACKET_SIZE = 1020
MAX_SEQ_NUM = 255
TIMEOUT = 10

packet_loss_calculator = PacketLossRateCalculator()
congestion_window_controller = CongestionWindowSizeController()
processing_time_calculator = ProcessingTimeCalculator()
RTTCalculator = RTTCalculator()
Reward_calculator = RewardCalculator()
packet_sending_rate_calculator = PacketSendingRateCalculator()

def receive_file(file_name, arq_protocol, dqn_model, stop_event):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.settimeout(TIMEOUT)  # Set socket timeout

    seq_num = 0

    logger.info("Server started on {}:{}".format(SERVER_IP, SERVER_PORT))
    logger.info("Server is waiting for data...")

    with open(file_name, 'wb') as file:
        while not stop_event.is_set():
            try:
                logger.info("Waiting to receive data...")
                data, client_address = server_socket.recvfrom(BUFFER_SIZE)
                seq_num, packet_data = struct.unpack('B', data[:1])[0], data[1:]

                logger.info("Received data from {}".format(client_address))
                logger.info("Received packet {}".format(seq_num))

                processed_data = arq_protocol.process_packet(seq_num, packet_data)
                if processed_data is not None:
                    file.write(processed_data)

                packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time = compute_metrics()

                state = np.array([packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time]).reshape(1, -1)
                action = dqn_model.act(state)
                reward = Reward_calculator.compute_reward(
                    packet_loss_rate=packet_loss_rate,
                    rtt=rtt,
                    congestion_window_size=congestion_window_size,
                    processing_time=processing_time
                )
                next_state = np.array([packet_sending_rate_calculator.compute_packet_sending_rate(),
                                       RTTCalculator.compute_rtt(),
                                       packet_loss_calculator.compute_packet_loss_rate(),
                                       congestion_window_controller.get_window_size(),
                                       processing_time_calculator.stop_timer()]).reshape(1, -1)
                dqn_model.train(state, action, reward, next_state, done=False)

                # Fine-tune the model
                dqn_model.fine_tune(new_epsilon_decay=0.99, new_learning_rate=0.0005)

            except socket.timeout:
                logger.error("Timeout: No data received within the specified timeout.")
                handle_timeout(seq_num)
                pass

    server_socket.close()

def compute_metrics():
    packet_sending_rate = packet_sending_rate_calculator.compute_packet_sending_rate()
    rtt = RTTCalculator.compute_rtt()
    packet_loss_rate = packet_loss_calculator.compute_packet_loss_rate()
    congestion_window_size = congestion_window_controller.get_window_size()
    processing_time = processing_time_calculator.stop_timer()

    return packet_sending_rate, rtt, packet_loss_rate, congestion_window_size, processing_time

def handle_timeout(seq_num):
    """Handle a timeout event."""
    RTTCalculator.stop_timer()
    packet_loss_calculator.track_sent_packet(seq_num=seq_num)
    congestion_window_controller.decrease_window()
    processing_time = processing_time_calculator.stop_timer()  # Update this line
    reward = Reward_calculator.compute_reward(
        packet_loss_rate=packet_loss_calculator.compute_packet_loss_rate(),
        rtt=RTTCalculator.compute_rtt(),
        congestion_window_size=congestion_window_controller.get_window_size(),
        processing_time=processing_time
    )
    logger.error("Timeout: No data received within the specified timeout.")

def start_server(file_name, arq_protocol, dqn_model):
    """Start the server thread."""
    stop_event = Event()
    server_thread = Thread(target=receive_file, args=(file_name, arq_protocol, dqn_model, stop_event))
    server_thread.start()
    logger.info(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    return stop_event

if __name__ == "__main__":
    try:
        file_name = "received_file.txt"
        arq_protocol = ARQProtocol()
        dqn_model = DQNReinforcementLearning(state_size=5, action_size=10)
        stop_event = start_server(file_name, arq_protocol, dqn_model)

    except Exception as e:
        logger.error(f"Error: {str(e)}")