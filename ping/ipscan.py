#!/usr/bin/env python
# -*- coding : utf-8 -*-

import platform
import os
import thread
import time


def get_os():
    """
    Get os Type
    """
    os = platform.system()

    #Python not have switch
    if os == 'Windows':
        return 'n'
    else:
        return 'c'


def ping_ip(ip_str):
    """
    ping ip
    """
    cmd = ["ping", "-{op}".format(op=get_os()), "3", "-b", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    flag = False
    #print ip_str
    #print output
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >= 0:
            flag = True
            break

    if flag:
        print "ip: %s is ok ***" % ip_str


def find_ip(ip_prefix):
    """
    Give the current ip prefix,example:127.0.0 then scan all IP
    """
    for i in range(1, 256):
        ip = "%s.%s" % (ip_prefix, i)
        thread.start_new_thread(ping_ip, (ip, ))
        time.sleep(0.3)

if __name__ == '__main__':
    ip_prefix = "192.168.1"
    find_ip(ip_prefix)
