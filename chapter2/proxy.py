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
        print("\n\n[!!] Exiting...")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n[!!] Exiting...")
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

    try:

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                line = "[==>] Received %d bytes from localhost."%len(local_buffer)

                print(line)
                hexdump(local_buffer)

                local_buffer = request_handler(local_buffer)
                remote_socket.send(local_buffer)
                print("[==>] Send to remote.")

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
    except Exception as e:
        print(f"Error by: {str(e)}")

def server_loop(local_host: str, local_port: int, 
        remote_host: str, remote_port: int, receive_first):
    """The server_loop function created a socket and then binds to the local host and listens.
    In the main loop, when a fresh connection request comes in, we hand it odd the proxy_handler in a new
    thread, which does all of the sending and receiving of juicy bits to either side of the data
    stream. The only part left to write is the main function"""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"\n[!!]Error in  {str(e)}")
        print("[!!] Failed to listen on %s:%d"%(local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions")
        print("[!!] Exiting...\n")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[!!] Exiting\n")
        sys.exit(0)

    print("[*] Listening on %s:%d "%(local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d"%(addr[0], addr[1])

        print(line)
        # start a thread to takl to the remote host
        proxy_thread = threading.Thread(
                target=proxy_handler,
                args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():


    if len(sys.argv[1:]) != 5: 
        print("Usage: ./proxy.py [localhost] [localhost]", end="")
        print("[remotehost] [remoteport] receive_first[]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")

        sys.exit(0)


    local_host = sys.argv[1]
    local_port = int(sys.argv[2])


    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()
