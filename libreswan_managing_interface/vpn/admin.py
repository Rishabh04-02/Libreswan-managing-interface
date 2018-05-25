# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

#For accessing the set IP
from .models import dnsconfig

admin.site.register(dnsconfig)