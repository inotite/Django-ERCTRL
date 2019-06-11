# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'


# class Billing(models.Model):
#     # card_no = models.CharField(null=False, blank=False, max_length=20)
#     card_no = models.CharField(
#         max_length=20,
#         validators=[
#             RegexValidator(
#                 regex='^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$',
#                 message='Card No must be numeric and contain 16-20 digit',
#             ),
#         ]
#     )
#     cvc = models.CharField(
#         max_length=3,
#         validators=[
#             RegexValidator(
#                 regex='^\d{1,10}$',
#                 message='Cvc must be numeric and contain 3 digit',
#             ),
#         ]
#     )
#     exp_month = models.CharField(
#         max_length=2,
#         validators=[
#             RegexValidator(
#                 regex='^\d{1,10}$',
#                 message='Month must be numeric and contain 2 digit',
#             ),
#         ]
#     )
#     exp_year = models.CharField(
#         max_length=4,
#         validators=[
#             RegexValidator(
#                 regex='^\d{1,10}$',
#                 message='Year must be numeric and contain 4 digit',
#             ),
#         ]
#     )
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name="user_billing", null=True)

#     class Meta:
#         '''
#             Meta class for the model.
#         '''
#         verbose_name = _('Billing')
#         verbose_name_plural = _('Billings')
