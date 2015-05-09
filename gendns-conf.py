#!/usr/bin/python

import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Dockerflix DNS config builder')
parser.add_argument('-r', '--remoteip', help='Dockerflix public server IP address', default='199.233.247.225', required=False)
parser.add_argument('-c', '--config', help='DNS config file', default='./config/dockerflix-dnsmasq.conf', required=False)
parser.add_argument('-t', '--type', help='DNS config type', choices=['dnsmasq', 'bind'], default='dnsmasq', required=False)
parser.add_argument('-d', '--dnsmasqdir', help='BIND config dir', default='/etc/dnsmasq.d', required=False)
parser.add_argument('-b', '--binddir', help='BIND config dir', default='/etc/bind', required=False)
args = parser.parse_args()

f = open(args.config)
istr = f.read()
f.close
ostr = istr.replace('{IP}', args.remoteip)

if args.type == 'dnsmasq':
  print('#### paste this into your router\'s dnsmasq configuration ' + args.dnsmasqdir + '/dockerflix.conf')
  print(ostr)
elif args.type == 'bind':
  print('#### paste this into your router\'s BIND configuration ' + args.binddir + '/dockerflix.zones and include it in your BIND configuration')
  print(re.sub(r"address=/(.*)/(.*)", 'zone \"\g<1>.\" {\n\ttype master;\n\tfile \"' + args.binddir + '/db.dockerflix\";\n};\n', ostr, flags=re.MULTILINE))
  print('\n;#### paste this into your router\'s BIND configuration ' + args.binddir + '/db.dockerflix')
  print('$TTL 86400\n@\tIN SOA ns1 root.localhost. (\n\t2012100401\n\t604800\n\t86400\n\t2419200\n\t86400\n\t)\n\n@\tIN NS ns1\nns1\tIN A ' + args.remoteip + '\n@\tIN A ' + args.remoteip + '\n*\tIN A ' + args.remoteip + '\n')
