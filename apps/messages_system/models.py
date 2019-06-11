from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns inbox messages according to received by the given user.
        """
        return self.filter(
            recipient_messages__recipient=user,
            recipient_messages__recipient_deleted_date__isnull=True,
        )

    def sent_for(self, user):
        """
        Returns outbox messages according to sent by the given user.
        """
        return self.filter(
            creator=user,
            creator_deleted_date__isnull=True,
        )


class Message(models.Model):
    """
    Message from user to user
    """
    subject = models.CharField("Subject", max_length=140)
    message_body = models.TextField("Body")
    creator = models.ForeignKey(
        User, related_name='sent_messages', verbose_name="Sender")
    parent_message = models.ForeignKey(
        'self', related_name='upcoming_messages', null=True, blank=True,
        verbose_name="Parent message")
    sent_date = models.DateTimeField("sent at", null=True, blank=True)
    read_date = models.DateTimeField("read at", null=True, blank=True)
    replied_date = models.DateTimeField("replied at", null=True, blank=True)
    creator_deleted_date = models.DateTimeField(
        "Sender deleted date", null=True, blank=True)

    objects = MessageManager()

    def __str__(self):
        return self.subject


class Recipient(models.Model):
    """
    Recipient message from sender
    """
    message = models.ForeignKey(
        Message, related_name='recipient_messages', null=True, blank=True,
        verbose_name="Recipient")
    recipient = models.ForeignKey(
        User, related_name='received_messages', null=True, blank=True,
        verbose_name="Recipient")
    read_date = models.DateTimeField("read date", null=True, blank=True)
    recipient_deleted_date = models.DateTimeField(
        "Recipient deleted date", null=True, blank=True)
