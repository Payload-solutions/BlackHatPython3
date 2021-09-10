#!/uar/bin/python3

from scapy.all import(
    ARP,
    Ether,
    conf,
    get_if_hwaddr,
    send,
    sniff,
    sndrcv,
    srp,
    wrpcap
)
from pprint import pprint
import subprocess
import sys
import os
from multiprocessing import Process
from typing import Any



def  check_network() -> Any:
    output = subprocess.check_output(["ifconfig"], stderr=subprocess.STDOUT, shell=True)
    return output.decode().replace("\n", "")



def get_mac(targetip):

    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)

    for _, r in resp:
        return r[Ether].src
    return None

class Arper:

    def __init__(self, victim, gateway, interface="eth0"):
        pass

    def run(self):
        pass

    def poison(self):
        pass

    def sniff(self, count=200):
        pass

    def restore(self):
        pass





def main():

    # represent a tuple with the information
    # in the network settings
    # check_network()

    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])

    for x in sys.argv:
        print(x)


    myarp = Arper(victim, gateway, interface)
    myarp.run()


if __name__ == "__main__":
    main()
