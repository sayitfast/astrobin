# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-22 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrobin', '0059_userprofile_shadow_bans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='is_wip',
            field=models.BooleanField(default=False),
        ),
    ]