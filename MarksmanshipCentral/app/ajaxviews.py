import json
from http import HTTPStatus
from datetime import datetime
from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from app.datasvcs import *
from app.forms import *
from django.forms.models import modelformset_factory, formset_factory
from app.helpers import *
from models.models import *
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.contrib import messages

class HttpResponseAccepted(HttpResponse):
	status_code=HTTPStatus.ACCEPTED

class HttpReponseNoCoffee(HttpResponse):
	status_code=HTTPStatus.IM_A_TEAPOT
	

def game_autocomplete(request):
	if request.GET.get('q'):
		q = request.GET['q']
		data = Game.active_objects.filter(Q(name__icontains=q) | Q(alias__icontains=q)).order_by("name").values_list('name',flat=True)
		json = list(data)
		return JsonResponse(json, safe=False)

def librarysearch_autocomplete(request):
	if request.GET.get('q'):
		q = request.GET['q']
		data = Game.active_objects.filter(Q(name__icontains=q) | Q(alias__icontains=q)).order_by("name").annotate(lib_entry = Concat('name',Value(' ('),'alias',Value(')'))).values_list('lib_entry',flat=True)
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
		update_total_credits(p.person_id,p.credits,g)
	return HttpResponseAccepted()

def game_approve(request):
		g_id = request.GET['game_id']
		game = Game.active_objects.get(pk=g_id)
		game.verified = True
		game.save()
		sess=Session.active_objects.filter(game_id=g_id)
		for s in sess:
			update_scoring(s.id,g_id)
		return HttpResponseAccepted()

def game_delete(request):    #Don't call this if there are sessions referencing
		g_id = request.GET['game_id']
		game = Game.active_objects.get(pk=g_id)
		game.active=False
		game.save()
		return HttpResponseAccepted()

def game_replace(request):
	g_new_libraryname = request.GET['new_name']
	n = g_new_libraryname.split('(')
	g_new=n[0].strip()
	g_old_id = request.GET['old_id']
	add_alias = request.GET['add_alias']
	new_g=Game.active_objects.get(name=g_new)
	new_g.verified=True
	if add_alias == 'true':
		g_old=Game.active_objects.get(pk=g_old_id)
		new_g.alias = new_g.alias+','+g_old.name+','+g_old.alias
	new_g.save()
	sess=Session.active_objects.filter(game_id=g_old_id)
	for s in sess:
		s.game_id=new_g.pk
		s.save()
		update_scoring(s.id,new_g.pk)
	g_old=Game.active_objects.get(pk=g_old_id)
	g_old.delete()
	return HttpResponseAccepted()


def game_save(request):
	g_id = request.GET['game_id']
	g_name = request.GET['game_name']
	alias = request.GET['alias']
	weapon_id = request.GET['weapon_id']
	game=Game.active_objects.get(pk=g_id)
	game.verified=True
	game.name = g_name
	game.alias=alias
	weap=Weapon.objects.get(pk=weapon_id)
	game.weapon=weap
	game.save()
	sess=Session.active_objects.filter(game_id=g_id)
	for s in sess:
		update_scoring(s.id,g_id)
	return HttpResponseAccepted()


def session_resolve(request):
	session_id = request.GET['session_id']
	approved = request.GET['approved']
	sess = Session.active_objects.get(pk=session_id)
	players = SessionParticipants.active_objects.filter(session_id=session_id)
	sess.dupsessid = None
	if approved == 'true':
		for p in players:
			update_total_credits(p.person_id,p.credits,sess.game)
	else:
		for p in players:
			p.active=False
			p.save()
		sess.active=False
	sess.save()
	return HttpResponseAccepted()

		
def fleet_chapters(request):
	fleet_id = request.GET['fleet_id']
	if fleet_id != '':
		ch = Chapter.active_objects.filter(fleet_id=fleet_id).order_by('name').values('id','name')
	else:
		ch = Chapter.active_objects.all().order_by('name').values('id','name')
	json_ch = json.dumps(list(ch), cls=DjangoJSONEncoder)
	return JsonResponse(json_ch,safe=False)



