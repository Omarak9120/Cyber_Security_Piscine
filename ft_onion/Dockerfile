FROM debian:stable-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    nginx tor openssh-server sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy configs and site
COPY index.html /var/www/html/index.html
COPY nginx.conf /etc/nginx/sites-available/default
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY start.sh /start.sh

# Setup SSH
RUN mkdir /var/run/sshd && \
    echo "root:root42" | chpasswd

# Create Tor hidden service directory
RUN mkdir -p /var/lib/tor/hidden_service && \
    chown debian-tor:debian-tor /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

EXPOSE 80 4242

CMD ["/bin/bash", "/start.sh"]
