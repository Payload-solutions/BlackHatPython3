#!/usr/bin/python
"""Developing a simple tcp server"""

import time
import socket
import sys
from pprint import pprint
import threading



# typing zone
type_sock = socket.socket


def make_tcp_server(host: str, port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening in {host}:{port}")

    while True:

        client, addr = server.accept()
        print(f"type of addres {type(addr)} and addr {addr}")
        print(f"accepted connection from {addr[0]} to {addr[1]} ")

        socket_handler = threading.Thread(target=client_handler, args=(client,))
        socket_handler.start()

def client_handler(socket_client: type_sock):
    with socket_client as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

def main():

    try:
        make_tcp_server(host="0.0.0.0", port=9998)
    except KeyboardInterrupt:
        print("[!] Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
