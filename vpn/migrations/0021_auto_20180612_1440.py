# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-12 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn', '0020_auto_20180612_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpnforremotehost',
            name='mobike',
            field=models.CharField(blank=True, default='no', help_text='eg. <b><a>no</a></b> OR <b><a>yes</a></b>', max_length=3),
        ),
        migrations.AlterField(
            model_name='generatecertificate',
            name='token',
            field=models.CharField(default='ddg4pexo0n70bnayxy5y', help_text='<b><a>System Generated - Do not alter</a></b>', max_length=20),
        ),
    ]
