#!/bin/bash

# Start SSH
service ssh start

# Start nginx
service nginx start

# Start Tor
tor &

# Keep container running
tail -f /dev/null
