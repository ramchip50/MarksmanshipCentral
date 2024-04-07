"""
Definition of views.
"""

from ast import Name
from datetime import datetime
from http.client import CONFLICT
from json import JSONEncoder
import json
from pickle import NONE
from tabnanny import check
from types import NoneType
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

class sessiondisplay():
	def __init__(self,id,startdate,enddate,playmode,turnsplayed):
		self.id=id
		self.startdate=startdate
		self.enddate=enddate
		self.playmode=playmode
		self.turnsplayed=turnsplayed
	players = None
	
def test(request):
	st=datetime(2024,3,1)
	et=datetime(2024,3,31)
	# chap = Chapter.active_objects.get(id=66)
	# flt = Fleet.active_objects.get(id=2)
	# sessions=get_allsessioncredits_bydate_andchapter(st,et,chap)
	# #sessions=get_allsessioncredits_bydate_andfleet(st,et,flt)
	#history= get_session_history_bydate(st,et,7012)
	
	#plyrs = history[4].players
	#plyrs.append(history[4].players.split(','))
	#u  history[4].players.toJson()
	#u='{"lastname": "Admin", "firstname": "Test"},{"lastname": "Blue", "firstname": "Chaco"},{"lastname": "Greene", "firstname": "Kevin"}'
	#l = dict(u)
	#uj = json.loads(u)
#	p = history[4].players.split(,[')
#	for o in u:
	if request.method == "POST":
		whutnot = request.POST.__getitem__('chapter')
	else:
		whutnot = None
	context = {"coffee":no_coffee(), "whut":whutnot}
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
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	if request.method == "POST":
		form = GameForm(request.POST)
		if form.is_valid():
			g = Game()
			g.name=form.cleaned_data["name"]
			if form.cleaned_data["alias"] == '':
				g.alias = g.name
			else:
				g.alias=form.cleaned_data["alias"]
			g.weapon = Weapon.objects.get(pk=form.cleaned_data["weapon"])
			g.save()
			submitted = True     
			form=GameForm 
		else:
			submitted=False
	else: 
		submitted = False
		form = GameForm

	context = {
		'person': person,
		'form':form,
	    'submitted':submitted
		}
		
		
	return render(request, "app/NewGame.html", context)

def newsession(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
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
	
	context = {
		'person':person,
		'form':form,
		'formset1':formset1,
	    'formset2':formset2,
	    'submitted':submitted,
		'message':message
		}
		
	return render(request, 'app/NewSession2.html', context)

def oversight(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	submittedgames = Game.active_objects.filter(verified = False)
	newgames=list()
	for sg in submittedgames:
		if Session.active_objects.filter(game_id=sg.pk).exists():
			newgames.append({'game_id':sg.pk,'name':sg.name,'alias':sg.alias,'weapon':sg.weapon,'createdon':sg.createdon,'has_session':True})
		else:
			newgames.append({'game_id':sg.pk,'name':sg.name,'alias':sg.alias,'weapon':sg.weapon,'createdon':sg.createdon,'has_session':False})
		
	submittedsessions = Session.active_objects.order_by('startdate').filter(dupsessid__gt=0)
	participants = list()
	nonTRMN = list()
	linkedsessions=[]
	for s in submittedsessions:
		linkedsessions.append(Session.active_objects.get(pk=s.dupsessid).pk)
		for sp in SessionParticipants.active_objects.filter(session=s.id).values_list("session_id","person"):
			p=Person.active_objects.get(pk=sp[1])
			participants.append({'session_id': sp[0],'name': p.lastname +', '+p.firstname})

		for n in NonTRMNParticipants.active_objects.filter(session=s.id).values_list("session_id","fullname"):
			nonTRMN.append({'session_id': n[0],'name': n[1]})

	conflictsessions = Session.active_objects.filter(pk__in=linkedsessions)
	for c in conflictsessions:
			for sp in SessionParticipants.active_objects.filter(session=c.id).values_list("session_id","person"):
				p=Person.active_objects.get(pk=sp[1])
				participants.append({'session_id': sp[0],'name': p.lastname +', '+p.firstname})

	context={
		'person':person,
		'games': newgames,
		'submittedsessions':submittedsessions,
		'conflictsessions' :conflictsessions,
		'nonTRMN' : nonTRMN,
		'participants':participants
		}
	return render(request, 'app/Oversight.html', context)
#endregion

#Reports
#region Reports
def reports(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)

	return render(request, 'app/Reports.html', {'person':person})

def member_reports(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	form=BaseReportSearch()
	history = None
	startdate=None
	enddate=None 
	if request.method == 'POST':
		form=BaseReportSearch(request.POST or None)
		if form.is_valid():
			startdate = datetime.strptime(form.cleaned_data['startdate'],"%Y-%m-%d")    #2024-04-04
			enddate = datetime.strptime(form.cleaned_data['enddate'],"%Y-%m-%d") 
			history = get_session_history_bydate(startdate,enddate,personpk)
		else:
			form=BaseReportSearch()
	context = {
		"startdate":startdate,
		"enddate":enddate,
		"person":person,
		"form":form,
		"history":history}

	return render(request, 'app/MemberReport.html',context)

def credit_reports(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	submitted = False
	startdate = None
	enddate = None
	credits = None
	if person.role_id < 3:
		form = BaseReportSearch()
	elif person.role_id == 3 :
		ch = list(Chapter.active_objects.filter(fleet_id=person.chapter.fleet_id).order_by('name').values_list('id','name'))
		ch.insert(0,('','-- All --'))
		form = ReportSearch_fleet(chapters=ch)
	else:
		form = ReportSearch_staff()
	if request.method == 'POST':
		if person.role_id < 3:
			form = BaseReportSearch(request.POST or None)
		elif person.role_id == 3 :
			form = ReportSearch_fleet(request.POST or None,chapters=ch)
		else:
			form = ReportSearch_staff(request.POST or None)
		if form.is_valid():
			startdate = datetime.strptime(form.cleaned_data['startdate'],"%Y-%m-%d")    #2024-04-04
			enddate = datetime.strptime(form.cleaned_data['enddate'],"%Y-%m-%d")
			if person.role_id == 2:
				credits = get_allsessioncredits_bydate_andchapter(startdate, enddate, person.chapter_id)
			elif person.role_id == 3:
				if form.cleaned_data["chapter"] == '':
					credits = get_allsessioncredits_bydate_andfleet(startdate,enddate,person.chapter.fleet_id)
				else:
					credits = get_allsessioncredits_bydate_andchapter(startdate, enddate, int(form.cleaned_data["chapter"]))
			else:
				if form.cleaned_data["fleet"]=='' and form.cleaned_data["chapter"] =='':
					credits = get_allsessioncredits_bydate(startdate,enddate)
				elif form.cleaned_data["fleet"] != '' and form.cleaned_data["chapter"] == '':
					credits = get_allsessioncredits_bydate_andfleet(startdate, enddate, int(form.cleaned_data["fleet"]))
				else:
					credits = get_allsessioncredits_bydate_andchapter(startdate, enddate, int(form.cleaned_data["chapter"]))
					
			


	context={
		'startdate':startdate,
		'enddate':enddate,
		'credits':credits,
		'person': person,
		'form': form
		}
		 
	return render(request, 'app/CreditReport.html', context)

def award_reports(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	submitted = False
	startdate = None
	enddate = None
	awards= None
	if person.role_id < 3:
		form = BaseReportSearch()
	elif person.role_id == 3 :
		ch = list(Chapter.active_objects.filter(fleet_id=person.chapter.fleet_id).order_by('name').values_list('id','name'))
		ch.insert(0,('','-- All --'))
		form = ReportSearch_fleet(chapters=ch)
	else:
		form = ReportSearch_staff()
	if request.method == 'POST':
		if person.role_id < 3:
			form = BaseReportSearch(request.POST or None)
		elif person.role_id == 3 :
			form = ReportSearch_fleet(request.POST or None,chapters=ch)
		else:
			form = ReportSearch_staff(request.POST or None)
		if form.is_valid():
			startdate = datetime.strptime(form.cleaned_data['startdate'],"%Y-%m-%d")    #2024-04-04
			enddate = datetime.strptime(form.cleaned_data['enddate'],"%Y-%m-%d")
			if person.role_id == 2:
				awards = get_earned_awards_bydate_andchapter(startdate, enddate, person.chapter_id)
			elif person.role_id == 3:
				if form.cleaned_data["chapter"] == '':
					awards = get_earned_awards_bydate_andfleet(startdate,enddate,person.chapter.fleet_id)
				else:
					awards = get_earned_awards_bydate_andchapter(startdate, enddate, int(form.cleaned_data["chapter"]))
			else:
				if form.cleaned_data["fleet"]=='' and form.cleaned_data["chapter"] =='':
					awards = get_earned_awards_bydate(startdate,enddate)
				elif form.cleaned_data["fleet"] != '' and form.cleaned_data["chapter"] == '':
					awards = get_earned_awards_bydate_andfleet(startdate, enddate, int(form.cleaned_data["fleet"]))
				else:
					awards = get_earned_awards_bydate_andchapter(startdate, enddate, int(form.cleaned_data["chapter"]))
					
			


	context={
		'startdate':startdate,
		'enddate':enddate,
		'awards':awards,
		'person': person,
		'form': form
		}

	return render(request, 'app/AwardReport.html', context)


#endregion




