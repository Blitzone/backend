# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-04 21:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20160704_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertopic',
            options={'ordering': ('-timestampUpdated',)},
        ),
    ]