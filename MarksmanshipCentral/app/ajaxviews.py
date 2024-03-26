from datetime import datetime
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



