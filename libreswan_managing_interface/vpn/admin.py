# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

#For accessing the set IP
from django.core.exceptions import ValidationError
from django import forms

from .models import subnettosubnet,Vpnforremotehost


def write_to_file(modeladmin,request,queryset):
    for qs in queryset:
        list_values = ['also','connaddrfamily','left','leftsubnet','right','rightsubnet','keyringtries','auto']
        lastval = len(list_values)
        file = "/home/rishabh/try.txt"  # writing data to ipsec.conf file
        f = open(file, 'a')  # Opening file in append mode
        f.write("conn\t" + qs.connection_name + "\n")
        for i in range(0,lastval):
            current = list_values[i]
            getattr(qs, current)
            if(getattr(qs, current)!=''):
                f.write("\t\t" +current+ "=" +getattr(qs, current)+ "\n")
        f.close()


class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name','creation_date']
    actions = [write_to_file]

admin.site.register(subnettosubnet,TaskAdmin)
admin.site.register(Vpnforremotehost,TaskAdmin)