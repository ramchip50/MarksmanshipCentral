"""
Definition of forms.
"""

from django import forms 
from django.forms import ChoiceField, ModelForm
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from models.models import *
from app.formhelpers import *

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
    
class SessionForm(ModelForm):
    CHOICES = [
        ('Time', 'Time Based'),
        ('Turn', 'Turn Based'),
    ]
    gamelist = Game.objects.all().values_list('id','name') #Get dictionary list for populating dropdown
    game = forms.ChoiceField(choices=gamelist,widget=forms.Select(attrs={'class':'form-control'}))
    playmode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onclick':"javascript:yesnoCheck();"}), choices=CHOICES, initial='Time')
    startdate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    enddate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    turnsplayed = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    
    class Meta:
        model=Session
        fields=(
            'game',
            'startdate',
            'enddate',
            'playmode',
            'turnsplayed'
            )
          


class TRMNpartForm(ModelForm):
    
    person = forms.CharField(label="Name ")
    session = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'hidden'}))
    class Meta:
        model=SessionParticipants
        fields=(
            'person',
            'session',
#            'minutes',
#            'credits'
        )
        
 
class NonpartForm(ModelForm):
    class Meta:
        model=NonTRMNParticipants
        fields=(
		    'firstname',
		    'lastname'
#		    'session',
        ) 
        

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('memberid', 'firstname', 'lastname', 'emailaddress', 'chapter', 'branch')

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'alias', 'weapon')

class ParticipantForm(ModelForm):
    class Meta:
        model = SessionParticipants
        fields= ('session', 'person', 'minutes', 'credits')

class NonPartForm(ModelForm):
    class Meta:
        model = NonTRMNParticipants
        fields= ('session', 'emailaddress', 'firstname', 'lastname')

       

        