#!/usr/bin/python3

import socket
import sys


def tcp_connection(target: str, port: int):
    """socket client connection."""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))

    # sending data to host
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

    # receiving data from response 
    response = client.recv(4096)

    print(response.decode())

    client.close()


def udp_connection(host: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b"AAABBBCCC", (host, port))

    # at the moment to receive data, we will recive two params
    data, addr = client.recvfrom(4096)
    print(data.decode())

    client.close()

def main():
    # tcp_connection("www.google.com", 80)
    try:
        udp_connection("127.0.0.1", 9997)
    
    except KeyboardInterrupt:
        print("[*] Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
