# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from erm_business.models import Timezone, Business

admin.site.register(Timezone)
admin.site.register(Business)
