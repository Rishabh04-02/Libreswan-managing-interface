# Generated by Django 2.0.6 on 2018-08-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn', '0047_auto_20180813_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpnforremotehost',
            name='dpdaction',
            field=models.CharField(blank=True, default='clear', help_text='Valid - <b><a>clear</a></b> OR <b><a>restart</a></b> OR <b><a>hold</a></b>', max_length=7),
        ),
    ]
