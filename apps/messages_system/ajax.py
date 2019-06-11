import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView
from django.utils import timezone
from messages_system.models import Message, Recipient
from erm_auth.views import BaseLoginRequired


class InboxMessageDelete(BaseLoginRequired, DeleteView):
    """Delete message from recipient model."""
    model = Recipient
    success_url = reverse_lazy('user_messages')

    @method_decorator(csrf_exempt)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.recipient_deleted_date = timezone.now()
        self.object.save()
        response_data = {"result": "ok"}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")


class OutboxMessageDelete(BaseLoginRequired, DeleteView):
    """Delete message from sender model."""
    model = Message
    success_url = reverse_lazy('user_messages')

    @method_decorator(csrf_exempt)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.creator_deleted_date = timezone.now()
        self.object.save()
        response_data = {"result": "ok"}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
