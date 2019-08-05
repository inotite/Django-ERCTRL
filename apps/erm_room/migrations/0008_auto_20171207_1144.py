# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 11:37
from __future__ import unicode_literals

from django.db import models, migrations


def load_data(apps, schema_editor):
    Room = apps.get_model("erm_room", "Room")
    User = apps.get_model("auth", "User")
    user = User.objects.first()
    rooms = Room.objects.all()
    if user and rooms:
        for room in rooms:
            room.user = user
            room.save()


class Migration(migrations.Migration):

    dependencies = [
        ('erm_room', '0007_room_user'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]