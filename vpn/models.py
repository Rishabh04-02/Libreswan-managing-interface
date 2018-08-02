# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.validators import MaxValueValidator

# Create your models here.
""" Subnet to Subnet Model for storing values to CONNECTION_NAME.conf
    The connection will be loaded from  /etc/ipsec.d/CONNECTION_NAME.conf
    ipsec auto --start <connname> will be used to start connection in case of subnet to subnet (lan to lan) connections
"""
class SubnetToSubnet(models.Model):
    connection_name = models.CharField(
        max_length=20,
        default='',
        help_text=
        "See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    also = models.CharField(
        max_length=20,
        default='',
        blank=True,
        help_text="The value is a section <b><a>name</a></b>")
    left = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text=
        "Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b> OR <b><a>%opportunistic</a></b>"
    )
    leftsubnet = models.CharField(
        max_length=16, default='', blank=True, help_text="eg. vhost:%no,%priv")
    right = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text=
        "Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b>"
    )
    rightsubnet = models.CharField(
        max_length=19,
        default='',
        blank=True,
        help_text="Valid - <b><a>Input IP</a></b> OR <b><a>leave blank</a></b>")
    keyringtries = models.CharField(
        max_length=16,
        default='%forever',
        blank=True,
        help_text="eg. <b><a>%forever</a></b>")
    auto = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>start</a></b>")
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.connection_name

    class Meta:
        verbose_name = _("02. Subnet to Subnet Conection")
        verbose_name_plural = _("02. Subnet to Subnet Connections")


""" Vpn for remote hosts Model for storing values to CONNECTION_NAME.conf
    The connection will also be loaded from  /etc/ipsec.d/CONNECTION_NAME.conf
    ipsec auto --add <connname> will be used to add connection in this case 
"""
class VpnForRemoteHost(models.Model):
    connection_name = models.CharField(
        max_length=20,
        default='',
        blank=True,
        help_text=
        "See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    left = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text=
        "Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b> OR <b><a>%opportunistic</a></b>"
    )
    leftcert = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>vpn.example.com</a></b>")
    leftid = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>@vpn.example.com</a></b>")
    leftsendcert = models.CharField(
        max_length=16,
        default='sendifasked',
        blank=True,
        help_text="Valid - <b><a>yes|always</a></b> OR <b><a>no|never</a></b>")
    leftsubnet = models.CharField(
        max_length=16, default='', blank=True, help_text="eg. vhost:%no,%priv")
    leftrsasigkey = models.CharField(
        max_length=16,
        default='%dnsondemand',
        blank=True,
        help_text="eg. <b><a>%cert</a></b>")
    right = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text=
        "Valid - <b><a>Input IP</a></b> OR <b><a>%defaultroute</a></b> OR <b><a>%any</a></b>"
    )
    rightaddresspool = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text=
        "See Reference - <a>https://libreswan.org/man/ipsec.conf.5.html</a>")
    rightca = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>%same</a></b>")
    modecfgdns = models.CharField(
        max_length=32,
        default='',
        blank=True,
        help_text="eg. <b><a>8.8.8.8,193.100.157.123</a></b>")
    narrowing = models.CharField(
        max_length=3,
        default='no',
        blank=True,
        help_text="Valid - <b><a>no</a></b> OR <b><a>yes</a></b>")
    dpddelay = models.CharField(
        max_length=4, default='0', blank=True, help_text="eg. <b><a>10</a></b>")
    dpdtimeout = models.CharField(
        max_length=4,
        default='0',
        blank=True,
        help_text="eg. <b><a>150</a></b>")
    dpdaction = models.CharField(
        max_length=4,
        default='hold',
        blank=True,
        help_text=
        "Valid - <b><a>clear</a></b> OR <b><a>restart</a></b> OR <b><a>hold</a></b>"
    )
    mobike = models.CharField(
        max_length=3,
        default='no',
        blank=True,
        help_text="Valid - <b><a>no</a></b> OR <b><a>yes</a></b>")
    auto = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>start</a></b>")
    ikev2 = models.CharField(
        max_length=16,
        default='',
        blank=True,
        help_text="eg. <b><a>insist</a></b>")
    rekey = models.CharField(
        max_length=16, default='', blank=True, help_text="eg. <b><a>no</a></b>")
    fragmentation = models.CharField(
        max_length=16,
        default='yes',
        blank=True,
        help_text=
        "Valid - <b><a>yes</a></b> OR <b><a>no</a></b> OR <b><a>force</a></b>")
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.connection_name

    class Meta:
        verbose_name = _("01. VPN for Remote Host")
        verbose_name_plural = _("01. VPN for Remote Hosts")


""" Model for User Profile creation, will be used to store some values regarding certificate generation, email verifications etc.
"""
class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(
        default=False,
        editable=False,
        help_text="Valid - <b><a>True</a></b> OR <b><a>False</a></b>")
    certificate_revoked = models.BooleanField(
        default=False,
        editable=False)

    def __unicode__(self):
        return unicode(self.username)


""" Model for certificate generation, will be used to update token/cert_password values
"""
class GenerateCertificate(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    cert_name = models.CharField(
        max_length=15,
        default='',
        blank=True,
        editable=False,
        help_text="<b><a>System Generated - Do not alter</a></b>")
    cert_password = models.CharField(
        max_length=20,
        default='',
        blank=True,
        editable=False,
        help_text="<b><a>System Generated - Do not alter</a></b>")
    key_name = models.CharField(
        max_length=15,
        default='',
        blank=True,
        editable=False,
        help_text="<b><a>System Generated - Do not alter</a></b>")

    def __unicode__(self):
        return unicode(self.username)

    class Meta:
        verbose_name = _("4. Generate OR Revoke User Certificate")
        verbose_name_plural = _("4. Generate OR Revoke User Certificates")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(username=instance)
        GenerateCertificate.objects.create(username=instance)
        instance.userprofile.save() 
        instance.generatecertificate.save()


""" Model for writing certificate configuration to a file, the configuration will be loaded from a file while generatig certificates.
"""
class CertificateConfiguration(models.Model):

    country_name = models.CharField(
        max_length=2,
        default='CA',
        blank=False,
        help_text="Enter 2 Letter country code")
    state_province = models.CharField(
        max_length=20,
        default='Ontario',
        blank=False,
        help_text="Enter State or Province Name (full name)")
    locality_name = models.CharField(
        max_length=20,
        default='Ottawa',
        blank=False,
        help_text="Enter Locality name (eg.city)")
    organization_name = models.CharField(
        max_length=30,
        default='No Hats Corporation',
        blank=False,
        help_text="Enter Organization name (eg. company ltd)")
    organization_unit = models.CharField(
        max_length=20,
        default='Clients',
        blank=False,
        help_text="Enter Organization unit name (eg. section name)")
    common_name = models.CharField(
        max_length=20,
        default='user',
        blank=False,
        help_text=
        "Enter Common Name (eg, your name or your server's hostname), user will write the username of user."
    )
    email_address = models.CharField(
        max_length=30,
        default='@email.com',
        blank=False,
        help_text=
        "It will be shown as username@email.com, if common name is user. else it will be shown as @email.com"
    )
    expiration_period = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)],
        default='365',
        blank=False,
        help_text="Certificate Expiration period in days, value <= 9999")

    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = _("3. User Certificate configuration options")
        verbose_name_plural = _("3. User Certificate configuration options")


""" Model for certificate generation, will be used to update token/cert_password values
"""
class GeneratePrivateKey(models.Model):

    key_name = models.CharField(
        max_length=20,
        default='ca.key.pem',
        blank=False,
        help_text="Key identification name")
    key_password = models.CharField(
        max_length=20,
        default='',
        blank=True,
        help_text="<b><a>Enter the Certificate password</a></b>")

    def __str__(self):
        return self.key_name

    class Meta:
        verbose_name = _("1. Generate CA Private Key")
        verbose_name_plural = _("1. Generate CA Private Key")


""" Model for storing privatekey password, will be used while signing the certificates.
"""
class PrivateKeyPassword(models.Model):

    key_name = models.CharField(
        primary_key=True,
        max_length=20,
        default='Private Key',
        blank=False)
    priv_key_password = models.CharField(
        max_length=20,
        default='',
        blank=False)

    def __str__(self):
        return self.priv_key_password


""" Model for generating root certificate, This certificate will be used to sign all other certificates.
"""
class GenerateRootCertificate(models.Model):

    country_name = models.CharField(
        max_length=2,
        default='CA',
        blank=False,
        help_text="Enter 2 Letter country code")
    state_province = models.CharField(
        max_length=20,
        default='Ontario',
        blank=False,
        help_text="Enter State or Province Name (full name)")
    locality_name = models.CharField(
        max_length=20,
        default='Ottawa',
        blank=False,
        help_text="Enter Locality name (eg.city)")
    organization_name = models.CharField(
        max_length=30,
        default='No Hats Corporation',
        blank=False,
        help_text="Enter Organization name (eg. company ltd)")
    organization_unit = models.CharField(
        max_length=20,
        default='Clients',
        blank=False,
        help_text="Enter Organization unit name (eg. section name)")
    common_name = models.CharField(
        max_length=20,
        default='Libreswan.org',
        blank=False,
        help_text="Enter Common Name (eg, your name or your server's hostname)."
    )
    email_address = models.CharField(
        max_length=30,
        default='support@libreswan.org',
        blank=False,
        help_text="Enter email address")
    expiration_period = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)],
        default='665',
        blank=False,
        help_text="Certificate Expiration period in days, value <= 9999")

    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = _("2. Generate CA Root Certificate")
        verbose_name_plural = _("2. Generate CA Root Certificate")
