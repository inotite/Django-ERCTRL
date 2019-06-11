from django import forms
from django.core.validators import RegexValidator
CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'


class BillingForm(forms.Form):
    card_no = forms.CharField(required=True, max_length=16, validators=[
        RegexValidator(
            regex='^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$',
            message='Card No must be numeric and contain 16 digit',
        ),
    ])
    cvc = forms.CharField(required=True, max_length=3, validators=[
        RegexValidator(
            regex='^\d{1,10}$',
            message='Cvc must be numeric and contain 3 digit',
        ),
    ])
    exp_year = forms.CharField(required=True, max_length=4, validators=[
        RegexValidator(
            regex='^\d{1,10}$',
            message='Year must be numeric and contain 4 digit',
        ),
    ])
    exp_month = forms.CharField(required=True, max_length=2, validators=[
        RegexValidator(
            regex='^\d{1,10}$',
            message='Month must be numeric and contain 2 digit',
        ),
    ])
    coupon_code = forms.CharField(required=False, max_length=225)
