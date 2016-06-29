import re

from string import punctuation

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import forms as auth_forms

from .models import User


def good_password(password):
    if len(password) < 8:
        return False

    score = 0

    if re.search('[0-9]', password):
        score += 1
    if re.search('[a-z]', password):
        score += 1
    if re.search('[A-Z]', password):
        score += 1
    if re.search('[%s]' % punctuation, password):
        score += 1

    return score > 2


class ProfileCreationForm(auth_forms.UserCreationForm):
    def clean_password1(self):
        if not good_password(self.cleaned_data['password1']):
            raise ValidationError('Too simple password.')

        return self.cleaned_data['password1']

    class Meta:
        model = User
        fields = ('username',)


class RegistrationForm(ProfileCreationForm):
    email = forms.EmailField(label='email address', required=True)

    class Meta(ProfileCreationForm.Meta):
        fields = ProfileCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('Email (%s) already in use.' % self.cleaned_data['email'])

        return self.cleaned_data['email']


class SetPasswordFormMixin(forms.Form):
    def clean_new_password1(self):
        if not good_password(self.cleaned_data['new_password1']):
            raise ValidationError('Too simple password.')

        return self.cleaned_data['new_password1']


class UserPasswordChangeForm(auth_forms.PasswordChangeForm, SetPasswordFormMixin):
    pass


class UserPasswordSetForm(auth_forms.SetPasswordForm, SetPasswordFormMixin):
    pass


class UserPasswordResetForm(auth_forms.PasswordResetForm):
    def clean_email(self):
        if not User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('User with such e-mail address not exist.')

        return self.cleaned_data['email']
