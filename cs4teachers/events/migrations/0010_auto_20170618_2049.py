# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20170618_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('event', 'slug')]),
        ),
    ]