# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from erm_automation.models import (
    Event, EventReference, Action, ActionReference, Automation)


class EventAdmin(admin.ModelAdmin):
    pass
# list_display = ('event_id', 'event_name')
# list_display_links = ('event_id', 'event_name')
# search_fields = ('event_name',)

admin.site.register(Event, EventAdmin)


class EventReferenceAdmin(admin.ModelAdmin):
    pass
# list_display = ('erm_event_reference_id', 'event', 'event_value')
# list_display_links = ('erm_event_reference_id', 'event')
# search_fields = ('event',)

admin.site.register(EventReference, EventReferenceAdmin)


class ActionAdmin(admin.ModelAdmin):
    # list_display = ('action_id', 'action_name')
    # list_display_links = ('action_id', 'action_name')
    # search_fields = ('action_name',)
    pass

admin.site.register(Action, ActionAdmin)


class ActionReferenceAdmin(admin.ModelAdmin):
    pass
    # list_display = ('erm_action_reference_id', 'action_value', 'action_id')
    # list_display_links = ('erm_action_reference_id',
    #                       'action_value', 'action_id')
    # search_fields = ('action_id',)

admin.site.register(ActionReference, ActionReferenceAdmin)


class AutomationAdmin(admin.ModelAdmin):
    pass
    # list_display = ('automation_id', 'event_reference_value', 'action_reference_value',
    #                 'action_id', 'action_reference_id', 'event_id', 'event_reference_id')
    # list_display_links = ('automation_id', 'event_reference_value', 'action_reference_value',
    #                       'action_id', 'action_reference_id', 'event_id', 'event_reference_id')
    # search_fields = ('event_id',)

admin.site.register(Automation, AutomationAdmin)
