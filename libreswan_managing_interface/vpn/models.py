# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Subnet to Subnet Model for storing values to ipsec.conf
class subnettosubnet(models.Model):
    connection_name = models.CharField(max_length = 20,default='',help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    also = models.CharField(max_length=20, default='',blank=True, help_text="The value is a section <b><a>name</a></b>")
    connaddrfamily = models.CharField(max_length=4, default='ipv4',blank=True,help_text="Valid/accepted values are <b><a>ipv4</a></b> OR <b><a>ipv6</a></b>")
    left = models.CharField(max_length = 16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b> OR <b><a>%opportunistic</a></b>")
    leftsubnet = models.CharField(max_length=16, default='',blank=True,help_text="eg. vhost:%no,%priv")
    right = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b>")
    rightsubnet = models.CharField(max_length=19, default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>leave blank</a></b>")
    keyringtries = models.CharField(max_length=16,default='%forever',blank=True,help_text="eg. <b><a>%forever</a></b>")
    auto = models.CharField(max_length=16, default='',blank=True, help_text="eg. <b><a>start</a></b>")
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.connection_name

#Subnet to Subnet Model for storing values to ipsec.conf
class Vpnforremotehost(models.Model):
    connection_name = models.CharField(max_length = 20,default='',blank=True,help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    left = models.CharField(max_length = 16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b> OR <b><a>%opportunistic</a></b>")
    leftcert = models.CharField(max_length=16, default='', blank=True,help_text="eg. <b><a>vpn.example.com</a></b>")
    leftid = models.CharField(max_length=16, default='', blank=True, help_text="eg. <b><a>@vpn.example.com</a></b>")
    leftsendcert = models.CharField(max_length=16, default='sendifasked', blank=True, help_text="Valid - <b><a>yes|always</a></b> OR <b><a>no|never</a></b>")
    leftsubnet = models.CharField(max_length=16, default='',blank=True,help_text="eg. vhost:%no,%priv")
    leftrsasigkey = models.CharField(max_length=16, default='%dnsondemand', blank=True, help_text="eg. <b><a>%cert</a></b>")
    right = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b>")
    rightaddresspool = models.CharField(max_length=16, default='', blank=True,help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    rightca = models.CharField(max_length=16, default='', blank=True,help_text="eg. <b><a>%same</a></b>")
    modecfgdns = models.CharField(max_length=32, default='', blank=True,help_text="eg. <b><a>8.8.8.8,193.100.157.123</a></b>")
    narrowing = models.CharField(max_length=3, default='no', blank=True,help_text="Valid - <b><a>no</a></b> OR <b><a>yes</a></b>")
    dpddelay = models.CharField(max_length=4, default='0', blank=True,help_text="eg. <b><a>10</a></b>")
    dpdtimeout = models.CharField(max_length=4, default='0', blank=True, help_text="eg. <b><a>150</a></b>")
    dpdaction = models.CharField(max_length=4, default='hold', blank=True, help_text="Valid - <b><a>clear</a></b> OR <b><a>restart</a></b> OR <b><a>hold</a></b>")
    auto = models.CharField(max_length=16, default='', blank=True, help_text="eg. <b><a>start</a></b>")
    ikev2 = models.CharField(max_length=16, default='', blank=True, help_text="eg. <b><a>insist</a></b>")
    rekey = models.CharField(max_length=16, default='', blank=True, help_text="eg. <b><a>no</a></b>")
    fragmentation = models.CharField(max_length=16, default='yes', blank=True, help_text="Valid - <b><a>yes</a></b> OR <b><a>no</a></b> OR <b><a>force</a></b>")
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.connection_name