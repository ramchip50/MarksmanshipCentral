#Common Functions Go here. reference = from app.helpers import * 


from datetime import datetime
from decimal import *
from unicodedata import name
from django.forms import BaseFormSet
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from app.forms import SessionForm, TRMNpartForm, NonpartForm
from models.models import *



def no_coffee():
    return "I'm a teapot"

#Award Functions
#region

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
    weapons = Weapon.objects.all()
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

#endregion

#Session Functions
# region



def check_session_and_save(personpk,sessionform:SessionForm,trmn_participants:BaseFormSet,nontrmn:BaseFormSet):
    #check for eligibility.
    has_one_trmn = trmn_participants[0].has_changed()
    has_two_nontrmn = nontrmn[0].has_changed() and nontrmn[1].has_changed()
    if has_one_trmn == False:
        if has_two_nontrmn == False:
              return "NOT_ELIGIBLE"
    
    #check for duplicates
    #map the incoming form to a session object that we can save later.
    newsession = Session()
    game = Game.active_objects.get(name=sessionform.cleaned_data["game"])
    newsession.fill(game,sessionform.cleaned_data["startdate"],sessionform.cleaned_data["enddate"],sessionform.cleaned_data["playmode"],turnsplayed=sessionform.cleaned_data["turnsplayed"])
    #get the game and date
    date_format = '%Y-%m-%dT%H:%M'
    session_startdate = datetime.strptime(newsession.startdate,date_format)
    #find a session with the same game and date
    saved = Session.active_objects.filter(game = newsession.game,startdate__startswith = session_startdate.date()).first()
    if saved != None:
        #saved_enddate = datetime.strptime(saved.enddate,date_format)
        csum = personpk
        for t in trmn_participants:
            if t.has_changed() :
                names=t.cleaned_data["person"].split(',')
                p=Person.active_objects.get(lastname=names[0].strip(),firstname=names[1].strip())
                csum += p.pk  
        #compare to checksum of personids from save
        saved_trmnpart = SessionParticipants.active_objects.filter(session_id=saved.pk)
        csum1=0
        for s in saved_trmnpart:
            csum1 += s.person_id
        if csum == csum1 and session_startdate < saved.enddate:
            return 'DUP_SESSION'
        else:
            newsession.dupsessid=saved.pk
    #Calculate Credits
    if newsession.playmode == 'Time':
        enddate = datetime.strptime(newsession.enddate,date_format)
        diff = enddate - session_startdate
        minutes=diff.total_seconds()/60
        basecredits = Decimal(minutes/60)
    else:
        minutes=0
        basecredits = Decimal(newsession.turnsplayed)*Decimal(.25)
    #Multipier
    mult = len(trmn_participants)
    earned_credits = Decimal(basecredits*mult)
    newsession.save()
       
    #save this person as a participant
    thisplayer = SessionParticipants()
    thisplayer.person = Person.active_objects.get(pk=personpk)
    thisplayer.session = newsession
    thisplayer.minutes = minutes
    thisplayer.credits = earned_credits
    thisplayer.save()
    if newsession.dupsessid == None:
        update_total_credits(personpk, earned_credits, newsession.game)
    
    #save the rest of the players
    for t in trmn_participants:
        if t.has_changed():
            nextplayer= SessionParticipants()
            names=t.cleaned_data["person"].split(',')
            nextplayer.person = Person.active_objects.get(lastname=names[0].strip(),firstname=names[1].strip())
            nextplayer.session = newsession
            nextplayer.minutes = minutes
            nextplayer.credits = earned_credits
            if newsession.dupsessid == None:
                update_total_credits(nextplayer.person.pk, earned_credits, newsession.game)
            nextplayer.save()

    for n in nontrmn:
        if n.has_changed():
            non=NonTRMNParticipants()
            non.fullname=n.cleaned_data["fullname"]
            non.session = newsession
            non.save()

    return 'SAVED'

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
            
# endregion    

#Member Functions
#region

def transfer_branch(person:Person, newbranch:Branch):
	sessiontotals = CategoryCredits.objects.filter(person_id=person.pk) #totals from recorded sessions
	weaponawards = TotalCredits.objects.filter(person=person) #total from issued awards
	pistolweapon = Weapon.objects.get(name='Pistol') 
	rifleweapon = Weapon.objects.get(name='Rifle')
	#Navy to Army , create total credits record for all CategoryCredits
	if person.branch.name != 'RMA' and newbranch.name == 'RMA':
		toArmy = True
	else:
		if newbranch.name != 'RMA' and person.branch.name == 'RMA':  #Regroup Category credits to Pistol and Rifle
			toArmy = False

	#clear TC
	for s in weaponawards:
		s.clear()

	if toArmy == True:  
		for cc in sessiontotals:
			thisweapon = Weapon.objects.get(pk=cc.weapon_id)
			try:
				savedaward = TotalCredits.objects.get(person=person,weapon=thisweapon)
			except:      
				savedaward=TotalCredits()
				savedaward.person = person
				savedaward.weapon = thisweapon
				savedaward.createdon = datetime.now()
			savedaward.weapontotal = cc.weaponcredits 
			savedaward.save()   
	
	else:
		try:
			pistolaward = TotalCredits.objects.get(person=person,weapon=pistolweapon)
		except:  
			pistolaward = TotalCredits()
			pistolaward.person = person
			pistolaward.weapon = pistolweapon
			pistolaward.createdon = datetime.now()
		try:          
			rifleaward = TotalCredits.objects.get(person=person,weapon=rifleweapon)
		except:
			rifleaward = TotalCredits()
			rifleaward.person = person
			rifleaward.weapon = rifleweapon
			rifleaward.createdon = datetime.now()

		for cc in sessiontotals:
			if cc.weapon_id < 6:
					pistolaward.weapontotal+=cc.weaponcredits
			else:
					rifleaward.weapontotal+=cc.weaponcredits
		pistolaward.save()
		rifleaward.save()
				
	weaponawards = TotalCredits.active_objects.filter(person=person)
	for s in weaponawards:
		if (s.weapontotal>=5 and s.weapontotal < 100) and s.marksman == None:
			s.marksman = datetime.now()
		if (s.weapontotal>=100 and s.weapontotal < 200) and s.sharpshooter == None:
			s.sharpshooter = datetime.now()
		if (s.weapontotal>=200 and s.weapontotal < 600) and s.expert == None:
			s.expert = datetime.now()
		if (s.weapontotal>=600) and s.high_expert == None:
			s.high_expert = datetime.now()
		s.save()    
	
	person.branch=newbranch
	person.save()

#endregion
        
        
        



        
        


    