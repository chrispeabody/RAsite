# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 01:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_comment_note'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
