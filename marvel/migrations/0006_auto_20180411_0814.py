# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-11 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel', '0005_auto_20180410_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
