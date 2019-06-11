from django.forms import ModelForm
from django import forms
from erm_business.models import Business
from helpers.countries import COUNTRIES


class BusinessForm(ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES, required=True)

    class Meta:
        model = Business
        fields = ['business_name', 'address1', 'address2',
                  'country', 'state', 'city', 'zipcode', 'phone_no']

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        # timezones = Timezone.objects.all()
        # self.fields['timezone'].queryset = timezones
