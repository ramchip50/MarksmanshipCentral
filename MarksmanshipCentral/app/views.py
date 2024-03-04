"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from app.forms import *
from django.forms.models import modelformset_factory
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
    context = {"person": person, "form":form }
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
	submitted = False
	if request.method == 'POST':
		form = SessionForm(request.POST or None)
		TRMNSessionformset = modelformset_factory(SessionParticipants, form=TRMNpartForm, extra = 10, max_num=10)
		NonSessionformset = modelformset_factory(NonTRMNParticipants, form=NonpartForm, extra = 3, max_num=3)
		formset1 = TRMNSessionformset(request.POST or None) 
		formset2 = NonSessionformset(request.POST or None) 
		if all([form.is_valid(), formset1.is_valid(), formset2.is_valid()]):
			parent = form.save()
			parent.save()
			for form in formset1:
				child1 = formset1.save()
				child1.session = parent.pk
				child1.save()
			for form in formset2:
				child2=formset2.save()
				child2.session = parent.pk
				child2.save()
			return HttpResponseRedirect('app/NewSession2?submitted=True')
	else:
		form = SessionForm()
		TRMNSessionformset = modelformset_factory(SessionParticipants, form=TRMNpartForm, extra = 10, max_num=10)
		NonSessionformset = modelformset_factory(NonTRMNParticipants, form=NonpartForm, extra = 3, max_num=3)
		formset1 = TRMNSessionformset() 
		formset2 = NonSessionformset() 
		if "submitted" in request.GET:
			Submitted = True
	
	return render(request, 'app/NewSession2.html', {'form':form,'formset1':formset1, 'formset2':formset2, 'submitted':submitted})



    
def reports(request):
    return render(request, 'app/Reports.html')

def oversight(request):
    return render(request, 'app/Oversight.html')


