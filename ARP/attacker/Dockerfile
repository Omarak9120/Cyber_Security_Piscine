FROM debian:bullseye

# Install essential tools
RUN apt-get update && apt-get install -y \
    tcpdump \
    iputils-ping \
    net-tools \
    ftp \
    curl \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /workspace

# Default command
CMD ["bash"]
