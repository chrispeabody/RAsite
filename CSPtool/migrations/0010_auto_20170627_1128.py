# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSPtool', '0009_auto_20170627_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='idNum',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]