# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from erm_automation.models import (
    Automation, Event, Action, EventReference, ActionReference)
from erm_auth.views import BaseLoginRequired
from erm_room.models import (Room, Clue, RoomImages, Sounds, Videos, Puzzles)


class AutomationList(BaseLoginRequired, ListView):
    template_name = "automation/automation-list.html"
    model = Automation

    def get_context_data(self, **kwargs):
        context = super(AutomationList, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(
            user=self.request.user, is_tablet_room=False, is_guide_room=False)
        context['room_id'] = context['rooms'].first().id if context['rooms'] else None
        context['automations'] = Automation.objects.filter(
            room_id=context['room_id'])
        context['is_room_avaliable'] = context['rooms'].count()
        return context


class EventCreate(BaseLoginRequired, CreateView):
    template_name = "events/create_event.html"
    model = Event
    success_url = reverse_lazy('dashboard_rooms_automation')
    fields = '__all__'


class AutomationCreate(BaseLoginRequired, View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'automation/create_automation.html'

    def get_context_data(self, room_id):
        context = {}
        context['events'] = Event.objects.all()
        context['actions'] = Action.objects.all()
        context['clues'] = Clue.objects.filter(
            room=room_id).values("id", "name")
        context['images'] = RoomImages.objects.filter(room=room_id)
        context['sounds'] = Sounds.objects.filter(room=room_id)
        context['videos'] = Videos.objects.filter(room=room_id)
        context['puzzles'] = Puzzles.objects.filter(room=room_id)
        context['room'] = Room.objects.get(id=room_id)
        context['room_id'] = room_id
        return context

    def create_or_update_automation(self, room_id):
        data = json.loads(self.request.POST.get("data_json"))
        event_data = data.get('event_fields')
        event_reference = EventReference(**event_data)
        event_reference.save()
        action_datas = data.get('action_fields')
        for action_data in action_datas:
            action_reference = ActionReference(**action_data)
            action_reference.save()
            automation, status = Automation.objects.get_or_create(
                event_reference=event_reference,
                room_id=room_id)
            automation.action_reference.add(action_reference)
        return

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        context = self.get_context_data(kwargs.get('pk'))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.create_or_update_automation(kwargs.get('pk'))
        context = self.get_context_data(kwargs.get('pk'))
        # if form.is_valid():
        # <process form cleaned data>
        if context:
            messages.success(request, 'Automation was successfully added!')
            return redirect('dashboard_rooms_automation')

        return render(request, self.template_name, context)


class AutomationUpdate(BaseLoginRequired, View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    template_name = 'automation/edit_automation.html'

    def create_or_update_automation(self, room_id):
        data = json.loads(self.request.POST.get("data_json"))
        event_data = data.get('event_fields')
        event_reference = EventReference(**event_data)
        event_reference.save()
        action_datas = data.get('action_fields')
        for action_data in action_datas:
            action_reference = ActionReference(**action_data)
            action_reference.save()
            automation, status = Automation.objects.get_or_create(
                event_reference=event_reference,
                room_id=room_id)
            automation.action_reference.add(action_reference)
        return

    def get_context_data(self, **kwargs):
        context = {}
        room_id = kwargs.get('room_id')
        automation_id = kwargs.get('automation_id')
        automation = Automation.objects.get(id=automation_id)
        event_references = automation.event_reference
        action_references = automation.action_reference.all()
        context['events'] = Event.objects.all()
        context['actions'] = Action.objects.all()
        context['room_id'] = room_id
        context['automation_id'] = automation_id
        context['automation'] = automation
        context['event_reference'] = event_references
        context['action_references'] = action_references
        context['images'] = RoomImages.objects.filter(room=room_id)
        context['sounds'] = Sounds.objects.filter(room=room_id)
        context['videos'] = Videos.objects.filter(room=room_id)
        context['puzzles'] = Puzzles.objects.filter(room=room_id)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for action_reference in context['action_references']:
            context['automation'].action_reference.remove(action_reference)
            action_reference.delete()
        context['automation'].delete()
        context['event_reference'].delete()
        self.create_or_update_automation(kwargs.get('room_id'))
        if context['automation']:
            messages.success(request, 'Automation was successfully update!')
            return redirect('dashboard_rooms_automation')
        return render(request, self.template_name, context)


class AutomationCreateOrUpdate(BaseLoginRequired, View):

    def get_template_name(self, is_edit=False):
        if is_edit:
            template_name = 'automation/edit_automation.html'
        else:
            template_name = 'automation/create_automation.html'
        return template_name

    def get_context_data(self, **kwargs):
        context = {}
        automation_id = kwargs.get('automation_id')
        room_id = kwargs.get('room_id') if automation_id else kwargs.get('pk')
        context['room'] = Room.objects.get(id=room_id)
        phSetting, phGroups, phScenes = context['room'].get_groups_and_scenes_by_ph_settings()
        context['events'] = Event.objects.all()
        context['actions'] = Action.objects.all().order_by("action_name")
        context['images'] = RoomImages.objects.filter(room=room_id)
        context['sounds'] = Sounds.objects.filter(room=room_id)
        context['videos'] = Videos.objects.filter(room=room_id)
        context['puzzles'] = Puzzles.objects.filter(room=room_id)
        context['room_id'] = room_id
        context['phSetting'] = phSetting
        context['phGroups'] = phGroups
        context['phScenes'] = phScenes

        if automation_id:
            automation = Automation.objects.get(id=automation_id)
            event_references = automation.event_reference
            action_references = automation.action_reference.all()
            context['event_reference'] = event_references
            context['action_references'] = action_references
            context['automation_id'] = automation_id
            context['automation'] = automation
            context['action_reference_count'] = action_references.count()
        return context

    def create_or_update_automation(self, room_id):
        data = json.loads(self.request.POST.get("data_json"))
        event_data = data.get('event_fields')
        event_reference = EventReference(**event_data)
        event_reference.save()
        action_datas = data.get('action_fields')
        for action_data in action_datas:
            action_reference = ActionReference(**action_data)
            action_reference.save()
            automation, status = Automation.objects.get_or_create(
                event_reference=event_reference,
                room_id=room_id)
            automation.action_reference.add(action_reference)
        return

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        is_edit = False if kwargs.get('pk') else True
        return render(request, self.get_template_name(is_edit), context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('automation_id'):
            for action_reference in context['action_references']:
                context['automation'].action_reference.remove(action_reference)
                action_reference.delete()
            context['automation'].delete()
            context['event_reference'].delete()
            self.create_or_update_automation(kwargs.get('room_id'))
            message = 'Automation was successfully updated!'
        else:
            self.create_or_update_automation(kwargs.get('pk'))
            message = 'Automation was successfully added!'

        if context:
            messages.success(request, message)
            return redirect('dashboard_rooms_automation')
        is_edit = False if kwargs.get('pk') else True
        return render(request, self.get_template_name(is_edit), context)
