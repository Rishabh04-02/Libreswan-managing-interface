# Libreswan-managing-interface
Managing Interface for Libreswan VPN software, built using [django](https://github.com/django/django). 

![Libreswan Managing Interface - Screenshot](https://image.ibb.co/hH1zRU/01_Functionalities.png)

## Functionalities of Libreswan Managing Interface
* [Add User](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#add-user)
* [Create VPN for remote host connection profiles](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#create-vpn-for-remote-host-connection-profiles)
* [Create Subnet to Subnet VPN connection profiles](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#create-subnet-to-subnet-vpn-connection-profiles)
* [Generate Private Key (CA private key)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#generate-private-key-ca-private-key)
* [Generate root certificate (Using CA private key)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#generate-root-certificate-using-ca-private-key)
* [Create certificate configurations (for user certificates)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#create-certificate-configurations-for-user-certificates)
* [Generate user certificates](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#generate-user-certificates)
* [Revoke user certificates](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#revoke-user-certificates)
* [Enable user (Allow User to login)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#enable-user-allow-user-to-login)
* [Disable user (Disallow User to login)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#disable-user-disallow-user-to-login)
* [Delete User Data (Keys & Certificates)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#delete-user-data-keys--certificates)
* [Delete all certificates (User, CA & Default Certificate configuration)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#delete-all-certificates-user-ca--default-certificate-configuration)
* [Account activation (email verification)](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#account-activation-email-verification)
* [Download the certificate generated for user](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md#download-the-certificate-generated-for-user)

## Initial project setup/First time installation (Libreswan Managing Interface)
Please Refer:
1. [**Installation Instructions**](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/INSTALLATION_INSTRUCTIONS.md) - A step by step guide on Installation of Libreswan Managing Interface.
2. [**Libreswan Administration guide**](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/ADMINISTRATION_GUIDE.md) - A guide on how to use different functionalities of the Libreswan Managing Interface.
3. [**Google Summer of Code 2018 - Project Proposal**](https://therishabh.in/Libreswan_Managing_Interface_Project_Proposal-Rishabh.pdf) - Web based Certificate and Profile User Interface.

## About [The Libreswan Project](https://libreswan.org/)
Libreswan is a free software implementation of the most widely supported and standardized VPN protocol based on (**"IPsec"**) and the *Internet Key Exchange*(**"IKE"**). These standards are produced and maintained by the Internet Engineering Task Force (**"IETF"**).

Libreswan has been under active development for over 15 years, going back to The FreeS/WAN Project founded in 1997 by John Gilmore and Hugh Daniel. For more information, see the project's [History](https://libreswan.org/wiki/History). Libreswan supports IKE versions 1 and 2. It runs on Linux 2.4 to 4.x, FreeBSD and Apple OSX. On Linux, it can use the built-in IPsec stack (**"XFRM/NETKEY"**) or its own IPsec stack (**"KLIPS"**). It uses the [NSS](https://libreswan.org/wiki/Using_NSS_with_libreswan) crypto library. The list of supported RFC's can be found at [Implemented standards](https://libreswan.org/wiki/Implemented_Standards).

## Download
Libreswan is licensed under the *GNU Public License*(**"GPLv2"**). See the [License](https://www.gnu.org/licenses/gpl-2.0.html). It ships as part of many Linux distributions, including Fedora, RHEL/EPEL and Arch Linux and can be installed on those systems using the native software management tools. The source code is available as tar ball and via our git repository. Older versions, patches and pre-compiled versions are available on our download site.

## Configuration examples
Common configuration examples can be found in our [Wiki](https://libreswan.org/wiki/Configuration_examples). Furthermore, our [test cases](https://github.com/libreswan/libreswan/tree/master/testing/pluto) also document our behaviour. You can find test case results and logfiles on our daily testing site at [testing.libreswan.org](http://testing.libreswan.org/). And of course, the manual page of [ipsec.conf](https://libreswan.org/man/ipsec.conf.5.html) documents the configuration options as well. 

## License
This project(*Libreswan Managing Interface*) is Licensed under : [**GNU General Public License v2.0**](https://github.com/Rishabh04-02/Libreswan-managing-interface/blob/master/LICENSE)
