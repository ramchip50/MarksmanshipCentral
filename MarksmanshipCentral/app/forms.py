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

#region Fields

class GameField(forms.CharField):
    widget=forms.TextInput(attrs={'style':'width:500px','class':'basicAutoComplete formcontrol',
           'placeholder':'Type name to search','data-url':'/game_autocomplete/','autocomplete':'off'})

    def validate(self,value):
        try:
           Game.active_objects.get(name=value)
           return
        except:
            raise ValidationError(_('Game not in directory. Go to New Game page to add it'))

class PlayerField(forms.CharField):
    widget=forms.TextInput(attrs={'style':'width:500px','class':'basicAutoComplete formcontrol',
           'placeholder':'Type name to search','data-url':'/member_autocomplete/','autocomplete':'off'})
     
    def validate(self,value):
        try:
           names=value.split(',')
           p=Person.active_objects.get(lastname=names[0].strip(),firstname=names[1].strip())
           return
        except:
            raise ValidationError(_('Member not found in roster'))  






#endregion

#region Forms




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
    
class SessionForm(forms.Form):
    CHOICES = [
        ('Time', 'Time Based'),
        ('Turn', 'Turn Based'),
    ]
    game = GameField()
    playmode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onclick':"javascript:yesnoCheck();"}), choices=CHOICES, initial='Time')
    startdate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    enddate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    turnsplayed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    
    def clean(self):
        sd = self.cleaned_data["startdate"]
        ed = self.cleaned_data["enddate"]
        if ed <= sd:
            raise ValidationError(_('End date must be after start date')) 


class TRMNpartForm(forms.Form):
        person = PlayerField()

class NonpartForm(forms.Form):
        firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        

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

#endregion       

        