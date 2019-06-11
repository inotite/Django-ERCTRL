from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation
)
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from erm_auth.models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()

        superusers = User.objects.filter(is_superuser=True)

        try:
            superuser_profile = superusers.first().profile
        except Profile.DoesNotExist:
            superuser_profile = Profile()
            superuser_profile.user = superusers.first()
            superuser_profile.save()

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile()

        profile.user = user
        profile.save()

        return user


class UserUpdateForm(ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile()

        profile.user = user
        profile.save()

        return user
