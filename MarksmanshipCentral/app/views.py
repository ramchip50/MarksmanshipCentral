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
	st=datetime(2024,2,1)
	et=datetime(2024,4,1)
	chap = Chapter.active_objects.get(id=66)
	flt = Fleet.active_objects.get(id=2)
	sessions=get_allsessioncredits_bydate_andchapter(st,et,chap)
	#sessions=get_allsessioncredits_bydate_andfleet(st,et,flt)
	context = {"coffee":no_coffee(),"sessions":sessions}
	return render(request,'app/TestPage.html',context)

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

def game_autocomplete(request):
	if request.GET.get('q'):
		q = request.GET['q']
		data = Game.active_objects.filter(Q(name__icontains=q) | Q(alias__icontains=q)).values_list('name',flat=True)
		json = list(data)
		return JsonResponse(json, safe=False)

def member_autocomplete(request):
	if request.GET.get('q'):
		q = request.GET['q']
		data = Person.active_objects.filter(Q(lastname__icontains=q) | Q(firstname__icontains=q)).order_by("lastname","firstname").annotate(full_name = Concat('lastname',Value(', '),'firstname')).values_list("full_name")
		json = list(data)
		return JsonResponse(json, safe=False)

def reports(request):
	return render(request, 'app/Reports.html')

def member_reports(request):
	return render(request, 'app/MemberActivity.html')

def credit_reports(request):
	personpk = request.session["personid"]
	person = get_object_or_404(Person,pk=personpk)
	submitted = False
	personal = PersonForm(request.POST or None, instance=person)
	form = ReportSearch()
	if request.method == 'POST':
		form=PersonForm()
		 
	return render(request, 'app/CreditActivity.html', {'form':form, 'personal':personal})

def award_reports(request):
	return render(request, 'app/AwardActivity.html')

def oversight(request):
	games = Game.active_objects.filter(verified = False)
	
	sessions = Session.active_objects.order_by('startdate').filter(dupsessid__gt=0)
	participants = []
	for s in sessions:
		for sp in SessionParticipants.active_objects.filter(session=s.id).values_list("session_id","person"):
			participants.append(sp)
		
		
	nonTRMN = []
	for s in sessions:
		for n in NonTRMNParticipants.active_objects.filter(session=s.id).values_list("session_id","fullname"):
			nonTRMN.append(n)
			
	if request.method == 'POST':
		if request.POST.get('one'):
			id_list1 = request.POST.getlist('boxes')
			for x in id_list1:
				Game.active_objects.filter(pk=int(x)).update(verified = True)
				messages.success(request, ("Records Approved!"))
				return HttpResponseRedirect('app/oversight.html')
			
		elif request.POST.get('two'):
			id_list2 = request.POST.getlist('dups')
			sessions.update(flagged=False)
			
			for x in id_list2:
				Session.objects.filter(pk=int(x)).update(active=0) 
				messages.success(request, ("Records Deleted!"))
				for SessionParticipant in participants:
					update_total_credits(participants.person, participants.credits, participants.session.name)
			
			return HttpResponseRedirect('app/oversight.html')
	

	return render(request, 'app/Oversight.html', {'games':games,'sessions':sessions,'nonTRMN':nonTRMN,'participants':participants})




