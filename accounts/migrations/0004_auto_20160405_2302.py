# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_blitzuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blitzuser',
            name='avatar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='images.Image'),
        ),
    ]
