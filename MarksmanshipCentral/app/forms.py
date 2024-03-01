"""
Definition of forms.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from models.models import Person 


class signinform(forms.Form):
    email_address = forms.EmailField(max_length=255,required=True,label='Email Address',
                                     widget=forms.EmailInput)
    passwrd = forms.CharField(max_length=50, required=True,label='Password',
                               widget=forms.PasswordInput)    

    def clean(self):
        try:
            person = get_object_or_404(Person, emailaddress=self.cleaned_data["email_address"])
        except Http404:
            raise ValidationError(_('Email address not found'))
        
        if person.passwrd != self.cleaned_data["passwrd"]:
                raise ValidationError(_('Password does not match'))
          
        return self.cleaned_data["email_address"]
       

        