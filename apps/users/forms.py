from django import forms
from django.forms.models import ModelForm
from djstripe.models import Plan
from users.models import UserRole
from helpers.currency import CURRENCY_CHOICES


ROLE_TYPE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)


class UserRoleForm(ModelForm):

    role = forms.ChoiceField(
        label="Role",
        choices=ROLE_TYPE_CHOICES,
        initial=0,
        required=True
    )

    class Meta:
        model = UserRole
        fields = ('role',)


class PlanForm(ModelForm):

    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, required=True)

    class Meta:
        model = Plan
        fields = ['name', 'amount', 'currency', 'interval', 'trial_period_days']

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)