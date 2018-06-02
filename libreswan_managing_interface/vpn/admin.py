# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User

"""
    Admin imported to access user submitted info for VPN models
    User imported to add generate certificate options to admin activity
"""


# Register your models here.

#For accessing the set IP
from django.core.exceptions import ValidationError
from .models import subnettosubnet,Vpnforremotehost


"""
    write_to_file function -
    Used to write config values to ipsec.conf
"""
def write_to_file(modeladmin,request,queryset):
    for qs in queryset:
        list_values = ['also','connaddrfamily','left','leftsubnet','right','rightsubnet','keyringtries','auto','leftcert','leftid','leftsendcert','leftrsasigkey','rightaddresspool','rightca','modecfgdns','narrowing','dpddelay','dpdtimeout','dpdaction','ikev2','rekey','fragmentation']
        lastval = len(list_values)
        file = "/etc/ipsec.conf"  # writing data to ipsec.conf file
        f = open(file, 'a')  # Opening file in append mode
        f.write("conn\t" + qs.connection_name + "\n")   #writing the connection name
        for i in range(0,lastval):
            current = list_values[i]    #Getting the current value of attribute
            if(hasattr(qs,current) and getattr(qs, current)!=''):   #Check If attribute exists and has a value
                f.write("\t\t" +current+ "=" +getattr(qs, current)+ "\n")   #Write to file the attribute and value
        f.write("\n")
        f.close()   #Closing the file


#Creating admin task options
class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name','creation_date']
    actions = [write_to_file]

#Generate user certificate
def generate_user_certificate(self, request, queryset):
    print('Generating certificate')


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'last_login', 'date_joined']   #email address verified field will be added here
    actions = [generate_user_certificate]






"""
    Displaying the models to admin
"""
#For users
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#For VPN's
admin.site.register(subnettosubnet,TaskAdmin)
admin.site.register(Vpnforremotehost,TaskAdmin)