#!/usr/bin/python

import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Dockerflix DNS config builder')
parser.add_argument('-r', '--remoteip', help='Dockerflix public server IP address', default='199.233.247.225', required=False)
parser.add_argument('-c', '--config', help='DNS config file', default='./config/dockerflix-dnsmasq.conf', required=False)
args = parser.parse_args()

f = open(args.config)
istr = f.read()
f.close
ostr = istr.replace("{IP}", args.remoteip)

print('#### paste this into your router\'s /etc/dnsmasq.d/dockerflix.conf')
print(ostr)

