# Use iwaseyusuke/mininet:ubuntu-22.04 as the base image
FROM iwaseyusuke/mininet:ubuntu-22.04

LABEL maintainer="Your Name <khalidbsheer4@gmail.com>"
LABEL version="1.0"
LABEL description="Custom Mininet image with additional tools and scripts"

# Set environment variables
ENV USER_NAME=mininetuser
ENV WORK_DIR=/home/${USER_NAME}

# Install required packages
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        curl \
        dnsutils \
        ifupdown \
        iproute2 \
        iptables \
        iputils-ping \
        mininet \
        net-tools \
        openvswitch-switch \
        openvswitch-testcontroller \
        tcpdump \
        vim \
        x11-xserver-utils \
        xterm \
        python3 \
        python3-pip \
        linux-headers-generic && \
    apt-get install -y wireshark && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and configure sudo
RUN useradd -ms /bin/bash ${USER_NAME} && \
    mkdir -p /etc/sudoers.d && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME}

# Set the working directory
USER ${USER_NAME}
WORKDIR ${WORK_DIR}

# Copy your custom scripts and requirements to mininet-scripts directory
COPY custom_topology.py client.py server.py arq.py custom_logging.py packet_loss_rate_calculator.py \
    processing_time_calculator.py packet_sending_rate_calculator.py reinforcement_learning.py \
    reward_calculator.py rtt_calculator.py requirements.txt mininet-scripts/

# Install required Python packages
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r mininet-scripts/requirements.txt