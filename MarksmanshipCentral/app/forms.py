"""
Definition of forms.
"""

import email
from os import name
from random import choice
from typing import Any
from django import forms
from django.db.models import QuerySet
from django.db.models.functions import Now 
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

class RegistrationForm(ModelForm):
    class Meta:
        model = Person
        fields = ('memberid', 'firstname', 'lastname', 'emailaddress', 'chapter', 'branch')
        widgets = {
            'memberid': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'firstname': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'lastname': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'emailaddress': forms.EmailInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'chapter': forms.Select(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'branch': forms.Select(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
            'passwrd': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}),
         }

class signinform(forms.Form):
    email_address = forms.EmailField(max_length=255,required=True,label='Email Address',widget=forms.EmailInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}))
    passwrd = forms.CharField(max_length=50, required=True,label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg mb-3 text-dark'}))    

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
    turnsplayed = forms.IntegerField(widget=forms.NumberInput(attrs={'style':'width:350px','class':'form-control'}),required=False)
    
    def clean(self):
        sd = datetime.strptime(self.cleaned_data["startdate"],"%Y-%m-%dT%H:%M")    #2024-04-05T10:56
        ed = datetime.strptime(self.cleaned_data["enddate"],"%Y-%m-%dT%H:%M")
        
        td = ed-sd
        if td.total_seconds() <= 0:
            raise ValidationError(_('End date must be after start date')) 

        if self.cleaned_data["playmode"] == 'Time':
            if td.total_seconds()/3600 >= 24:
                raise ValidationError(_('Time based session cannot be more than 24 hours'))
        else:
            if self.cleaned_data['turnsplayed'] == None:
                raise ValidationError(_('Enter the number of turns'))
            



class TRMNpartForm(forms.Form):
        person = PlayerField(label='Member Name')

class NonpartForm(forms.Form):
        fullname = forms.CharField(label='Player Name',widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}))

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('memberid', 'firstname', 'lastname', 'emailaddress', 'chapter', 'branch')
        widgets = {
            'memberid': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3'}),
            'firstname': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3'}),
            'lastname': forms.TextInput(attrs={'class':'form-control form-control-lg mb-3'}),
            'emailaddress': forms.EmailInput(attrs={'class':'form-control form-control-lg mb-3'}),
            'chapter': forms.Select(attrs={'class':'form-control form-control-lg mb-3'}),
            'branch': forms.Select(attrs={'class':'form-control form-control-lg mb-3'}),
            }
            

class GameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}))    
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width:350px'}),required=False)
    l = Weapon.objects.all().values_list("id","name")
    weapon = forms.ChoiceField(choices=l,widget=forms.Select(attrs={'class':'form-control','style':'width:350px'}))

    def clean(self):
        if self.cleaned_data["weapon"] == '0':
            raise ValidationError(_('You must select a weapon')) 
        if Game.active_objects.filter(name__iexact=self.cleaned_data["name"]):
            raise ValidationError(_('That title is already in the library')) 
        
class BaseReportSearch(forms.Form):
    startdate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'date', 'class':'form-control'}))
    enddate = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'date', 'class':'form-control'}))
    

    def clean(self) -> dict[str, Any]:
        sd = self.cleaned_data["startdate"]
        ed = self.cleaned_data["enddate"]
        if ed <= sd:
            raise ValidationError(_('End date must be after start date')) 
        return super().clean()

class ReportSearch_fleet(BaseReportSearch):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('chapters')
        super(ReportSearch_fleet,self).__init__(*args, **kwargs)
        self.fields["chapter"] = forms.ChoiceField(choices = choices, widget=forms.Select(attrs={'class':'form-control'}), required=False)
                            
class ReportSearch_staff(BaseReportSearch):
	ch = list(Chapter.active_objects.all().order_by('name').values_list('id','name'))
	ch.insert(0,('','-- All --'))
	chapter = forms.ChoiceField(choices=ch,widget=forms.Select(attrs={'class':'form-control'}), required=False)
	CH2= list(Fleet.objects.all().order_by('name').values_list('id','name'))
	CH2.insert(0,('','-- All --'))
	fleet = forms.ChoiceField(choices = CH2, widget=forms.Select(attrs={'class':'form-control','onchange':'fleet_change()'}), required=False)


#endregion       

        