# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm_automation', '0010_automation_action_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventreference',
            name='event_sec',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]