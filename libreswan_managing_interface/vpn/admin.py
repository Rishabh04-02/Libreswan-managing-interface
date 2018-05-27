# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

#For accessing the set IP
from .models import dnsconfig


def write_to_file(modeladmin,request,queryset):
    for qs in queryset:
        file = "/etc/ipsec.conf"    #writing data to ipsec.conf file
        f = open(file, 'a')  # Opening file in append mode
        f.write("conn\t"+qs.connection_name + "\n")
        f.write("\t\t"+qs.left_text + "\n")
        f.write("\t\t"+qs.left_subnet_text + "\n")
        f.write("\t\t"+qs.left_next_hop + "\n")
        f.write("\t\t"+qs.left_source_ip + "\n")
        f.write("\t\t"+qs.right_text + "\n")
        f.write("\t\t"+qs.right_subnet_text + "\n")
        f.write("\t\t"+qs.right_next_hop + "\n")
        f.write("\t\t"+qs.right_source_ip + "\n")
        f.write("\t\t"+qs.keyring_tries + "\n")
        f.close()


class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name','right_text']
    actions = [write_to_file]

admin.site.register(dnsconfig,TaskAdmin)