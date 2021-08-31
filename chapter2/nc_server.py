#!/usr/bin/python3

import threading
import shlex
import argparse
import subprocess
import sys
import textwrap
import socket
from netcat.netcat import NetCat

print("""
        ::'#####:::'##::::'##:'########:::::'###::::'##:::'##:'##::::::::'#######:::::'###::::'########::
        :'##.. ##::. ##::'##:: ##.... ##:::'## ##:::. ##:'##:: ##:::::::'##.... ##:::'## ##::: ##.... ##:
        '##:::: ##::. ##'##::: ##:::: ##::'##:. ##:::. ####::: ##::::::: ##:::: ##::'##:. ##:: ##:::: ##:
         ##:::: ##:::. ###:::: ########::'##:::. ##:::. ##:::: ##::::::: ##:::: ##:'##:::. ##: ##:::: ##:
         ##:::: ##::: ## ##::: ##.....::: #########:::: ##:::: ##::::::: ##:::: ##: #########: ##:::: ##:
        . ##:: ##::: ##:. ##:: ##:::::::: ##.... ##:::: ##:::: ##::::::: ##:::: ##: ##.... ##: ##:::: ##:
        :. #####::: ##:::. ##: ##:::::::: ##:::: ##:::: ##:::: ########:. #######:: ##:::: ##: ########::
        ::.....::::..:::::..::..:::::::::..:::::..:::::..:::::........:::.......:::..:::::..::........:::

        owner: payload
""")


def main():
    parser = argparse.ArgumentParser(description="Black hat python tool",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''Example:
        ============================================================================== 

        netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555 # connect to server

        ==============================================================================
                                    '''))

    parser.add_argument('-c', '--command', action="store_true", help="command shell")
    parser.add_argument('-e', '--execute', help="execute specified command")
    parser.add_argument('-l', '--listen', action="store_true", help="listen")
    parser.add_argument('-p', '--port', type=int, default=55555, help='specified port')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()

if __name__ == "__main__":
    main()