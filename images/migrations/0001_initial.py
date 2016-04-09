# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blitz',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('startDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigIntegerField(default=0, primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=256)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BlitzUser')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('dislikedBy', models.ManyToManyField(related_name='dislikedBy', to='accounts.BlitzUser')),
                ('likedBy', models.ManyToManyField(related_name='likedBy', to='accounts.BlitzUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BlitzUser')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.Topic'),
        ),
        migrations.AddField(
            model_name='blitz',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.Topic'),
        ),
        migrations.AddField(
            model_name='blitz',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blitzUser1', to='accounts.BlitzUser'),
        ),
        migrations.AddField(
            model_name='blitz',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blitzUser2', to='accounts.BlitzUser'),
        ),
        migrations.AddField(
            model_name='blitz',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blitzWinner', to='accounts.BlitzUser'),
        ),
    ]
