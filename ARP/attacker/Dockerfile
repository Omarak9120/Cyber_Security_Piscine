FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    for i in 1 2 3; do apt-get install -y --fix-missing \
      dnsutils \
      curl \
      vim \
      python3 \
      python3-pip \
      tcpdump \
      iputils-ping \
      net-tools \
      ftp \
      nano && break || sleep 10; done && \
    rm -rf /var/lib/apt/lists/*

    COPY analyse.sh /root/analyse.sh
    COPY sniff_ftp.py /root/sniff_ftp.py
    
    WORKDIR /root
    RUN chmod +x analyse.sh