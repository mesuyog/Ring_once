import re
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

    def clean_phone(self):
        return self.cleaned_data['phone']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'phone')