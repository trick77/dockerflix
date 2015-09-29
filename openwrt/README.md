# How to use with OpenWRT

You can use this with your OpenWRT based router to create a wifi to watch foreign netflix etc.

1. Setup your Router, make sure you add your ssh key
1. ssh into your router and add the line `conf-dir=/etc/dnsmasq.d`
1. `mkdir /etc/dnsmasq.d`
1. copy the file created by the python script of the project into a new file in `/etc/dnsmasq.d`
1. restart dnsmasq `/etc/init.d/dnsmasq restart`

Tada! You can watch foreign netflix through the wifi..

#### Bonus: Set this up to use with a Chromecast

Chromecast uses 8.8.8.8 and 8.8.4.4 hardcoded to resolve DNS queries.
You can either add these two lines through the web interface (Network -> Firewall -> Custom Rules) or just run them through ssh
```
iptables -t nat -A PREROUTING -d 8.8.8.8 -j DNAT --to-destination <ip-of-your-dockerflix-host>
iptables -t nat -A PREROUTING -d 8.8.4.4 -j DNAT --to-destination <ip-of-your-dockerflix-host>
```


## Even fancier

If you have multiple instances of this container running around the world, you can put files with the different ips in a folder and replace them through a shellscript
```sh
#!/bin/sh

set -x
set -e

if [ $# -eq 0 ] ; then
	echo "Usage: ./switch-to <filename of file containing dnsmasq rules>"
	exit
fi

OLDIP=$(tail -n1 /etc/dnsmasq.d/foreign-dns | sed -e 's/\//\n/g' | tail -n1)

REGION=$1

cd $(dirname $0)

# replace the rules
cp "$REGION" "/etc/dnsmasq.d/foreign-dns"

# find previous ip..
NEWIP=$(tail -n1 /etc/dnsmasq.d/foreign-dns | sed -e 's/\//\n/g' | tail -n1)

# remove old iptables rules
iptables -t nat --delete PREROUTING -d 8.8.4.4 -j DNAT --to-destination $OLDIP
iptables -t nat --delete PREROUTING -d 8.8.8.8 -j DNAT --to-destination $OLDIP

# create new iptables rules
iptables -t nat -A PREROUTING -d 8.8.8.8 -j DNAT --to-destination $NEWIP
iptables -t nat -A PREROUTING -d 8.8.4.4 -j DNAT --to-destination $NEWIP

# finally restart dnsmasq
/etc/init.d/dnsmasq restart
```
