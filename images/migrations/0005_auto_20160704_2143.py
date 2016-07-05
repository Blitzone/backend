# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-04 21:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20160704_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertopic',
            options={'ordering': ('timestampUpdated',)},
        ),
        migrations.RemoveField(
            model_name='userchapter',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='usertopic',
            name='timestampUpdated',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 4, 21, 43, 4, 807425, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
