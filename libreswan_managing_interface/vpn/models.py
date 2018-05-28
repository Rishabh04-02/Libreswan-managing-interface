# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Model for checking when are the values stored in ipsec.conf
class dnsconfig(models.Model):
    connection_name = models.CharField(max_length = 20,default='',help_text="Choices - %defaultroute OR leave blank, Reference - https://libreswan.org/man/ipsec.conf.5.html")
    left_text = models.CharField(max_length = 16,default='',help_text="Choices - %defaultroute OR leave blank")
    left_subnet_text = models.CharField(max_length=19,default='',help_text="Choices - %defaultroute OR leave blank")
    left_next_hop = models.CharField(max_length=16,default='',help_text="Choices - %defaultroute OR leave blank")
    left_source_ip = models.CharField(max_length=16,default='',help_text="Choices - %defaultroute OR leave blank")
    right_text = models.CharField(max_length=16,default='',help_text="Choices - %defaultroute OR leave blank")
    right_subnet_text = models.CharField(max_length=19, default='',help_text="Choices - %defaultroute OR leave blank")
    right_next_hop = models.CharField(max_length=16,default='',help_text="Choices - %defaultroute OR leave blank")
    right_source_ip = models.CharField(max_length=16,default='',help_text="Choices - %defaultroute OR leave blank")
    keyring_tries = models.CharField(max_length=16,default='%forever',help_text="Choice - %forever")

    def __str__(self):
        return self.connection_name