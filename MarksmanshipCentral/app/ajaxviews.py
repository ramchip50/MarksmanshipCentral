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


def update_scoring(session_id:int,game_id:int):
	g = Game.active_objects.get(id=game_id)
	pl = SessionParticipants.active_objects.filter(session_id=session_id)
	for p in pl:
		update_total_credits(p.person_id,p.earned_credits,g)

def game_approve(request):
		g_id = request.GET['game_id']
		game = Game.active_objects.get(pk=g_id)
		game.verified = True
		game.save()
		sess=Session.active_objects.filter(game_id=g_id)
		update_scoring(sess.id,g_id)
		return no_coffee()

def game_replace(request):
	g_id_new = request.GET['new_game_id']
	g_id_old = request.GET['old_game_id']
	new_g=Game.active_objects.get(id=g_id_new)
	new_g.verified=True
	new_g.save()
	sess=Session.active_objects.filter(game_id=g_id_old)
	for s in sess:
		s.game_id=g_id_new
		update_scoring(s.id,g_id_new)
	old_g=Game.active_objects.get(id=g_id_old)
	old_g.delete()
	return no_coffee()

def game_edit(request):
			
	
 	return no_coffee()


