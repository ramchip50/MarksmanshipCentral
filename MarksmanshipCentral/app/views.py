"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from app.forms import signinform
#from app.helpers import has_role
from models.models import Game, Person, Session
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
    context = {"person": person}
    if person.branch.name == 'RMA':
        template = 'app/HomeArmy.html'
    else:
        template = 'app/HomeNavy.html'
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
    context = {"person": person}
    return render(request, 'app/Personal.html',context)    

def newgame(request):
    return render(request, 'app/NewGame.html')

def newsession(request):
    return render(request, 'app/NewSession2.html')
    
def reports(request):
    return render(request, 'app/Reports.html')

def oversight(request):
    return render(request, 'app/Oversight.html')


