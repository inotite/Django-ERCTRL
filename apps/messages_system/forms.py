from django import forms
from django.utils.translation import ugettext_lazy as _
from messages_system.models import Message


class ComposeForm(forms.ModelForm):
    """
    A simple default form for private messages.
    """
    recipient = forms.CharField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=140)
    message_body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '12', 'cols': '55'}))

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'message_body']

    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)

    # def save(self, sender):
    #     from django.utils import timezone
    #     import pytz
    #     timezone.now()
    #     import pdb;pdb.set_trace()
    #     recipient_ids = self.cleaned_data.get('recipient').split(",")[1:]
    #     for recipient_id in recipient_ids:
    #         Recipient.objects.create(
    #             message=self.instance, recipient_id=recipient_id)
    #     return self.instance

        # recipient = Recipient()
        # recipient

        # recipients = self.cleaned_data['recipient']
        # subject = self.cleaned_data['subject']
        # body = self.cleaned_data['body']
        # message_list = []
        # for r in recipients:
        #     msg = Message(
        #         sender=sender,
        #         recipient=r,
        #         subject=subject,
        #         body=body,
        #     )
        #     if parent_msg is not None:
        #         msg.parent_msg = parent_msg
        #         parent_msg.replied_at = timezone.now()
        #         parent_msg.save()
        #     msg.save()
        #     message_list.append(msg)
        #     if notification:
        #         if parent_msg is not None:
        #             notification.send([sender], "messages_replied", {
        #                               'message': msg, })
        #             notification.send([r], "messages_reply_received", {
        #                               'message': msg, })
        #         else:
        #             notification.send([sender], "messages_sent", {
        #                               'message': msg, })
        #             notification.send([r], "messages_received", {
        #                               'message': msg, })
        # return message_list
