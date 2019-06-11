# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Timezone(models.Model):
    timezone = models.CharField(null=False, blank=False, max_length=255)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Timezone')
        verbose_name_plural = _('Timezones')

    def __str__(self):
        return self.timezone


class Business(models.Model):
    business_name = models.CharField(null=False, blank=False, max_length=255)
    address1 = models.CharField(null=False, blank=False, max_length=255)
    address2 = models.CharField(null=False, blank=False, max_length=255)
    city = models.CharField(null=False, blank=False, max_length=255)
    state = models.CharField(null=False, blank=False, max_length=255)
    country = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(null=False, blank=False, max_length=255)
    phone_no = models.CharField(null=False, blank=False, max_length=255)
    # timezone foreignkey
    timezone = models.ForeignKey(Timezone, related_name='timezones', null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_business", null=True)

    class Meta:
        '''
            Meta class for the model.
        '''
        verbose_name = _('Business')
        verbose_name_plural = _('Business')