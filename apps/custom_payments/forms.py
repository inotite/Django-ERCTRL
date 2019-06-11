from django import forms
from django.core.exceptions import NON_FIELD_ERRORS


class PaymentForm(forms.Form):
    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class CardForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput(), required=True)
    last_4_digits = forms.CharField(widget=forms.HiddenInput(), required=False)
