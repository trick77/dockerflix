Dockerflix
========

Want to watch U.S. Netflix, Hulu, MTV, Vevo, Crackle, ABC, NBC, PBS...?  
Got a Dnsmasq capable router at home, a Raspberry Pi or similar Linux computer?  
Got a virtual private server with a U.S. IP address?  
Know how to set up the latest and greatest version of Docker?  
**Then you've come to the right place!**

Since my [other  DNS unblocking project](https://github.com/trick77/tunlr-style-dns-unblocking) wasn't easy to install and hard to maintain, I came up with a new variant using [dlundquist's](https://github.com/dlundquist) [sniproxy](https://github.com/dlundquist/sniproxy) instead of HAproxy. To make the installation a breeze, I boxed the proxy into a Docker container and wrote a small, Python-based Dnsmasq configuration generator.

## Installation

Clone the repository on your VPS server and build the Dockerflix image using the provided shell script:  
 `./build.sh`

## Usage

Once the Dockerflix image has been built, just run it using:  
`docker run -p 80:80 -p 443:443 --name dockerflix trick77/dockerflix`

Make sure TCP ports 80 and 443 on your VPS are not in use by some other software like a pre-installed web server. Check with `netstat -tulpn` when in doubt. Make sure both ports are accessible from the outside if using an inbound firewall on the VPS server.

From now on, you can start or suspend the Dockerflix container using `docker start dockerflix` and `docker stop dockerflix`

To see if the Dockerflix container is up and running use `docker ps` or `docker ps -a`. Want to get rid of Dockerflix? Just type `docker stop dockerflix; docker rm dockerflix` and it's gone. 

## Post installation

Now that we have a proxy, we need to make sure that all **relevant** DNS queries are answered with your VPS' public IP address. Generate a Dnsmasq configuration using:
`python ./gendns-conf.py -r <PUBLIC_IP_OF_YOUR_VPS_SERVER>`

This configuration has to be used in your home router (if it runs Dnsmasq for DNS resolution) or a Linux-based computer like the Raspberry Pi. Obviously, all DNS requests originating at home have to be resolved/forwarded through Dnsmasq from now on.

## Limitations

Dockerflix only handles requests using plain HTTP or TLS using the SNI extension. Some multimedia players don't support SNI and thus won't work with Dockerflix. 

## Contributing

Please contribute using pull requests instead of opening issues to complain that this or that doesn't work. No one gets paid here, so don't expect any support.
