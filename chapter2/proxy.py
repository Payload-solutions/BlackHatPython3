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



"""Inside these functions, uou can modify the packet contents, perform fuzzing tasks, test for
authentication issues, or fo whatever else your heart desires. This can be useful, for example, 
if you find plaintext user credentials sent and want to try to elevate privileges on an application
by passing in admin inestead of your own username"""
def request_handler(buffer):
    # perform packet moddifications
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer


def proxy_handler(client_socket: socket.socket, remote_host: str, remote_port: int, receive_first):
    """The function contains the bulk of the logic for our proxy. To start off, we connect to the
    remote host. Then we check to make sure we don't need to first initiate a connection to the remote
    side and request data before going into the main loop. Some server daemons will expect you to do
    this (FTP servers typically send a banner first, for example). We then use the receive_from func-
    tion for both sides of the communication. It accepts a connected socket object and performs a receive.
    We dump the contents of the packet so that we can inspect it for anything interesting. Next, we hand
    the output to the response_handler function and then send the received buffer to the local client.
    The rest of the proxy code is straightforward: we set up our loop to continually read from the local
    client, process the data send it to the remote client, read from the remote client, process the 
    data, and send it to the local client until w no longer detect any data. when there's no dat to send
    on either side of the connection, we close both the local and remote sockets and break out of the loop.

    Let's put together the sever_loop function to set up and manage the connection"""
    remote_socket = socket.socket(socket.AF_INTE, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)


    remote_buffer = response_handler(remote_buffer)

    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhosts."%len(remote_buffer))
        client_socket.send(remote_buffer)


    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>]Received %d bytes from localhost."%len(local_buffer)

            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==> Send to remote.]")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote. "%len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connecions.")
            break



def main():
    pass


if __name__ == "__main__":
    main()
