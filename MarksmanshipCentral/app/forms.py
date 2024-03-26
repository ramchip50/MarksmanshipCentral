"""
Definition of forms.
"""

from os import name
from random import choice
from django import forms
from django.db.models import QuerySet 
from django.forms import ChoiceField, ModelForm
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from models.models import *
from app.formhelpers import *

#Fields
#region Fields

class GameField(forms.CharField):
    widget=forms.TextInput(attrs={'style':'width:350px','class':'basicAutoComplete formcontrol',
           'placeholder':'Type name to search','data-url':'/game_autocomplete/','autocomplete':'off'})

    def validate(self,value):
        try:
           Game.active_objects.get(name=value)
           return
        except:
            raise ValidationError(_('Game not in directory. Go to New Game page to add it'))

class PlayerField(forms.CharField):
    widget=forms.TextInput(attrs={'style':'width:350px','class':'basicAutoComplete formcontrol',
           'placeholder':'Type name to search','data-url':'/member_autocomplete/','autocomplete':'off'})
     
    def validate(self,value):
        try:
           names=value.split(',')
           p=Person.active_objects.get(lastname=names[0].strip(),firstname=names[1].strip())
           return
        except:
            raise ValidationError(_('Member not found in roster'))  

#endregion


#Forms
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
    startdate = forms.CharField(widget=forms.TextInput(attrs={'style':'width:350px', 'type': 'datetime-local', 'class':'form-control'}))
    enddate = forms.CharField(widget=forms.TextInput(attrs={'style':'width:350px', 'type': 'datetime-local', 'class':'form-control'}))
    turnsplayed = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    
    def clean(self):
        sd = self.cleaned_data["startdate"]
        ed = self.cleaned_data["enddate"]
        if ed <= sd:
            raise ValidationError(_('End date must be after start date')) 
   

class TRMNpartForm(forms.Form):
        person = PlayerField(label='Member Name')

class NonpartForm(forms.Form):
        fullname = forms.CharField(label='Player Name',widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}))

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('memberid', 'firstname', 'lastname', 'emailaddress', 'chapter', 'branch')

class GameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}))    
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}))
    l = Weapon.objects.all().values_list("id","name")
    weapon = forms.ChoiceField(choices=l,widget=forms.Select(attrs={'class':'form-control','style':'width:350px'}))

        
class ReportSearch(forms.Form):
    CH1=Chapter.objects.all()
    CH2=Fleet.objects.all()
    startdate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    enddate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'datetime-local', 'class':'form-control'}))
    chapter = forms.ModelChoiceField(queryset = CH1, widget=forms.Select(attrs={'class':'form-control'}))
    branch = forms.ModelChoiceField(queryset = CH2, widget=forms.Select(attrs={'class':'form-control'}))


#endregion       

        