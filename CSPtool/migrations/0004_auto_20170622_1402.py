# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSPtool', '0003_auto_20170620_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csp',
            name='id',
        ),
        migrations.AlterField(
            model_name='csp',
            name='name',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]
