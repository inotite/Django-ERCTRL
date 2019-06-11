from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.utils import timezone
from erm_auth.views import BaseLoginRequired
from messages_system.models import Message, Recipient
from messages_system.forms import ComposeForm
from users.managers import UserManager


class ComposeMessage(BaseLoginRequired, CreateView):
    """
    Room view for creating an new object instance.
    """
    template_name = "messages_system/compose.html"
    form_class = ComposeForm
    success_url = reverse_lazy('user_messages')

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.sent_date = timezone.now()
        self.object.creator = self.request.user
        response = super(ComposeMessage, self).form_valid(form)
        recipient_ids = self.request.POST.get('recipient').split(",")[1:]
        for recipient_id in recipient_ids:
            Recipient.objects.create(
                message=self.object, recipient_id=recipient_id)

        return response

    def get_context_data(self, **kwargs):
        context = super(ComposeMessage, self).get_context_data(**kwargs)
        user = self.request.user
        context["recipients"] = UserManager.get_message_recipients_source(user)
        context["base_portal"] = user.profile.get_base_portal()
        return context


class InboxList(BaseLoginRequired, ListView):
    template_name = "messages_system/inbox-list.html"
    # context_object_name = 'inbox_list'
    model = Recipient

    def get_queryset(self):
        """Returns Polls that belong to the current user"""
        return Message.objects.inbox_for(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(InboxList, self).get_context_data(**kwargs)
        user = self.request.user
        context["base_portal"] = user.profile.get_base_portal()
        context["outbox_list"] = Message.objects.sent_for(user)
        return context
