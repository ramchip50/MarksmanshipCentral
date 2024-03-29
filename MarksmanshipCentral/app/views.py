"""
Definition of views.
"""

from datetime import datetime
from pickle import NONE
from tabnanny import check
from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from app.datasvcs import *
from app.forms import *
from django.forms.models import modelformset_factory, formset_factory
from app.helpers import *
from models.models import *
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
#Site
#region Site
def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	personid = request.session.get('personid',default=None)
	if personid != None:
		return HttpResponseRedirect('landing/')
	else:
		return HttpResponseRedirect('login/')

def contact(request):
	"""Renders the contact page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/contact.html',
		{
			'title':'Contact',
			'message':'Your contact page.',
			'year':datetime.now().year,
		}
	)

def about(request):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/about.html',
		{
			'title':'About',
			'message':'Your application description page.',
			'year':datetime.now().year,
		}
	)

def test(request):
	# st=datetime(2024,2,1)
	# et=datetime(2024,4,1)
	# chap = Chapter.active_objects.get(id=66)
	# flt = Fleet.active_objects.get(id=2)
	# sessions=get_allsessioncredits_bydate_andchapter(st,et,chap)
	# #sessions=get_allsessioncredits_bydate_andfleet(st,et,flt)
	games = Game.active_objects.filter(verified = False)
	sessions = Session.active_objects.order_by('startdate').filter(dupsessid__gt=0)
	participants = list()
	for s in sessions:
		for sp in SessionParticipants.active_objects.filter(session=s.id).values_list("session_id","person"):
			p=Person.active_objects.get(pk=sp[1])
			participants.append({'session_id': sp[0],'name': p.lastname +', '+p.firstname})
	nonTRMN = list()
	for s in sessions:
		for n in NonTRMNParticipants.active_objects.filter(session=s.id).values_list("session_id","fullname"):
			nonTRMN.append({'session_id': n[0],'name': n[1]})

#	return render(request, 'app/Oversight.html', {'games':games,'sessions':sessions,'nonTRMN':nonTRMN,'participants':participants})



	context = {"coffee":no_coffee(),"games":games}
	return render(request,'app/TestPage.html',context)
#endregion

#Admin
#region Admin
def landing(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	credits = award_list(personpk)
	if person.branch.name == 'RMA':
		template = 'app/HomeArmy.html'
	else:
		template = 'app/HomeNavy.html'
	context = {"person": person,"credits":credits}
	return render(request, template, context)
						
def login(request):
	if request.method == 'POST':
		form = signinform(request.POST)
		if form.is_valid():
			person_email = form.cleaned_data
			person = get_object_or_404(Person,emailaddress=person_email)
			request.session["personid"] = person.pk
			#newbranch=Branch.active_objects.get(id=6)
			#transfer_branch(person,newbranch)
			return HttpResponseRedirect('/landing/')
	else:
		form = signinform
		
	context = {
		'form':form
	}
			
	return render(request,'app/TRMNlogin.html',context)

def logout(request):
	request.session.flush()
	return render(request,'app/TRMNlogout.html')    

def personal(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	submitted = False
	form = PersonForm(request.POST or None, instance=person)
	if form.is_valid():
		form.save()
		return redirect('app/personal')
	
	context = {"person": person, "form":form}
	return render(request, 'app/Personal.html',context)    
#endregion

#DataEntry
#region DataEntry
def newgame(request):
	if request.method == "POST":
		form = GameForm(request.POST)
		if form.is_valid():
			g = Game()
			g.name=form.cleaned_data["name"]
			g.alias=form.cleaned_data["alias"]
			g.weapon = Weapon.objects.get(pk=form.cleaned_data["weapon"])
			g.save()
			submitted = True     
			form=GameForm      
	else: 
		submitted = False
		form = GameForm

	return render(request, "app/NewGame.html", {'form':form, 'submitted':submitted})

def newsession(request):
	personpk = request.session["personid"]  
	submitted = False
	if request.method == 'POST':
		form = SessionForm(request.POST or None)
		TRMNSessionformset = formset_factory(TRMNpartForm, extra = 6, max_num=6)
		NonSessionformset = formset_factory(NonpartForm, extra = 2, max_num=2)
		formset1 = TRMNSessionformset(request.POST or None) 
		formset2 = NonSessionformset(request.POST or None) 
		if all([form.is_valid(), formset1.is_valid(), formset2.is_valid()]):
			result=check_session_and_save(personpk,form,formset1,formset2)
			formset1 = TRMNSessionformset()        
			formset2 = NonSessionformset()
			form = SessionForm()
			if result =="NOT_ELIGIBLE":  
				message = "Must have one other TRMN player or two non-TRMN players"
			elif result=="DUP_SESSION":
				message = "Duplicate Session"
			elif result=="SAVED":
				message = "Session Saved"
			else:
				message = no_coffee()  

			#HttpResponseRedirect('/landing/')
		else:
			message = "Misfire. Session Not Saved"
	else:
		message = ''
		form = SessionForm()
		TRMNSessionformset = formset_factory(TRMNpartForm, extra = 6, max_num=6)
		NonSessionformset = formset_factory(NonpartForm, extra = 2, max_num=2)
		formset1 = TRMNSessionformset() 
		formset2 = NonSessionformset() 
		if "submitted" in request.GET:
			Submitted = True
	
	return render(request, 'app/NewSession2.html', {'form':form,'formset1':formset1, 'formset2':formset2, 'submitted':submitted,'message':message})

def oversight(request):
	games = Game.active_objects.filter(verified = False)
	sessions = Session.active_objects.order_by('startdate').filter(dupsessid__gt=0)
	participants = list()
	for s in sessions:
		for sp in SessionParticipants.active_objects.filter(session=s.id).values_list("session_id","person"):
			p=Person.active_objects.get(pk=sp[1])
			participants.append({'session_id': sp[0],'name': p.lastname +', '+p.firstname})
	nonTRMN = list()
	for s in sessions:
		for n in NonTRMNParticipants.active_objects.filter(session=s.id).values_list("session_id","fullname"):
			nonTRMN.append({'session_id': n[0],'name': n[1]})

	return render(request, 'app/Oversight.html', {'games':games,'sessions':sessions,'nonTRMN':nonTRMN,'participants':participants})
#endregion

#Reports
#region Reports
def reports(request):
	return render(request, 'app/Reports.html')

def member_reports(request):
	return render(request, 'app/MemberReport.html')

def credit_reports(request):
    personpk = request.session["personid"]
    person = get_object_or_404(Person,pk=personpk)
    submitted = False
    personal = PersonForm(request.POST or None, instance=person)
    if person.role == 1:
        form = ReportSearch_user()
    elif person.role == 2:
        form = ReportSearch_chapter()
    else :
        form = ReportSearch_fleet()
    if request.method == 'POST':
        pass
         
    return render(request, 'app/CreditReport.html', {'form':form, 'personal':personal})

def award_reports(request):
    personpk = request.session["personid"]
    person = get_object_or_404(Person,pk=personpk)
    submitted = False
    personal = PersonForm(request.POST or None, instance=person)
    if person.role == 1:
        form = ReportSearch_user()
    elif person.role == 2:
        form = ReportSearch_chapter()
    else :
        form = ReportSearch_fleet()
    if request.method == 'POST':
        pass
         
    return render(request, 'app/AwardReport.html', {'form':form, 'personal':personal})


#endregion




