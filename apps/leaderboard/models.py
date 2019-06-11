# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from erm_room.models import LiveViewFont


class Leaderboard(models.Model):
    entries_to_display = models.IntegerField(default=0)
    background_color = models.CharField(max_length=255, default="#000000")
    column_background_color = models.CharField(max_length=255, default="#333333")
    column_week_header_color = models.CharField(max_length=255, default="#2194ca")
    column_month_header_color = models.CharField(max_length=255, default="#17a668")
    column_year_header_color = models.CharField(max_length=255, default="#da9627")
    column_alltime_header_color = models.CharField(max_length=255, default="#28b779")
    column_body_color = models.CharField(max_length=255, default="#ffffff")
    font_color = models.CharField(max_length=255, default="#ffffff")
    column_font_color = models.CharField(max_length=255, default="#000000")
    scroll_speed = models.IntegerField(default=4)
    refresh_interval = models.IntegerField(default=60)
    display_time_elapsed = models.BooleanField(default=True)
    escape_rate_label = models.CharField(max_length=255, default="Escape Rate")
    week_label = models.CharField(max_length=255, default="Current Week")
    month_label = models.CharField(max_length=255, default="Current Month")
    year_label = models.CharField(max_length=255, default="Current Year")
    all_time_label = models.CharField(max_length=255, default="All Time")
    no_winners_yet_label = models.CharField(max_length=255, default="No winners...")
    live_view_font = models.ForeignKey(
        LiveViewFont, related_name='leaderboard_live_view_fonts', null=True)
    room_name_font_size = models.IntegerField(default=94)
    room_escape_rate_font_size = models.IntegerField(default=94)
    column_header_font_size = models.IntegerField(default=94)
    team_name_font_size = models.IntegerField(default=34)
    time_font_size = models.IntegerField(default=34)
    image_height = models.IntegerField(default=34)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Leaderboard')
        verbose_name_plural = _('Leaderboards')

    def __str__(self):
        return self.escape_rate_label
