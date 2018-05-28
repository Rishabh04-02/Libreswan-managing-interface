# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

#For accessing the set IP
from django.core.exceptions import ValidationError
from django import forms

from .models import dnsconfig
"""
#for data validation
class dnsconfigForm(forms.model):

    class Meta:
        model=dnsconfig

    def clean_right_text(self):
        data=self.cleaned_data['right_text']
        #Check if right_text == %any
        if data=='%any':
            raise ValidationError(_('Right text can not be %any'))

        return data
"""

def write_to_file(modeladmin,request,queryset):
    for qs in queryset:
        file = "/home/rishabh/Desktop/try.txt"    #writing data to ipsec.conf file
        f = open(file, 'a')  # Opening file in append mode
        f.write("conn\t"+qs.connection_name + "\n")
        f.write("\t\tleft="+qs.left_text + "\n")
        f.write("\t\tleftsubnet="+qs.left_subnet_text + "\n")
        f.write("\t\tleftnexthop="+qs.left_next_hop + "\n")
        f.write("\t\tleftsourceip="+qs.left_source_ip + "\n")
        f.write("\t\tright="+qs.right_text + "\n")
        f.write("\t\trightsubnet="+qs.right_subnet_text + "\n")
        f.write("\t\trightnexthop="+qs.right_next_hop + "\n")
        f.write("\t\trightsourceip="+qs.right_source_ip + "\n")
        f.write("\t\tkeyringtries="+qs.keyring_tries + "\n")
        f.close()


class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name','right_text']
    actions = [write_to_file]

admin.site.register(dnsconfig,TaskAdmin)