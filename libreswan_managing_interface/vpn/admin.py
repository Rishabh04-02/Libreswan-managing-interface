# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
import os
import string
import random
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# For accessing the set Input,generating the certificates
from django.core.exceptions import ValidationError
from .models import subnettosubnet,Vpnforremotehost,GenerateCertificate

# Register your models here.
"""
    OS imported to check and create dir
    subprocess imported to run commands through subprocess    
    String imported to generate string
    random imported to generate random string    
    Admin imported to access user submitted info for VPN models
    User imported to add generate certificate options to admin activity
    BaseUserAdmin imported to view/save the contents to database after cert generation
"""

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
        f.write("conn\t" + qs.connection_name + "\n")   # Writing the connection name
        for i in range(0,lastval):
            current = list_values[i]    # Getting the current value of attribute
            if(hasattr(qs,current) and getattr(qs, current)!=''):   # Check If attribute exists and has a value
                f.write("\t\t" +current+ "=" +getattr(qs, current)+ "\n")   # Write to file the attribute and value
        f.write("\n")
        f.close()   # Closing the file


# Creating admin task options
class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name','creation_date']
    actions = [write_to_file]

# Defining global variables
tempdirname = 'temp_cert/'  # Temporary directory name
dirname = 'certs/'          # Certificates directory name

# Check if folder exists/create folder
def check_folders():
    if (os.path.isdir("temp_cert/") != True):  # check if temporary certs dir exists
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

# Generate random name for cert and keys
def random_name(ntype):
    gen_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10)) + ntype
    return gen_name

# Generating temporary rsa key pair/certificates
def gen_temp_keys(keyname,certname):
    expiration_period = '500'
    cmd = ['openssl', 'req', '-newkey', 'rsa:2048', '-nodes', '-keyout', tempdirname + keyname, '-x509', '-days',
           expiration_period, '-out', tempdirname + certname]
    r = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        shell=False
    )
    # writing the values to PIPE
    r.stdin.write("CA\n")
    r.stdin.write("Ontario\n")
    r.stdin.write("Ottawa\n")
    r.stdin.write("No Hats Corporation\n")
    r.stdin.write("Clients\n")
    r.stdin.write("username.nohats.ca\n")
    r.stdin.write("info@izonetelecom.com\n")
    # getting the output/errors
    out, err = r.communicate('\n')
    r.stdin.close()

# Generate .p12 certificates
def gen_p12_cert(keyname,certname,password,username):
    cmd = ['openssl', 'pkcs12', '-inkey', tempdirname + keyname, '-in', tempdirname + certname, '-export', '-out', dirname + username + '.p12', '-password', 'pass:'+password]
    s = subprocess.Popen(
        cmd,
        shell=False
    )
    out, err = s.communicate('\n')

# Delete temporary certificates
def dlt_temp_cert(filename):
    cmd = ['rm', '-rf', tempdirname+filename]
    s = subprocess.Popen(
        cmd,
        shell=False
    )
    out, err = s.communicate('\n')


"""
   Generate user certificate -
   Steps for generating temporary/intermediate certificates in steps
   Step 1 - Generate random names for certs(public and private)
   Step 2 - Generate private and public keys
   Step 3 - Create .p12 file using the above keys
   Step 4 - Delete the certificates generated in Step 2.
   Step 5 - Save the information to database.
"""
def generate_user_certificate(self, request, queryset):
    check_folders();
    # For each qs in queryset generate the certificates.
    for qs in queryset:
        username = unicode(qs.username)      # Taking input username, it'll the name of the final generated certificate

        # Get random name for certificate and key - Step 1
        keyname = random_name('.pem');
        certname = random_name('.pem');

        # Generate certificates - Step 2
        gen_temp_keys(keyname,certname);

        # Generating the .p12 certificate - Step 3
        password = random_name('');
        gen_p12_cert(keyname,certname,password,username);

        # Delete the temporary certificates- Step 4
        dlt_temp_cert(keyname);
        dlt_temp_cert(certname);

        # Save/Update the password of certificate to database - Step 5
        GenerateCertificate.objects.filter(username__username=username).update(cert_password=password)



# Define an inline admin descriptor for UserDetail model
class UserDetailInline(admin.StackedInline):
    model = GenerateCertificate
    can_delete = False
    verbose_name_plural = 'User Details'

# Define a new User admin
class UserAuthAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'last_login', 'date_joined']
    actions = [generate_user_certificate]
    inlines = (UserDetailInline,)

# UserAdmin Class for new model
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email_verified','token','cert_password']
    actions = [generate_user_certificate]

    def has_add_permission(self, request):
        return False


# Changing Admin header text
admin.site.site_header = 'Libreswan Administration'

"""
    Displaying the models to admin
"""
# For users
admin.site.unregister(User)
admin.site.register(GenerateCertificate, UserAdmin)

# For VPN's and Cert generations
admin.site.register(User,UserAuthAdmin)
admin.site.register(subnettosubnet,TaskAdmin)
admin.site.register(Vpnforremotehost,TaskAdmin)