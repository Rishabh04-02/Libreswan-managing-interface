# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Model for checking when are the values stored in ipsec.conf
class dnsconfig(models.Model):
    connection_name = models.CharField(max_length = 20,default='',blank=True,help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    keyexchange = models.CharField(max_length=3, default='ike',help_text="The default and currently the only accepted value is <b><a>ike</a></b>")
    connaddrfamily = models.CharField(max_length=4, default='ipv4',help_text="Valid/accepted values are <b><a>ipv4</a></b> OR <b><a>ipv6</a></b>")
    type = models.CharField(max_length=12, default='tunnel', help_text="Valid - <b><a>tunnel</a></b> OR <b><a>transport</a></b> OR <b><a>passthrough</a></b> OR <b><a>drop</a></b> OR <b><a>reject</a></b>")
    left = models.CharField(max_length = 16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b> OR <b><a>%opportunistic</a></b>")
    leftsubnet = models.CharField(max_length=16, default='',blank=True,help_text="eg. vhost:%no,%priv")
    leftsubnets = models.CharField(max_length=16, default='',blank=True, help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    leftvti = models.CharField(max_length=16, default='',blank=True, help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    leftaddresspool = models.CharField(max_length=16, default='',blank=True, help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    leftprotoport = models.CharField(max_length=16, default='',blank=True, help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    leftnexthop = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>%defaultroute</a></b> OR <b><a>%direct</a></b> OR <b><a>leave blank</a></b>")
    leftsourceip = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>leave blank</a></b>")
    leftupdown = models.CharField(max_length=16,default='',blank=True,help_text="eg. <b><a>ipsec _updown --route yes</a></b> OR <b><a>%disabled</a></b>")
    right = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b>")
    rightsubnet = models.CharField(max_length=19, default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>leave blank</a></b>")
    rightaddresspool = models.CharField(max_length=16, default='',blank=True,help_text="See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    rightnexthop = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>leave blank</a></b>")
    rightsourceip = models.CharField(max_length=16,default='',blank=True,help_text="Valid - <b><a>Input IP</a></b> OR <b><a>leave blank</a></b>")
    keyringtries = models.CharField(max_length=16,default='%forever',help_text="eg. <b><a>%forever</a></b>")
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.connection_name