#!/usr/bin/python3
#coding: utf-8




import sys
import socket
import threading


HEX_FILTER = "".join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):

    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i: i + length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f"{ord(c):02x}" for c in word])
        hexwidth = length*3

        results.append(f"{i:04x} {hexa:<{hexwidth}} {printable}")

    if show:
        for line in results:
            print(line)

    else:
        return results


def receive_from(connection: socket.socket):
    """For receiving bot local and remote data, we pass in the socket object to be used.
    We create an empty byte string, buffer, that will accumulate responses from the socket.
    By default, we set a five-second timeout, which migth be aggressive if you're proxying
    traffic to other countries or over lossy networks, so increase the timeout as neccesary.
    We set up a loop to read response data into the buffer until there's no more data or we
    time out. Finally, we return byte string to the caller, which could be either the local
    or remote machine.

    Sometimes you may want to modify the response or request pacles before the proxy sends them 
    on their way. Let's add a couple of functions (request_handler and response_handler) to do
    just that."""

    buffer = b''
    connection.settimeout(5)
    try:

        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

    except Exception:
        print(\n\n[!] Exiting...)
        sys.exit(0)
    except KeyboardInterrupt:
        print(\n\n[!] Exiting...)
        sys.exit(0)

    return buffer




def main():
    pass


if __name__ == "__main__":
    main()
