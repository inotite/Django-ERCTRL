# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from erm_room.models import (Room, Clue, RoomImages, Sounds, Videos, Puzzles,
                             LiveViewFont, MicBiquadFilter)

EVENT_DICT = {
    'timeElapse': 'Time Elapsed',
    'timerStart': 'Timer Started',
    'timerStop': 'Timer Stopped',
    'roomComplet': 'Room Completed',
    'roomFail': 'Room Failed',
    'roomReset': 'Room Reset',
    'networkPolling': 'Network Polling (Listen for Prop)',
    'customButton': 'Custom Button',
    'customEvent': 'Custom Event'
}

ACTIONS_DICT = {
    'sendClueText': 'Send Clue Text',
    'playAlert': 'Play Alert Tone',
    'playSound': 'Play Sound',
    'playVideo': 'Play Video',
    'displayImage': 'Display Image',
    'networkRequest': 'Send Network Request (Trigger Prop)',
    'completePuzzle': 'Complete Puzzle',
    'philipsHue': 'Philips Hue Lights Scene',
    'philipsHueBlink': 'Philips Hue Lights Blink',
    'startTimer': 'Start Timer',
    'stopTimer': 'Stop Timer',
    'adjustTime': 'Adjust Time',
    'completeRoom': 'Complete Room',
    'failRoom': 'Fail Room',
    'resetRoom': 'Reset Room',
    'playIntroVideo': 'Start Video Brief',
    'startSoundtrack': 'Start Soundtrack',
    'stopSoundtrack': 'Stop Soundtrack',
    'requestClue': 'Request Clue from GM',
    'customScript': 'Run Script'
}


class Event(models.Model):
    event_name = models.CharField(null=False, blank=False, max_length=255)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.event_name

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('id',)


class EventReference(models.Model):
    event = models.ForeignKey(Event, related_name="events")
    # event_max = models.IntegerField(blank=True, null=True)
    event_sec = models.IntegerField(blank=True, null=True)
    event_min = models.IntegerField(blank=True, null=True)
    url = models.CharField(null=True, blank=True, max_length=255)
    trigger_value = models.CharField(null=True, blank=True, max_length=255)
    poll_interval = models.IntegerField(blank=True, null=True)
    button_label = models.CharField(null=True, blank=True, max_length=255)
    trigger_event_name = models.CharField(
        null=True, blank=True, max_length=255)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Event Reference')
        verbose_name_plural = _('Events References')

    def generate_method_name(self):
        event_name = self.event.event_name.split(" ")
        method_name = 'get_' + event_name[0].lower() + '_' + event_name[1].lower() + '_fields'
        return method_name

    @property
    def generate_event_type(self):
        event_name = self.event.event_name.split(" ")
        event_type = event_name[0].lower() + event_name[1]
        return event_type

    def get_time_elapsed_fields(self):
        return {'type': 'timeElapsed',
                'sec': self.event_sec,
                'min': self.event_min,
                'id': self.id}

    def get_network_polling_fields(self):
        return {'type': 'networkPoll',
                'url': self.url,
                'trigger_value': self.trigger_value,
                'poll_interval': self.poll_interval,
                'id': self.id}

    def get_custom_event_fields(self):
        return {'type': 'customEvent',
                'trigger_event_name': self.trigger_event_name,
                'id': self.id}

    def get_custom_button_fields(self):
        return {'type': 'customButton',
                'button_label': self.button_label,
                'id': self.id}

    def get_event_no_fields(self):
        return {'type': self.generate_event_type, 'id': self.id}


class Action(models.Model):
    action_name = models.CharField(null=False, blank=False, max_length=255)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
        ordering = ('id',)

    def __str__(self):
        return self.action_name


class ActionReference(models.Model):
    action = models.ForeignKey(Action, related_name="action_reference_actions")
    clue_text = models.CharField(null=True, blank=True, max_length=255)
    sound = models.ForeignKey(
        Sounds, related_name="action_reference_sounds", null=True, blank=True)
    video = models.ForeignKey(
        Videos, related_name="action_reference_videos", null=True, blank=True)
    room_images = models.ForeignKey(
        RoomImages, related_name="action_reference_room_images", null=True,
        blank=True)
    puzzle = models.ForeignKey(
        Puzzles, related_name="action_reference_puzzles", null=True,
        blank=True)
    blink_interval = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_to_adjust = models.IntegerField(blank=True, null=True)
    script_name = models.CharField(null=True, blank=True, max_length=255)
    script_text = models.TextField(blank=True, null=True)
    url = models.CharField(null=True, blank=True, max_length=255)
    group_id = models.IntegerField(null=True, blank=True)
    scene_id = models.CharField(null=True, blank=True, max_length=255)
    light_state = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Action Reference')
        verbose_name_plural = _('Action References')

    def generate_method_name(self):
        action_name = self.action.action_name.lower().replace(" ", "_")
        method_name = 'get_' + action_name + '_fields'
        return method_name

    @property
    def generate_action_type(self):
        firstLetterSmall = lambda s: s[:1].lower() + s[1:] if s else ''
        return firstLetterSmall(self.action.action_name).replace(" ", "")

    def get_send_clue_text_fields(self):
        return {'type': 'sendClueText',
                'clueText': self.clue_text,
                'id': self.id}

    def get_play_sound_fields(self):
        return {'type': 'playSound',
                'soundId': self.sound.id,
                'id': self.id}

    def get_play_video_fields(self):
        return {'type': 'playVideo',
                'videoId': self.video.id, 'id': self.id}

    def get_display_image_fields(self):
        return {'type': 'displayImage',
                'imageUrl': self.room_images.img_name.url, 'id': self.id}

    def get_complete_puzzle_fields(self):
        return {'type': 'completePuzzle',
                'puzzleId': self.puzzle.id, 'id': self.id}

    def get_philips_hue_lights_scene_fields(self):
        return {'type': 'philipsHue', 'scene_id': self.scene_id,
                'group_id': self.group_id, 'id': self.id}

    def get_philips_hue_lights_blink_fields(self):
        return {'type': 'philipsHueBlink',
                "duration": self.duration, "group": self.group_id,
                "interval": self.blink_interval, 'id': self.id}

    def get_adjust_time_fields(self):
        return {'type': 'adjustTime',
                'time_to_adjust': self.time_to_adjust, 'id': self.id}

    def get_run_script_fields(self):
        try:
            script_text = json.dumps(self.script_text)[:-1].replace('"$', "$");
        except IndexError:
            script_text = ""
        return {'type': 'customScript',
                'script_name': self.script_name,
                'script_text': script_text, 'id': self.id}

    def get_send_network_request_fields(self):
        return {'type': 'networkRequest',
                'url': self.url, 'id': self.id}

    def get_action_no_fields(self):
        return {'type': self.generate_action_type, 'id': self.id}

    def get_philips_hue_lights_on_or_off_fields(self):
        return {'type': 'phHueOnOff',
                "light_state": self.light_state, "group": self.group_id,
                'id': self.id}


class Automation(models.Model):
    event_reference = models.ForeignKey(
        EventReference, related_name="automation_event_references")
    action_reference = models.ManyToManyField(
        ActionReference, related_name="automations_action_references")
    room = models.ForeignKey(
        Room, null=True, on_delete=models.CASCADE,
        related_name='room_automations')

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Automation')
        verbose_name_plural = _('Automations')