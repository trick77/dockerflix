Dockerflix
========

Want to watch U.S. Netflix, Hulu, MTV, Vevo, Crackle, ABC, NBC, PBS...?  
Got a Dnsmasq capable router at home, a Raspberry Pi or similar Linux computer?  
Got a virtual private server with a U.S. IP address?  
**Then you've come to the right place!**

Simply said, Dockerflix emulates what companies like Unblock-Us and the like have been doing for years.
Dockerflix uses a man-in-the-middle approach to reroute certain requests through a (your) server in the U.S. and thus tricks geo-fenced on-demand streaming media providers into thinking the request originated from within the U.S. 
This so-called DNS unblocking approach differs vastly from a VPN.

Since my [other  DNS unblocking project](https://github.com/trick77/tunlr-style-dns-unblocking) wasn't easy to install and hard to maintain, I came up with a new variant using [dlundquist's](https://github.com/dlundquist) [sniproxy](https://github.com/dlundquist/sniproxy) instead of HAProxy. 
To make the installation a breeze, I boxed the proxy into a Docker container and wrote a small, Python-based Dnsmasq configuration generator. And voilà: DNS-unblocking as a service (DAAS) ;-)

Thanks to sniproxy's ability to proxy requests based on a wildcard/regex match it's now so much easier to add support for a service. 
Now it's usually enough to just add the main domain name to the proxy and DNS configuration and Dockerflix will be able to hop the geo-fence in most cases.
Since most on-demand streaming media providers are using an off-domain CDN for the video stream, only web site traffic gets sent through Dockerflix. A few exceptions may apply though, notably if the stream itself is geo-fenced.

## Docker installation

This will install the latest Docker version on Ubuntu 12.04 LTS and 14.04 LTS:

`wget -qO- https://get.docker.io/gpg | sudo apt-key add -`  
`echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list`  
`apt-get update`  
`apt-get install lxc-docker`  

## Dockerflix container installation

Clone this Github repository on your VPS server and build the Dockerflix image using the provided shell script:  
 `./build.sh`

## Usage

Once the Dockerflix image has been built, just run it using:  
`docker run -d -p 80:80 -p 443:443 --name dockerflix trick77/dockerflix`

Make sure TCP ports 80 and 443 on your VPS are not in use by some other software like a pre-installed web server. Check with `netstat -tulpn` when in doubt. Make sure both ports are accessible from the outside if using an inbound firewall on the VPS server.

From now on, the Dockerflix container can be resumed or suspended using `docker start dockerflix` and `docker stop dockerflix`

To see if the Dockerflix container is up and running use `docker ps` or `docker ps -a`. Want to get rid of Dockerflix? Just type `docker stop dockerflix; docker rm dockerflix` and it's gone. 

## Post installation

Now that we have set up the proxy, we need to make sure only the **relevant** DNS queries get answered with the VPS' public IP address. Generate a Dnsmasq configuration using:  
`python ./gendns-conf.py --remoteip <PUBLIC_IP_OF_YOUR_VPS_SERVER>`

This configuration has to be used in your home router (if it runs Dnsmasq for DNS resolution) or a Linux-based computer like the Raspberry Pi. Obviously, all DNS requests originating at home have to be resolved/forwarded through Dnsmasq from now on.

## Test

Everything has been set up properly once your VPS' IP address shows up in the web browser when navigating to http://ipinfo.io/

If the web browser shows your home IP there's something wrong with DNS resolution. Tip: Make sure not to fall into the OS or browser DNS cache trap, always restart after changing DNS addresses.

## Demo proxy server

If you don't have your own U.S.-located virtual private server yet feel free to use my Dockerflix demo server. Just omit the `--remoteip <IP>` parameter when calling the gendns-conf.py script and the Dockerflix demo server's IP address will be used.

## Updating

Unless you've made local changes to Dockerflix, this one-liner executed in the cloned repository directory fetches the latest Dockerflix version from Github and creates a new Docker container with the updated version:

`git pull && docker stop dockerflix ; docker rm dockerflix ; ./build.sh && docker run -d -p 80:80 -p 443:443 --name dockerflix trick77/dockerflix`

Don't forget to update your local DNS configuration as well.

## Limitations

Dockerflix only handles requests using plain HTTP or TLS using the SNI extension. Some media players don't support SNI and thus won't work with Dockerflix. 
If you need to proxy plain old SSLv1/v2 for a device, have a look at the non-SNI approach in [tunlr-style-dns-unblocking](https://github.com/trick77/tunlr-style-dns-unblocking).
A few media players (i.e. Chromecast) ignore your DNS settings and always resort to a pre-configured DNS resolver which can't be changed (it still can be done though by rerouting these requests using iptables).

## Supported on-demand Internet streaming services 

| Service                                                         | Web browsers    | iOS | Android |
| --------------------------------------------------------------- | --------------- | --- | ------- |
| [Netflix](https://www.netflix.com/us/)                          | Yes             | Yes |         |
| [Hulu](http://www.hulu.com/)<sup>[1](#hulu)</sup>               | Yes             | Yes |         |
| [HBO Now](http://www.hbonow.com/)                               | Yes             | Yes |         |
| [MTV](http://www.mtv.com/videos/home.jhtml)                     | Yes             |     |         |
| [Vevo](http://www.vevo.com/)                                    | Yes             | Yes |         |
| [Crackle](http://www.crackle.com/)                              | Yes             | Yes |         |
| [ABC](http://abc.go.com/)                                       | Yes             |     |         |
| [NBC](http://www.nbc.com/video/full-episodes)                   | Yes             | Yes |         |
| [PBS](http://video.pbs.org/)                                    | Yes             | Yes |         |
| [LogoTV](http://www.logotv.com/video/showall.jhtml)             | Yes             |     |         |
| [CWTV](http://www.cwtv.com/shows/)                              | Yes             |     |         |
| [Southpark](http://southpark.cc.com/)                           | Yes             |     |         |
| [Smithsonian](http://www.smithsonianchannel.com/full-episodes)  | Yes             | Yes |         |
| [Spike](http://www.spike.com/episodes)                          | Yes             |     |         |
| [Cooking Channel TV](http://www.cookingchanneltv.com/)          | Yes             |     |         |
| [Pandora](http://www.pandora.com/)                              | Yes             | Yes |         |
| [iHeart Radio](http://www.iheart.com/)                          | Yes             |     |         |

<sup><a name="hulu">1</a></sup> Hulu has blacklisted many VPS providers in the U.S. You have to be lucky to find one which still works.

## Contributing

Like Dockerflix? Please star it on Github!

Please contribute by submitting pull requests instead of opening issues to complain that this or that doesn't work. No one gets paid here, so don't expect any real support.

## Advanced configuration

Using a wildcard domain approach may also send traffic to the proxy server even if it's not desired for a certain zone/sub-domain.
For instance, if a content provider uses its own sub-domain as an alias for a CDN, you may want to exclude the zone for that particular sub-domain from
your DNS configuration. This is where `config/dockerflix-dnsmasq-exclude.conf` comes into play. Use this file to forward zones to a different (i.e. Google DNS) 
DNS resolver. Since many CDN optimize their network routes around the world, this usually leads to better stream quality compared to sending the stream across the globe through the proxy server. Obviously, this is only helpful as long as the stream itself is not geo-fenced.
