# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
import os
import string
import random
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import subnettosubnet, Vpnforremotehost, GenerateCertificate


"""
    OS imported to check and create dir
    subprocess imported to run commands through subprocess    
    String and random imported to generate random string
    Admin imported to access user submitted info for VPN models
    User imported to add generate certificate options to admin activity
    BaseUserAdmin imported to view/save the contents to database after cert generation
    Messages will be used to display the return status after execution
    Models imported to save values to file and database
"""

# Register your models here.


"""
    write_to_file function -
    Used to write config values to /etc/ipsec.d/CONNECTION_NAME.conf
    The values will be loaded from there without disturbing other connections
"""


def write_to_file(modeladmin, request, queryset):
    for qs in queryset:
        list_values = [
            'also', 'connaddrfamily', 'left', 'leftsubnet', 'right',
            'rightsubnet', 'keyringtries', 'auto', 'leftcert', 'leftid',
            'leftsendcert', 'leftrsasigkey', 'rightaddresspool', 'rightca',
            'modecfgdns', 'narrowing', 'dpddelay', 'dpdtimeout', 'dpdaction',
            'ikev2', 'rekey', 'fragmentation'
        ]
        lastval = len(list_values)
        file = "/etc/ipsec.conf"  # writing data to ipsec.conf file
        f = open(file, 'a')  # Opening file in append mode
        f.write(
            "conn\t" + qs.connection_name + "\n")  # Writing the connection name
        for i in range(0, lastval):
            current = list_values[i]  # Getting the current value of attribute
            if (hasattr(qs, current) and getattr(qs, current) !=
                    ''):  # Check If attribute exists and has a value
                f.write("\t\t" + current + "=" + getattr(qs, current) +
                        "\n")  # Write to file the attribute and value
        f.write("\n")
        f.close()  # Closing the file


# Creating admin task options as this will display(list_display) info in the admin panel
class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name', 'creation_date']
    actions = [write_to_file]


# Defining global variables for using in multiple functions
tempdirname = 'temp_cert/'  # Temporary directory name
dirname = 'certs/'  # Certificates directory name


# Check if folder exists/create folder for storing the certificates
def check_folders(request):
    if (os.path.isdir("temp_cert/") !=
            True):  # check if temporary certs dir exists
        cmd = ['mkdir', tempdirname]
        p = subprocess.Popen(cmd, shell=False)
        out, err = p.communicate('\n')

        # Success message on folder creation
        messages.success(request,
                         "Directory for saving temporary certificates: " +
                         tempdirname + " created successfully.")

    if (os.path.isdir("certs/") != True):  # check if certs dir exists
        cmd = ['mkdir', dirname]
        q = subprocess.Popen(cmd, shell=False)
        out, err = q.communicate('\n')

        # Success message on folder creation
        messages.success(request, "Directory for saving .p12 certificates: " +
                         dirname + " created successfully.")


# Generate random name, will be used to assign name to cert and keys
def random_name(ntype):
    gen_name = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits)
        for _ in range(10)) + ntype
    return gen_name


# Generating temporary rsa key pair/certificates, will be used to create .p12 files
def gen_temp_keys(keyname, certname):
    expiration_period = '500'
    cmd = [
        'openssl', 'req', '-newkey', 'rsa:2048', '-nodes', '-keyout',
        tempdirname + keyname, '-x509', '-days', expiration_period, '-out',
        tempdirname + certname
    ]
    r = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=False)
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


# Generate .p12 certificates, will be used to establish connection
def gen_p12_cert(keyname, certname, password, username):
    cmd = [
        'openssl', 'pkcs12', '-inkey', tempdirname + keyname, '-in',
        tempdirname + certname, '-export', '-out', dirname + username + '.p12',
        '-password', 'pass:' + password
    ]
    s = subprocess.Popen(cmd, shell=False)
    out, err = s.communicate('\n')


# Delete temporary certificates, as .p12 file is generated and they're no longer required
def dlt_temp_cert(filename):
    cmd = ['rm', '-rf', tempdirname + filename]
    s = subprocess.Popen(cmd, shell=False)
    out, err = s.communicate('\n')


"""
   Generate user certificate -
   Steps for generating temporary/intermediate certificates:
   Step 1 - Generate random names for certs(public and private)
   Step 2 - Generate private and public keys
   Step 3 - Create .p12 file using the above keys
   Step 4 - Delete the certificates generated in Step 2.
   Step 5 - Save the information to database.
"""


def generate_user_certificate(self, request, queryset):
    check_folders(request)
    UsersList = []
    # For each qs in queryset generate the certificates.
    for qs in queryset:
        username = unicode(
            qs.username
        )  # Taking input username, it'll be the name of the final generated certificate

        # Step 1 - Get random name for certificate and key, as every key and cert will be unique this will save from any certificate/key overwriting
        keyname = random_name('.pem')
        certname = random_name('.pem')

        # Step 2 - Generate intermediate certificates, these will be used to generate the final .p12 certs
        gen_temp_keys(keyname, certname)

        # Step 3 - Generating the .p12 certificates, they are the final certs which will be used to establish connections
        password = random_name('')
        gen_p12_cert(keyname, certname, password, username)

        # Step 4 - Delete the temporary certificates, as they were only required to generate .p12 (final) certs
        dlt_temp_cert(keyname)
        dlt_temp_cert(certname)

        # Step 5 - Save/Update the password of certificates in/to database, as it'll be shown to user after his successfull login into the portal
        GenerateCertificate.objects.filter(username__username=username).update(
            cert_password=password)

        # Adding user to the userslist, So as to give a success notification/prompt
        UsersList.append(username)

    # Displaying success message for certificate generation
    allusers = ', '.join(UsersList)
    messages.success(
        request,
        "Certificate/s for user/s: " + allusers + " generated successfully.")


# Disable user function, this is being used to disable user profile. So, as to prevent user login into this portal
def DisableUser(self, request, queryset):
    UsersList = []
    for qs in queryset:
        user = qs.username
        active = qs.is_active
        User.objects.filter(username=user).update(is_active=False)
        UsersList.append(user)

    # Displaying success message for disabling user
    allusers = ', '.join(UsersList)
    messages.success(request,
                     "The users: " + allusers + " Disabled successfully.")


# Enable user function, this is enabling(reactivating) the disabled user. So, that user can login to the portal and do the required things
def EnableUser(self, request, queryset):
    UsersList = []
    for qs in queryset:
        user = qs.username
        active = qs.is_active
        User.objects.filter(username=user).update(is_active=True)
        UsersList.append(user)

    # Displaying success message for enabling user
    allusers = ', '.join(UsersList)
    messages.success(request,
                     "The users: " + allusers + " Enabled successfully.")


# Define an inline admin descriptor for UserDetail model, this is displaying a model(GenerateCertificates) into default user model
class UserDetailInline(admin.StackedInline):
    model = GenerateCertificate
    can_delete = False
    verbose_name_plural = 'User Details'


# Define a new User admin, this is the default user admin model
class UserAuthAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'is_active', 'last_login', 'date_joined'
    ]
    actions = [generate_user_certificate, EnableUser, DisableUser]
    inlines = (UserDetailInline,)


# UserAdmin Class for new model, this will allow the required actions to be done from a different models and not just from the default admin/user model
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email_verified', 'token', 'cert_password']
    actions = [generate_user_certificate]

    def has_add_permission(self, request):
        return False


# Changing Admin header text, this is done to customize the Admin interface
admin.site.site_header = 'Libreswan Administration'


"""
    Displaying the models to admin
"""


# For users
admin.site.unregister(User)
admin.site.register(GenerateCertificate, UserAdmin)

# For VPN's and Cert generations
admin.site.register(User, UserAuthAdmin)
admin.site.register(subnettosubnet, TaskAdmin)
admin.site.register(Vpnforremotehost, TaskAdmin)
