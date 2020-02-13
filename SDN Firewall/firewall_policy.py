#!/usr/bin/python
# CS 6250 Fall 2018 - Project 6 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def make_firewall_policy(config):
    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    print config  # for demonstration purposes only, so you can see the format of the config
    rules = []
    for entry in config:
        if (entry['macaddr_src'] == '-' and entry['macaddr_dst'] == '-' and entry['ipaddr_src'] == '-' and
                entry['ipaddr_dst'] == '-' and entry['port_src'] == '-' and entry['port_dst'] == '-' and
                entry['protocol'] == '-'):
            continue
        rule = match(ethtype=packet.IPV4)
        if entry['macaddr_src'] != '-':
            rule = rule & match(srcmac=MAC(entry['macaddr_src']))
        if entry['macaddr_dst'] != '-':
            rule = rule & match(dstmac=MAC(entry['macaddr_dst']))
        if entry['ipaddr_src'] != '-':
            rule = rule & match(srcip=IPAddr(entry['ipaddr_src']))
        if entry['ipaddr_dst'] != '-':
            rule = rule & match(dstip=IPAddr(entry['ipaddr_dst']))
        if entry['port_src'] != '-':
            rule = rule & match(srcport=int(entry['port_src']))
        if entry['port_dst'] != '-':
            rule = rule & match(dstport=int(entry['port_dst']))
        if entry['protocol'] != '-':
            tcp_rule = rule & match(protocol=packet.TCP_PROTO)
            udp_rule = rule & match(protocol=packet.UDP_PROTO)
            icmp_rule = rule & match(protocol=packet.ICMP_PROTO)
            if entry['protocol'] == 'T':
                rules.append(tcp_rule)
            elif entry['protocol'] == 'U':
                rules.append(udp_rule)
            elif entry['protocol'] == 'I':
                rules.append(icmp_rule)
            elif entry['protocol'] == 'B':
                rules.append(tcp_rule)
                rules.append(udp_rule)
        else:
            rules.append(rule)
    allowed = ~(union(rules))
    return allowed
