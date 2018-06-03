# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess
import os

import string
import random

from django.contrib import admin
from django.contrib.auth.models import User

"""
    OS imported to check and create dir
    subprocess imported to run commands through subprocess
    
    String imported to generate string
    random imported to generate random string
    
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
    #For each qs in queryset generate the certificates.     Do this
    tempdirname = 'temp_cert/'
    dirname = 'certs/'

    if(os.path.isdir("temp_cert/")!=True): #check if temporary certs dir exists
        cmd = ['mkdir', tempdirname]
        p = subprocess.Popen(
            cmd,
            shell=False
        )
        out, err = p.communicate('\n')

    if (os.path.isdir("certs/") != True):  # check if certs dir exists
        cmd = ['mkdir', dirname]
        q = subprocess.Popen(
            cmd,
            shell=False
        )
        out, err = q.communicate('\n')

    #Generating temporary/intermediate certificates

    #Generating random name for certificate and key
    keyname = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10)) + '.pem'
    print('private key - '+keyname)
    certname = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10)) +'.pem'
    print('certificate name - '+certname)

    expiration_period = '500'
    cmd = ['openssl', 'req', '-newkey', 'rsa:2048', '-nodes', '-keyout', tempdirname+keyname, '-x509', '-days', expiration_period, '-out', tempdirname+certname]
    r = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        shell=False
    )
    #writing the values to PIPE
    r.stdin.write("CA\n")
    r.stdin.write("Ontario\n")
    r.stdin.write("Ottawa\n")
    r.stdin.write("No Hats Corporation\n")
    r.stdin.write("Clients\n")
    r.stdin.write("username.nohats.ca\n")
    r.stdin.write("info@izonetelecom.com\n")
    #getting the output/errors
    out, err = r.communicate('\n')
    r.stdin.close()

    #Generating the .p12 certificate
    cmd = ['openssl', 'pkcs12', '-inkey', tempdirname+keyname, '-in', tempdirname+certname, '-export', '-out', 'temp_cert/username.p12', '-password', 'pass:password']
    s = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        shell=False
    )
    # writing the values to PIPE
    out, err = s.communicate('\n')



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