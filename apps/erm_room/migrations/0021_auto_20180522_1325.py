# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-22 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erm_room', '0020_puzzlessummary_play_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzlessummary',
            name='max_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='puzzlessummary',
            name='mean_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='puzzlessummary',
            name='median_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='puzzlessummary',
            name='min_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='puzzlessummary',
            name='solved_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
    ]