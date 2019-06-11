import json
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.generic.edit import DeleteView
from django.http import HttpResponse
from erm_auth.views import BaseLoginRequired
from erm_automation.models import (
    Automation, Event, Action, EventReference, ActionReference, Automation)


class RoomByAutomationDetailView(BaseLoginRequired, DetailView):
    template_name = "rooms/room_details.html"
    model = Automation

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(RoomByAutomationDetailView,
                     self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            room_id = kwargs.get('pk')
            automations = Automation.objects.filter(room_id=room_id)
            html_content = render_to_string(
                "automation/include/_automation-tr.html",
                {'automations': automations, 'room_id': room_id})
            return HttpResponse(json.dumps({'automation_data': html_content}),
                                status=200, content_type="application/json")
        else:
            return resp


class AutomationDelete(BaseLoginRequired, DeleteView):
    model = Automation
    success_url = reverse_lazy('dashboard_rooms_automation')

    @method_decorator(csrf_exempt)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        action_references = self.object.action_reference.all()
        for action_reference in action_references:
            self.object.action_reference.remove(action_reference)
            action_reference.delete()
        self.object.event_reference.delete()
        self.object.delete()
        response_data = {"result": "ok"}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
