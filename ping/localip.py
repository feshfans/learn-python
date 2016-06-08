#!/usr/bin/env python
# --*-- coding : UTF-8 --*--

import socket
import fcntl
import struct


def get_hostname():
    """
    Get host name
    """
    return socket.getfqdn(socket.gethostname())


def get_host():
    """
    Get host addr, but it is inner ip
    """
    return socket.gethostbyname(get_hostname())


def get_ip_address(ifname):
    """"
    Get the ip addr on specical network
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


if __name__ == '__main__':
    print get_hostname()
    print get_host()
    print get_ip_address("wlan0")
    print get_ip_address("docker0")
