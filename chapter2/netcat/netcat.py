

import threading
import shlex
import argparse
import subprocess
import sys
import textwrap
import socket


class NetCat:

    def __init__(self, args, buffer=None) -> None:
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)

    def run(self):

        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):

        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()

                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input("#> ")
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("[*] Exiting...")
            self.socket.close()
            sys.exit()





