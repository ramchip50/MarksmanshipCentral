"""
Definition of views.
"""

from datetime import datetime
from tabnanny import check
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from app.datasvcs import *
from app.forms import *
from django.forms.models import modelformset_factory, formset_factory
from app.helpers import *
from models.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


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
	submitted = False
	if request.method == "POST":
		form = GameForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/NewGame?submitted=True')
	else: 
		form = GameForm
		if 'submitted' in request.GET:
			submitted = True 
		return render(request, "app/NewGame.html", {'form':form, 'submitted':submitted})

def newsession(request):
	personpk = request.session["personid"]  
	submitted = False
	if request.method == 'POST':
		form = SessionForm(request.POST or None)
		TRMNSessionformset = formset_factory(TRMNpartForm, extra = 4, max_num=4)
		NonSessionformset = formset_factory(NonpartForm, extra = 2, max_num=2)
		formset1 = TRMNSessionformset(request.POST or None) 
		formset2 = NonSessionformset(request.POST or None) 
		if all([form.is_valid(), formset1.is_valid(), formset2.is_valid()]):
			check_session_and_save(personpk,form,formset1,formset2)

	else:
		form = SessionForm()
		TRMNSessionformset = formset_factory(TRMNpartForm, extra = 4, max_num=4)
		NonSessionformset = formset_factory(NonpartForm, extra = 2, max_num=2)
		formset1 = TRMNSessionformset() 
		formset2 = NonSessionformset() 
		if "submitted" in request.GET:
			Submitted = True
	
	return render(request, 'app/NewSession2.html', {'form':form,'formset1':formset1, 'formset2':formset2, 'submitted':submitted})



    
def reports(request):
    return render(request, 'app/Reports.html')

def oversight(request):
    return render(request, 'app/Oversight.html')


