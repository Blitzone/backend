# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigIntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
