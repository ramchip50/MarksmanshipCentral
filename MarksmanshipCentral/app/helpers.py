#Common Functions Go here. reference = from app.helpers import * 


import datetime
from django.forms import BaseModelFormSet
from django.db.models import Value
from django.db.models.functions import Concat
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

def check_session_and_save(personpk,session:SessionForm,trmn_participants:BaseModelFormSet,nontrmn:BaseModelFormSet):
#check for duplicates
    #get the game and date from incoming session
    game = session.game
    startdate = session.startdate
    #find a session with the same game and date
    saved = Session.active_objects.filter(game = game,startdate__startswith = datetime.date(startdate.year,startdate.month,startdate.day))
    if saved.count() > 0:
        csum = personpk
        for t in trmn_participants:
            csum += t.person_id
        #compare to checksum of personids from save
        saved_trmnpart = SessionParticipants.active_objects.filter(Session == saved)
        csum1=0
        for s in saved_trmnpart:
            csum1 += s.person_id
            
        if csum == csum1:
            return 'Duplicate Session Detected'
        else:
            session.flagged=True
    session.save()
    #Calculate Credits
    if session.playmode == 1:
        diff = session.enddate - session.startdate
        minutes=diff.total_seconds()/60
        basecredits = minutes/60
    else:
        basecredits = session.turnsplayed*.25
    #Multipier
    mult = len(trmn_participants)
    earned_credits = basecredits*mult
       
    #save this person as a participant
    thisplayer = SessionParticipants()
    thisplayer.session = session
    thisplayer.minutes = minutes
    thisplayer.credits = earned_credits
    thisplayer.save()
    update_total_credits(personpk, earned_credits, session.game)


    #save the rest of the players
    return 'Session Saved'



def update_total_credits(personpk, earned_credits, game:Game):
    person = Person.objects.get(id==personpk)
    if person.branch.name=='RMA':
        tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = game.weapon.pk)
    else:
        if game.weapon.pk < 6:
            tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = 1)
        else:
            tc, created = TotalCredits.objects.get_or_create(person_id = personpk, weapon_id = 6)
    tc.weapontotal += earned_credits
    if (tc.weapontotal>=5 and tc.weapontotal < 100) and tc.marksman == None:
        tc.marksman = datetime.datetime.today()
    if (tc.weapontotal>=100 and tc.weapontotal < 200) and tc.sharpshooter == None:
        tc.sharpshooter = datetime.datetime.today()
    if (tc.weapontotal>=200 and tc.weapontotal < 600) and tc.expert == None:
        tc.expert = datetime.datetime.today()
    if (tc.weapontotal>=600) and tc.high_expert == None:
        tc.high_expert = datetime.datetime.today()
    
            
    
 
        
        
        



        
        


    