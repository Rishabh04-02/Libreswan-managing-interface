# Libreswan-managing-interface
Managing Interface for Libreswan VPN software, built using [django](https://github.com/django/django). 

Libreswan is a free software implementation of the most widely supported and standarized VPN protocol based on (**"IPsec"**) and the *Internet Key Exchange*(**"IKE"**). These standards are produced and maintained by the Internet Engineering Task Force (**"IETF"**).

Libreswan has been under active development for over 15 years, going back to The FreeS/WAN Project founded in 1997 by John Gilmore and Hugh Daniel. For more information, see the project's [History](https://libreswan.org/wiki/History). Libreswan supports IKE versions 1 and 2. It runs on Linux 2.4 to 4.x, FreeBSD and Apple OSX. On Linux, it can use the built-in IPsec stack (**"XFRM/NETKEY"**) or its own IPsec stack (**"KLIPS"**). It uses the [NSS](https://libreswan.org/wiki/Using_NSS_with_libreswan) crypto library. The list of supported RFC's can be found at [Implemented standards](https://libreswan.org/wiki/Implemented_Standards).

## Download
Libreswan is licensed under the *GNU Public License*(**"GPLv2"**). See the [License](https://www.gnu.org/licenses/gpl-2.0.html). It ships as part of many Linux distributions, including Fedora, RHEL/EPEL and Arch Linux and can be installed on those systems using the native software management tools. The source code is available as tar ball and via our git repository. Older versions, patches and pre-compiled versions are available on our download site.

## Configuration examples
Common configuration examples can be found in our [Wiki](https://libreswan.org/wiki/Configuration_examples). Furthermore, our [test cases](https://github.com/libreswan/libreswan/tree/master/testing/pluto) also document our behaviour. You can find test case results and logfiles on our daily testing site at [testing.libreswan.org](http://testing.libreswan.org/). And of course, the manual page of [ipsec.conf](https://libreswan.org/man/ipsec.conf.5.html) documents the configuration options as well. 

## Initial project setup/First time installation
Please Refer:
1. [INSTALLATION INSTRUCTIONS](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/INSTALLATION_INSTRUCTIONS.md) 
2. [LIBRESWAN ADMINISTRATION GUIDE](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md)