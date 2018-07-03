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
from .models import SubnetToSubnet, VpnForRemoteHost, GenerateCertificate, UserProfile, CertificateConfiguration, GeneratePrivateKey, GenerateRootCertificate
""" OS imported to check and create dir
    subprocess imported to run commands through subprocess    
    String and random imported to generate random string
    Admin imported to access user submitted info for VPN models
    User imported to add generate certificate options to admin activity
    BaseUserAdmin imported to view/save the contents to database after cert generation
    Messages will be used to display the return status after execution
    Models imported to save values to file and database
"""

# Register your models here.
""" Defining global variables for using in multiple functions
    tempdirname - Temporary certificates holding directory name
    dirname - Final .p12 certificates holding directory name
"""
tempdirname = 'temp_cert/'
dirname = 'certs/'
configdirname = 'config/'
""" write_to_file function -
    writing data to /etc/ipsec.d/connection_name.conf file so that the connection can be saved and loaded from the conf* directory without disturbing other connections
    Opening file in w+ mode, as it will create the file if it doesn't exist otherwise write it
    Checking If attribute exists and has a value, so as to avoid writing attributes with no value to the configuration file
    Writing to file the non empty attributes and their respective value
"""


def write_to_file(modeladmin, request, queryset):
    ConnectionsList = []
    SubnetOrVpn = 0
    for qs in queryset:
        list_values = [
            'also', 'left', 'leftsubnet', 'right', 'rightsubnet',
            'keyringtries', 'auto', 'leftcert', 'leftid', 'leftsendcert',
            'leftrsasigkey', 'rightaddresspool', 'rightca', 'modecfgdns',
            'narrowing', 'dpddelay', 'dpdtimeout', 'dpdaction', 'ikev2',
            'rekey', 'fragmentation', 'mobike'
        ]
        lastval = len(list_values)
        file = "/etc/ipsec.d/" + qs.connection_name + ".conf"
        f = open(file, 'w+')
        f.write("conn\t" + qs.connection_name + "\n")
        for i in range(0, lastval):
            current = list_values[i]
            if (hasattr(qs, current) and getattr(qs, current) != ''):
                f.write("\t\t" + current + "=" + getattr(qs, current) + "\n")
                if current == 'leftcert':
                    SubnetOrVpn = 1
        f.write("\n")
        f.close()

        # Adding connection name to the Connectionslist, So as to give a single success notification/prompt for all connections
        ConnectionsList.append(qs.connection_name)
        if SubnetOrVpn == 1:
            #ipsec auto --add <conname>
            cmd = [
                'ipsec', 'auto', '--add',
                '/etc/ipsec.d/' + qs.connection_name + '.conf'
            ]
        else:
            cmd = [
                'ipsec', 'auto', '--start',
                '/etc/ipsec.d/' + qs.connection_name + '.conf'
            ]
        s = subprocess.Popen(cmd, shell=False)
        out, err = s.communicate('\n')

    # Displaying success message for certificate generation
    allconnections = ', '.join(ConnectionsList)
    messages.success(request, "Connection profiles: " + allconnections +
                     " created/updated successfully.")


""" write_configuration_to_file function -
    It writes the selected user configuration to the default configuration file,
    The values will be loaded from this file while generating the certificates.
    In this way user can create as many configurations as he wants and has the option to choose any configuration as default.
    All the certificates generated will use that configuration.
"""


def write_configuration_to_file(modeladmin, request, queryset):

    # Creating directory for saving certificates
    if (os.path.isdir(configdirname) != True):
        os.makedirs(configdirname, 0o755, True)

        # Success message on folder creation
        messages.success(request,
                         "Directory for saving default configuration file: `" +
                         configdirname + "` created successfully.")

    for qs in queryset:
        qs.expiration_period = str(qs.expiration_period)
        list_values = [
            'expiration_period', 'country_name', 'state_province',
            'locality_name', 'organization_name', 'organization_unit',
            'common_name', 'email_address'
        ]
        lastval = len(list_values)
        file = configdirname + "default_certificate.conf"
        f = open(file, 'w+')
        for i in range(0, lastval):
            current = list_values[i]
            if (hasattr(qs, current) and getattr(qs, current) != ''):
                f.write(getattr(qs, current) + "\n")
        f.close()

    # Displaying success message on saving default_configuration file
    messages.success(request, "Default Certificate configuration file: `" +
                     configdirname + "default_certificate.conf` updated.")


write_configuration_to_file.short_description = "Save Configuration as Default configuration"


""" Check if folder exists/create folder for storing the certificates
    this function is checking if the temporary and the final certificates holding dierctories exists
"""


def check_folders(request):
    if (os.path.isdir(tempdirname) != True):
        os.makedirs(tempdirname, 0o755, True)

        # Success message on folder creation
        messages.success(request,
                         "Directory for saving temporary certificates: " +
                         tempdirname + " created successfully.")

    if (os.path.isdir(dirname) != True):
        os.makedirs(dirname, 0o755, True)

        # Success message on folder creation
        messages.success(request, "Directory for saving .p12 certificates: " +
                         dirname + " created successfully.")


# Generate random name, will be used to assign name to cert and keys
def random_name(leng, ntype):
    gen_name = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits)
        for _ in range(leng)) + ntype
    return gen_name


# Generating temporary rsa key pair/certificates, will be used to create .p12 files
def gen_temp_keys(keyname, certname, username):
    #Fetch default configuration from file to write it to the certs
    DefaultConfigFile = open(configdirname + 'default_certificate.conf', 'r')
    FileContent = DefaultConfigFile.readlines()
    ExpirationPeriod = FileContent[0]
    CountryName = FileContent[1]
    StateProvince = FileContent[2]
    LocalityName = FileContent[3]
    OrgName = FileContent[4]
    OrgUnit = FileContent[5]
    CommonName = FileContent[6]
    EmailAddress = FileContent[7]

    if CommonName.strip('\n') == "user":
        CommonName = username

    cmd = [
        'openssl', 'req', '-newkey', 'rsa:2048', '-nodes', '-keyout',
        tempdirname + keyname, '-x509', '-days', ExpirationPeriod, '-out',
        tempdirname + certname
    ]
    r = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=False)
    # writing the values to PIPE
    r.stdin.write(CountryName.encode())
    r.stdin.write(StateProvince.encode())
    r.stdin.write(LocalityName.encode())
    r.stdin.write(OrgName.encode())
    r.stdin.write(OrgUnit.encode())
    r.stdin.write(CommonName.encode())
    r.stdin.write(EmailAddress.encode())
    # getting the output/errors
    out, err = r.communicate('\n'.encode())
    r.stdin.close()
    os.chmod(tempdirname + keyname, 0o400)


# Generate .p12 certificates, will be used to establish connection
def gen_p12_cert(keyname, certname, password, username):
    cmd = [
        'openssl', 'pkcs12', '-name', username, '-inkey', tempdirname + keyname,
        '-in', tempdirname + certname, '-export', '-out',
        dirname + username + '.p12', '-password', 'pass:' + password
    ]
    s = subprocess.Popen(cmd, shell=False)
    out, err = s.communicate('\n'.encode())
    os.chmod(dirname + username + '.p12', 0o400)


# Delete temporary certificates, as .p12 file is generated and they're no longer required
def dlt_temp_cert(filename):
    cmd = ['rm', '-rf', tempdirname + filename]
    s = subprocess.Popen(cmd, shell=False)
    out, err = s.communicate('\n'.encode())


"""
   Generate user certificate -
   Steps for generating temporary/intermediate certificates:
   Step 1 [Generate random names for certs(public and private)] - Get random name for certificate and key, as every key and cert will be unique this will save from any certificate/key overwriting
   Step 2 [Generate private and public keys] - Generate intermediate certificates, these will be used to generate the final .p12 certs
   Step 3 [Create .p12 file using the above keys] - Generating the .p12 certificates, they are the final certs which will be used to establish connections
   Step 4 [Delete the certificates generated in Step 2] - Delete the temporary certificates, as they were only required to generate .p12 (final) certs
   Step 5 [Save the information to database] - Save/Update the password of certificates in/to database, as it'll be shown to user after his successfull login into the portal
"""


def generate_user_certificate(self, request, queryset):
    check_folders(request)
    UsersList = []
    # For each qs in queryset generate the certificates. Taking input username, it'll be the name of the final generated certificate
    for qs in queryset:
        username = str(qs.username)
        keyname = random_name(10, '.pem')
        certname = random_name(10, '.pem')
        gen_temp_keys(keyname, certname, username)
        password = random_name(20, '')
        gen_p12_cert(keyname, certname, password, username)
        #dlt_temp_cert(keyname)
        dlt_temp_cert(certname)

        GenerateCertificate.objects.filter(username__username=username).update(
            cert_password=password)
        GenerateCertificate.objects.filter(username__username=username).update(
            key_name=keyname)

        # Adding user to the userslist, So as to give a single success notification/prompt for all connections
        UsersList.append(username)

    # Displaying success message for certificate generation
    allusers = ', '.join(UsersList)
    messages.success(
        request,
        "Certificates for users: " + allusers + " generated successfully.")


def save_key_as_private_key(self, request, queryset):

    # Creating directory for saving certificates
    if (os.path.isdir(configdirname + 'private/') != True):
        os.makedirs(configdirname + 'private/', 0o755, True)

        # Success message on folder creation
        messages.success(
            request,
            "Directory for saving private key & root certificate created successfully."
        )

    for qs in queryset:
        KeyPassword = qs.key_password

        cmd = [
            'openssl', 'genrsa', '-aes256', '-out',
            configdirname + 'private/ca.key.pem', '-passout',
            'pass:' + KeyPassword, '4096'
        ]
        r = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=False)
        # getting the output/errors
        out, err = r.communicate('\n'.encode())
        r.stdin.close()
        os.chmod(configdirname + 'private/ca.key.pem', 0o400)

    messages.success(request, "Key successfully saved as private key.")


def generate_root_certificate(self, request, queryset):

    # Creating directory for saving certificates
    if (os.path.isdir(configdirname + 'private/') != True):
        os.makedirs(configdirname + 'private/', 0o755, True)

        # Success message on folder creation
        messages.success(
            request,
            "Directory for saving private key & root certificate created successfully."
        )

    for qs in queryset:
        qs.expiration_period = str(qs.expiration_period)
        SetPassword = qs.password
        list_values = [
            'expiration_period', 'country_name', 'state_province',
            'locality_name', 'organization_name', 'organization_unit',
            'common_name', 'email_address'
        ]
        lastval = len(list_values)
        file = configdirname + "private/root_certificate.conf"
        f = open(file, 'w+')
        for i in range(0, lastval):
            current = list_values[i]
            if (hasattr(qs, current) and getattr(qs, current) != ''):
                f.write(getattr(qs, current) + "\n")
        f.close()

        #Fetch configuration from file to write it to the certs
        DefaultConfigFile = open(
            configdirname + 'private/root_certificate.conf', 'r')
        FileContent = DefaultConfigFile.readlines()
        ExpirationPeriod = FileContent[0]
        CountryName = FileContent[1]
        StateProvince = FileContent[2]
        LocalityName = FileContent[3]
        OrgName = FileContent[4]
        OrgUnit = FileContent[5]
        CommonName = FileContent[6]
        EmailAddress = FileContent[7]

        cmd = [
            'openssl', 'req', '-key', configdirname + 'private/ca.key.pem',
            '-passin', 'pass:' + SetPassword, '-new', '-x509', '-days',
            ExpirationPeriod, '-sha256', '-out',
            configdirname + 'private/ca.root.pem'
        ]
        r = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=False)
        # writing the values to PIPE
        r.stdin.write(CountryName.encode())
        r.stdin.write(StateProvince.encode())
        r.stdin.write(LocalityName.encode())
        r.stdin.write(OrgName.encode())
        r.stdin.write(OrgUnit.encode())
        r.stdin.write(CommonName.encode())
        r.stdin.write(EmailAddress.encode())
        # getting the output/errors
        out, err = r.communicate('\n'.encode())
        r.stdin.close()
        os.chmod(configdirname + 'private/ca.root.pem', 0o400)
        os.remove(configdirname + 'private/root_certificate.conf')

    messages.success(request, "Root certificate successfully generated.")


    

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


# Creating admin task options as this will display(list_display) info in the admin panel
class TaskAdmin(admin.ModelAdmin):
    list_display = ['connection_name', 'creation_date']
    actions = [write_to_file]


class TaskConfigureAdmin(admin.ModelAdmin):
    list_display = [
        'organization_name', 'organization_unit', 'common_name',
        'email_address', 'expiration_period'
    ]
    actions = [write_configuration_to_file]


class TaskConfigureRoot(admin.ModelAdmin):
    list_display = [
        'key_name', 'key_password'
    ]
    actions = [save_key_as_private_key]


class TaskConfigureRootCert(admin.ModelAdmin):
    list_display = [
        'organization_name', 'organization_unit', 'common_name',
        'email_address', 'expiration_period'
    ]
    actions = [generate_root_certificate]


# Define an inline admin descriptor for UserDetail model, this is displaying a model(GenerateCertificates) into default user model
class UserDetailInline(admin.StackedInline):
    model = GenerateCertificate
    can_delete = False
    verbose_name_plural = 'User Details'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


# Define a new User admin, this is the default user admin model
class UserAuthAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'is_active', 'last_login', 'date_joined'
    ]
    actions = [EnableUser, DisableUser]
    inlines = (UserDetailInline, UserProfileInline)


# UserAdmin Class for new model, this will allow the required actions to be done from a different models and not just from the default admin/user model
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email_verified', 'cert_password', 'key_name']

    # Fetching the email_verified field from UserProfile Model for accessibility
    def email_verified(self, obj):
        return obj.username.userprofile.email_verified

    # Using boolean field for convenience
    email_verified.boolean = True

    actions = [generate_user_certificate]


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
admin.site.register(GeneratePrivateKey, TaskConfigureRoot)
admin.site.register(GenerateRootCertificate, TaskConfigureRootCert)
admin.site.register(CertificateConfiguration, TaskConfigureAdmin)
admin.site.register(SubnetToSubnet, TaskAdmin)
admin.site.register(VpnForRemoteHost, TaskAdmin)
