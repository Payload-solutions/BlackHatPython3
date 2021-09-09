# Chapter 3

<p>
In this chapter we gonna implements sniffers as Wireshar but
built with python
</p>


### raw_socket_sniffer.py
======

<p>
We start defining the HOST IP to our own machine's address and constructing our socket object with the 
parameters necessary for sniffing packets on our network interface. The difference between Windows box
and Linux  is that Windows allow us to sniff all incoming packets regardless of protocol, whereas Linux
forces us to specify that we are sniffing ICMP packets. Note that we are using promiscuous mode, which 
requires administrative privileges on windows or root on Linux. Promiscuous model allows us to sniff 
all packets that the network card sees, even those not destined for our specific host. Then we set a 
socket option, that include the IP headers in our caputred packets. The net step is to determine 
if we are using Windows and, if so, preferom the additional step fof sending an IOCTL to the network 
card driver to enable promiscuous mode. I f you're running windows in a virtual machine, you will likely 
get a notifications that the guest
</p>
