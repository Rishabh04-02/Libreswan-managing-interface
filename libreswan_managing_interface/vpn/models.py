# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Model for checking when are the values stored in ipsec.conf
class dnsconfig(models.Model):
    left_text = models.CharField(max_length = 16)
    left_subnet_text = models.CharField(max_length=19,default='')
    left_next_hop = models.CharField(max_length=16,default='')
    left_source_ip = models.CharField(max_length=16,default='')
    right_text = models.CharField(max_length=16,default='')
    right_subnet_text = models.CharField(max_length=19, default='')
    right_next_hop = models.CharField(max_length=16,default='')
    right_source_ip = models.CharField(max_length=16,default='')
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.right_text