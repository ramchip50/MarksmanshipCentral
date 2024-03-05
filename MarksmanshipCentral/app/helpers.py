#Common Functions Go here. reference = from app.helpers import * 


import datetime
from django.db.models import Q, Value, QuerySet
from django.db.models.functions import Concat

from models.models import *
    
def player_select_list():
    return Person.objects.all().order_by("lastname","firstname").annotate(full_name = Concat('lastname',Value(', '),'firstname')).values_list("id","full_name")

def no_coffee():
    return "I'm a teapot"

class awardentry:
    def __init__(self,weapon_name,weapon_total,marksman,sharpshooter,expert,high_expert):
        self.weapon_name = weapon_name
        self.weapon_total = weapon_total
        self.marksman = marksman
        self.sharpshooter = sharpshooter
        self.expert = expert
        self.high_expert = high_expert


def award_list(personpk):
    awardgrid = list()
    weapons = Weapon.objects.filter(id__gt=0)
    for w in weapons:
        creds = TotalCredits.objects.filter(person_id = personpk, weapon_id = w.pk)
        if creds.count() > 0:
            for c in creds:
                thiscred = awardentry(w.name,c.weapontotal,c.marksman,c.sharpshooter,c.expert,c.high_expert)
                awardgrid.append(thiscred)
        else:
                thiscred = awardentry(w.name,0.00,None,None,None,None)
                awardgrid.append(thiscred)
        
    return awardgrid

def save_session(gamepk):
#check for duplicates
#get the game and date from incoming session
#find a session with the same game and date
#if not found, good to go
#if found, get checksum of personids from incoming 
    #compare to checksum of personids from save
    startdate = datetime.date(2024,3,1)
    saved = Session.objects.filter(game_id = gamepk,startdate__startswith = datetime.date(startdate.year,startdate.month,startdate.day))
    if saved.count() == 0:
        return 'no dup'
    else:
        return 'yes dup'
  

        
    