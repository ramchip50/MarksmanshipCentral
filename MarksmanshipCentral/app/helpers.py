#Common Functions Go here. reference = from app.helpers import * 


from datetime import datetime
from decimal import *
from django.forms import BaseModelFormSet
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from app.forms import SessionForm, TRMNpartForm, NonpartForm
from models.models import *



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
        creds = TotalCredits.active_objects.filter(person_id = personpk, weapon_id = w.pk)
        if creds.count() > 0:
            for c in creds:
                thiscred = awardentry(w.name,c.weapontotal,c.marksman,c.sharpshooter,c.expert,c.high_expert)
                awardgrid.append(thiscred)
        else:
                thiscred = awardentry(w.name,0.00,None,None,None,None)
                awardgrid.append(thiscred)
        
    return awardgrid

def check_session_and_save(personpk,sessionform:SessionForm,trmn_participants:BaseModelFormSet,nontrmn:BaseModelFormSet):
#check for duplicates
    #map the incoming form to a session object that we can save later.
    newsession = Session()
    newsession.fill(sessionform.cleaned_data["game"],sessionform.cleaned_data["startdate"],sessionform.cleaned_data["enddate"],sessionform.cleaned_data["playmode"],turnsplayed=sessionform.cleaned_data["turnsplayed"])
    #get the game and date
    date_format = '%Y-%m-%dT%H:%M'
    session_startdate = datetime.strptime(newsession.startdate,date_format)
    #find a session with the same game and date
    saved = Session.active_objects.filter(game = newsession.game,startdate__startswith = session_startdate.date()).first()
    if saved != None:
        csum = personpk
        for t in trmn_participants:
            if t.cleaned_data : csum += t.cleaned_data["person"].pk
        #compare to checksum of personids from save
        saved_trmnpart = SessionParticipants.active_objects.filter(session_id=saved.pk)
        csum1=0
        for s in saved_trmnpart:
            csum1 += s.person_id
        if csum == csum1:
            return 'Duplicate Session Detected'
        else:
            newsession.flagged=True
    #Calculate Credits
    if newsession.playmode == 'Time':
        enddate = datetime.strptime(newsession.enddate,date_format)
        diff = enddate - session_startdate
        minutes=diff.total_seconds()/60
        basecredits = minutes/60
    else:
        basecredits = newsession.turnsplayed*.25
    #Multipier
    mult = len(trmn_participants)
    earned_credits = Decimal(basecredits*mult)
    newsession.save()
       
    #save this person as a participant?
    thisplayer = SessionParticipants()
    thisplayer.person = Person.active_objects.get(pk=personpk)
    thisplayer.session = newsession
    thisplayer.minutes = minutes
    thisplayer.credits = earned_credits
    thisplayer.save()
    if newsession.flagged != True:
        update_total_credits(personpk, earned_credits, newsession.game)
    
    #save the rest of the players
    for t in trmn_participants:
        nextplayer= SessionParticipants()
        nextplayer.person = Person.active_objects.get(pk=t.cleaned_data["playername"])
        nextplayer.session = newsession
        nextplayer.minutes = minutes
        nextplayer.credits = earned_credits
        if newsession.flagged != True:
            update_total_credits(nextplayer.person.pk, earned_credits, newsession.game)
        nextplayer.save()

    for n in nontrmn:
        if(n.cleaned_data):
            non=NonTRMNParticipants()
            non.firstname=n.cleaned_data["firstname"]
            non.lastname=n.cleaned_data["lastname"]
            non.session = newsession
            non.save()

    return 'Session Saved'

def update_total_credits(personpk, earned_credits, game:Game):
    person = get_object_or_404(Person,pk=personpk)
    if person.branch.name=='RMA':
        tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = game.weapon.pk)
    else:
        if game.weapon.pk < 6:
            tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = 1)
        else:
            tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = 6)
    tc.weapontotal += earned_credits
    if (tc.weapontotal>=5 and tc.weapontotal < 100) and tc.marksman == None:
        tc.marksman = datetime.today()
    if (tc.weapontotal>=100 and tc.weapontotal < 200) and tc.sharpshooter == None:
        tc.sharpshooter = datetime.today()
    if (tc.weapontotal>=200 and tc.weapontotal < 600) and tc.expert == None:
        tc.expert = datetime.today()
    if (tc.weapontotal>=600) and tc.high_expert == None:
        tc.high_expert = datetime.today()
    tc.save()
            
    


        
        
        



        
        


    