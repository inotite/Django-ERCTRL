# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import collections
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from picklefield.fields import PickledObjectField
from phue import Bridge, PhueRequestTimeout
from socket import error as socket_error
from datetime import datetime

EVENT_NO_FIELDS = ['Timer Started', 'Timer Stopped', 'Room Completed',
                   'Room Failed', 'Room Reset']
ACTION_NO_FIELDS = ['Play Alert Tone', 'Start Timer', 'Stop Timer',
                    'Complete Room', 'Fail Room', 'Reset Room',
                    'Start Video Brief', 'Start Soundtrack',
                    'Stop Soundtrack', 'Request Clue from GM']
NETWORK_POLLING = 'Network Polling (Listen for Prop)'
SEND_NETWORK_REQUEST = 'Send Network Request (Trigger Prop)'
PH_ON_OFF = 'Philips Hue Lights on/off'

CHOICE = (
    ('0', 'No'),
    ('1', 'Yes'),
)

ENDING_GAME_CHIOCE = (
    ('video ending', 'video ending'),
    ('text ending', 'text ending')
)


def get_upload_path(instance, filename):
    timestamp = slugify(timezone.now().isoformat()) + "-"
    # fs = FileSystemStorage(location='/media/photos')
    return os.path.join("avatars", timestamp + filename)


class Theme(models.Model):
    theme_name = models.CharField(null=False, max_length=255, blank=False)
    theme_image = models.CharField(null=False, max_length=255, blank=False)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return self.theme_name


class MicBiquadFilter(models.Model):
    name = models.CharField(null=False, max_length=255, blank=False)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Mic Biquad Filter')
        verbose_name_plural = _('Mic Biquad Filters')

    def __str__(self):
        return self.name


class LiveViewFont(models.Model):
    font_name = models.CharField(null=False, blank=False, max_length=255)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Live View Font')
        verbose_name_plural = _('Live View Fonts')
        ordering = ('id',)

    def __str__(self):
        return self.font_name

    @property
    def get_short_font_name(self):
        try:
            if self.font_name.split(",")[0] == 'Digital-7':
                return 'Digital 7'
            if self.font_name.split(",")[0] == 'Katalyst active BRK':
                return 'Katalyst Hollow'
            if self.font_name.split(",")[0] == 'Katalyst inactive BRK':
                return 'Katalyst Solid'
            return self.font_name.split(",")[0].replace("'", "")
        except IndexError:
            return ""


class Room(models.Model):
    room_name = models.CharField(null=False, blank=False, max_length=255)
    default_time_limit = models.IntegerField(blank=True, default=60, null=True)
    num_clues = models.IntegerField(blank=True, null=True)

    clue_label = models.CharField(null=False, blank=False, max_length=255)
    time_remaining_label = models.CharField(
        null=False, blank=False, max_length=255)
    communication_box_label = models.CharField(
        null=False, blank=False, max_length=255)
    initial_data_feed_text = models.CharField(
        null=False, blank=False, max_length=255)

    success_screen_header = models.CharField(
        null=False, blank=False, max_length=255)
    success_screen_footer = models.CharField(
        null=False, blank=False, max_length=255)
    failure_screen_header = models.CharField(
        null=False, blank=False, max_length=255)
    failure_screen_footer = models.CharField(
        null=False, blank=False, max_length=255)
    hide_time_remaining_on_failure = models.BooleanField(default=False)
    # Theme foreign key
    theme = models.ForeignKey(Theme, related_name='erm_theme', null=True)
    logo = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    logo_max_height = models.IntegerField(blank=True, null=True)
    font_color = models.CharField(null=False, blank=False, max_length=255)
    background_color = models.CharField(
        null=False, blank=False, max_length=255)
    widget_header_color = models.CharField(
        null=False, blank=False, max_length=255)
    widget_body_color = models.CharField(
        null=False, blank=False, max_length=255)
    game_end_screen_font_color = models.CharField(
        null=False, blank=False, max_length=255)
    game_end_screen_background_color = models.CharField(
        null=False, blank=False, max_length=255)
    transparent_data_feed_background = models.BooleanField(default=False)
    transparent_timer_background = models.BooleanField(default=False)
    override_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)
    custom_header_includes = models.TextField(blank=True, null=True)

    hide_data_feed = models.BooleanField(default=False)
    hide_timer = models.BooleanField(default=False)
    data_feed_distance_from_top = models.IntegerField(blank=True, null=True)
    data_feed_distance_from_left = models.IntegerField(blank=True, null=True)
    timer_distance_from_top = models.IntegerField(blank=True, null=True)
    timer_distance_from_left = models.IntegerField(blank=True, null=True)
    overlay_image = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    # overlay_image = ImageField(
    #     max_length=250,
    #     upload_to=get_upload_path,
    #     blank=True,
    #     null=True
    # )
    clue_count_off_img = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    clue_count_available_img = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    clue_count_used_img = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    clue_count_img_width = models.IntegerField(
        blank=True, null=True, default=72)

    background_video = models.FileField(max_length=255,
                                        upload_to=get_upload_path,
                                        null=True, blank=True)
    loop_background_video = models.BooleanField(default=True)
    start_background_video_on_timer_start = models.BooleanField(default=False)
    override_default_timer = models.BooleanField(default=False)
    background_image = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    end_game_success_background = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    end_game_failure_background = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    soundtrack = models.FileField(max_length=255,
                                  upload_to=get_upload_path,
                                  null=True, blank=True)
    loop_soundtrack = models.BooleanField(default=False)
    success_audio = models.FileField(max_length=255,
                                     upload_to=get_upload_path,
                                     null=True, blank=True)
    failed_audio = models.FileField(max_length=255,
                                    upload_to=get_upload_path,
                                    null=True, blank=True)
    audio_alert = models.FileField(max_length=255,
                                   upload_to=get_upload_path,
                                   null=True, blank=True)
    audio_alert_on_clue_send = models.BooleanField(default=False)
    audio_alert_on_image_clue_send = models.BooleanField(default=False)
    audio_alert_on_clue_count_change = models.BooleanField(default=False)
    play_soundtrack_on_timer_start = models.BooleanField(default=False)
    # mic_biquad_filter foreign key
    mic_biquad_filter = models.ForeignKey(
        MicBiquadFilter, related_name='room_mic_biquad_filters', null=True)

    video_brief = models.FileField(max_length=255,
                                   upload_to=get_upload_path,
                                   null=True, blank=True)
    start_timer_after_video_brief = models.BooleanField(default=True)
    success_video = models.FileField(max_length=255,
                                     upload_to=get_upload_path,
                                     null=True, blank=True)
    fail_video = models.FileField(max_length=255,
                                  upload_to=get_upload_path,
                                  null=True, blank=True)
    success_screen_after_success_video = models.BooleanField(default=True)
    fail_screen_after_fail_video = models.BooleanField(default=True)

    # Live view Font foreign key

    live_view_font = models.ForeignKey(
        LiveViewFont, related_name='room_live_view_fonts', null=True)
    header_font_size = models.IntegerField(blank=True, null=True)
    timer_font_size = models.IntegerField(blank=True, null=True)
    clue_label_font_size = models.IntegerField(blank=True, null=True)
    text_clue_font_size = models.IntegerField(blank=True, null=True)
    room_end_header_font_size = models.IntegerField(blank=True, null=True)
    room_end_footer_font_size = models.IntegerField(blank=True, null=True)
    room_end_time_font_size = models.IntegerField(blank=True, null=True)
    leaderboard_image = ImageField(
        max_length=250,
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    leaderboard_room_description = models.TextField(blank=True, null=True)

    display_polling_output = models.BooleanField(default=False)
    lap_timer = models.BooleanField(default=False)

    enable_time_warp = models.BooleanField(default=False)
    display_timer_milliseconds = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_rooms", null=True)
    is_tablet_room = models.BooleanField(default=False)
    is_guide_room = models.BooleanField(default=False)
    admin_pin = models.CharField(
        null=False, blank=False, max_length=4)
    hint = models.BooleanField(default=False)
    final_code = models.CharField(max_length=255, blank=True, null=True)
    hint_tap_exit = models.BooleanField(default=True)
    hints_full_screen = models.BooleanField(default=True)
    success_timer_size = models.IntegerField(blank=True, null=True)
    success_hide_timer = models.BooleanField(default=False)
    fail_font_size = models.IntegerField(blank=True, null=True)
    fail_timer_size = models.IntegerField(blank=True, null=True)
    fail_hide_timer = models.BooleanField(default=False)
    success_ending_type = models.CharField(
        choices=ENDING_GAME_CHIOCE, max_length=255, default='Video Ending')
    fail_ending_type = models.CharField(
        choices=ENDING_GAME_CHIOCE, max_length=255, default='Video Ending')


    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return self.room_name

    def event_and_action_json(self, r_type=None):
        eventActionList = []
        room_automations = self.room_automations.all()

        for room_automation in room_automations:
            event_action_dict = collections.OrderedDict()
            event_reference = room_automation.event_reference
            if event_reference.event.event_name == NETWORK_POLLING:
                method_name = 'get_network_polling_fields'
            elif event_reference.event.event_name in EVENT_NO_FIELDS:
                method_name = 'get_event_no_fields'
            else:
                method_name = event_reference.generate_method_name()

            event_action_dict['event'] = getattr(
                event_reference, method_name)()
            event_actions = room_automation.action_reference.all()
            actionList = []

            for event_action in event_actions:
                action_dict = {}
                if event_action.action.action_name == SEND_NETWORK_REQUEST:
                    action_method_name = 'get_send_network_request_fields'
                elif event_action.action.action_name in ACTION_NO_FIELDS:
                    action_method_name = 'get_action_no_fields'
                elif event_action.action.action_name in PH_ON_OFF:
                    action_method_name = 'get_philips_hue_lights_on_or_off_fields'
                else:
                    action_method_name = event_action.generate_method_name()
                action_dict = getattr(event_action, action_method_name)()
                actionList.append(action_dict)
            event_action_dict['actions'] = actionList
            eventActionList.append(event_action_dict)
        if r_type == 'json':
            return json.dumps(eventActionList)
        return eventActionList

    def custom_event_of_actions(self):
        room_automations = self.room_automations.filter(
            event_reference__event__event_name='Custom Button'
        ).values_list("id", "event_reference__button_label")
        return room_automations

    def get_groups_and_scenes_by_ph_settings(self):
        try:
            phSetting = self.room_philip_group_and_scene.all().first()
            b = Bridge(phSetting.bridge_url, username=phSetting.username)
            b.connect()
            # import pdb;pdb.set_trace()
            phGroups = b.get_group()
            phScenes = b.get_scene()
        except (AttributeError, socket_error, PhueRequestTimeout):
            phSetting = None
            phGroups = []
            phScenes = []
        return phSetting, phGroups, phScenes


class Clue(models.Model):
    name = models.TextField(blank=True, null=True)
    room = models.ForeignKey(
        Room, related_name='room_clues', null=True, on_delete=models.CASCADE)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Clue')
        verbose_name_plural = _('Clues')

    def __str__(self):
        return self.name


class RoomImages(models.Model):
    img_name = models.FileField(max_length=255,
                                upload_to=get_upload_path,
                                null=False, blank=False)
    room = models.ForeignKey(
        Room, related_name='room_images', null=True, on_delete=models.CASCADE)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('RoomImage')
        verbose_name_plural = _('RoomImages')


class Sounds(models.Model):
    sound_img = models.FileField(max_length=255,
                                 upload_to=get_upload_path,
                                 null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=255)
    room = models.ForeignKey(
        Room, related_name='room_sounds', null=True, on_delete=models.CASCADE)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Sound')
        verbose_name_plural = _('Sounds')

    def __str__(self):
        return self.name

    @property
    def get_audio_url(self):
        return self.sound_img.url

    @property
    def get_audio_filetype(self):
        name, extension = os.path.splitext(self.sound_img.name)
        if extension == '.mp3':
            return 'audio/mpeg'
        else:
            return 'audio/ogg'


class Videos(models.Model):
    video_img = models.FileField(max_length=255,
                                 upload_to=get_upload_path,
                                 null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=255)
    room = models.ForeignKey(
        Room, related_name='room_videos', null=True, on_delete=models.CASCADE)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return self.name

    @property
    def get_video_url(self):
        return self.video_img.url

    @property
    def get_video_filetype(self):
        name, extension = os.path.splitext(self.video_img.name)
        if extension == '.mp4':
            return 'video/mp4'
        else:
            return 'video/ogg'


class Puzzles(models.Model):
    puzzle_name = models.CharField(null=False, blank=False, max_length=255)
    reset_instructions = models.TextField(blank=True, null=True)
    damage_or_notes = models.TextField(blank=True, null=True)
    room = models.ForeignKey(
        Room, related_name='room_puzzles', null=True, on_delete=models.CASCADE)
    # used for self guided room
    enabled_puzzle_clue = models.BooleanField(default=False)
    dashboard_icon = models.ImageField(
        max_length=255, upload_to=get_upload_path, blank=True, null=True)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Puzzle')
        verbose_name_plural = _('Puzzles')

    def __str__(self):
        return self.puzzle_name

class PuzzlesSummary(models.Model):
    min_time = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=9)
    max_time = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=9)
    mean_time = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=9)
    median_time = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=9)
    solved_time = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=9)
    puzzle = models.ForeignKey(
        Puzzles, related_name='room_puzzles_spummary', null=True,
        on_delete=models.CASCADE)
    play_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_puzzles_summary",
        null=True)
    play_count = models.IntegerField(blank=True, null=True)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('PuzzleSummary')
        verbose_name_plural = _('PuzzlesSummary')


class GameRecord(models.Model):
    room = models.ForeignKey(Room, related_name='game_records', null=True, on_delete=models.CASCADE)
    # team name
    team_name = models.CharField(null=False, blank=False, max_length=255)
    # time left in seconds
    time_remaining = models.IntegerField(default=3600)
    # number of players
    num_players = models.IntegerField(default=4)
    # number of clues given 
    num_clues = models.IntegerField(default=0)
    # completed date
    completed_on = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        #self.consumed_time = float(self.consumed_time.replace(':', '.'))
        #self.game_time = float(self.room.default_time_limit)
        if self.team_name is None:
            self.team_name = 'Unnamed'
        if self.completed_on is None:
            self.completed_on = timezone.now()
        
        print(self.team_name, self.completed_on, self.time_remaining, self.num_clues, self.num_players)
        super(GameRecord, self).save(*args, **kwargs)


class Scoring(models.Model):
    enable_scoring = models.BooleanField(default=False)
    starting_score = models.IntegerField(blank=True, null=True)
    score_title = models.CharField(null=True, blank=True, max_length=255)
    always_reduce = models.BooleanField(default=False)
    penalty_per_minute = models.IntegerField(blank=True, null=True)
    is_penalize = models.BooleanField(default=False)
    end_game_at_zero = models.BooleanField(default=False)
    room = models.OneToOneField(
        Room, related_name='room_scoring', null=True, on_delete=models.CASCADE)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Scoring')
        verbose_name_plural = _('Scorings')

    def __str__(self):
        return self.score_title


class PuzzleClue(models.Model):
    puzzle = models.ForeignKey(
        Puzzles, null=True, blank=True, on_delete=models.CASCADE)
    clue_type = models.CharField(
        max_length=255, null=True, blank=True)
    clue_uploads_options = models.CharField(
        max_length=255, null=True, blank=True)
    clue_textarea = models.TextField(null=True, blank=True)
    clue_file_uploads = models.FileField(
        max_length=255, upload_to=get_upload_path, null=True, blank=True)
    clue_icon = models.ImageField(
        max_length=255, upload_to=get_upload_path, blank=True, null=True)
    clue_checkbox = models.BooleanField(default=False)
    score_penatly = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(
        auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return self.clue_type


class PhilipGroupsAndScenes(models.Model):
    username = models.CharField(
        max_length=255, null=True, blank=True)
    bridge_url = models.CharField(
        max_length=255, null=True, blank=True)
    settings_data = PickledObjectField(default={})
    room = models.ForeignKey(
        Room, related_name='room_philip_group_and_scene', null=True,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_philip_group_and_scene", null=True)
