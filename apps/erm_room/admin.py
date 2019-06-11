# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from erm_room import models


class PuzzleClueAdmin(admin.ModelAdmin):
	list_display = ('clue_type', 'created', 'updated')

admin.site.register(models.PuzzleClue, PuzzleClueAdmin)


admin.site.register(models.Theme)
admin.site.register(models.MicBiquadFilter)
admin.site.register(models.LiveViewFont)
admin.site.register(models.Room)
admin.site.register(models.Clue)
admin.site.register(models.RoomImages)
admin.site.register(models.Sounds)
admin.site.register(models.Videos)
admin.site.register(models.Puzzles)