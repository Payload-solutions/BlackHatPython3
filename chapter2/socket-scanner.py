#!/usr/bin/python3

import socket

def connection(target: str, port: int):
    """socket client connection."""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))

    # sending data to host
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

    # receiving data from response 
    response = client.recv(4096)

    print(response.decode())

    client.close()



def main():
    connection("www.google.com", 80)

if __name__ == "__main__":
    main()
