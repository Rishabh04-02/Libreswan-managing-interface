# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn', '0031_auto_20180629_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='generaterootcertificate',
            name='cert_name',
            field=models.CharField(default='ca.key.pem', help_text='Certificate name - Do Not Change.', max_length=20),
        ),
    ]
