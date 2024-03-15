# Home for SQL Queries


from django.db import connection
from collections import namedtuple
from datetime import datetime

def gettotal_sql():
    mbr = 7014
    #query = "Select person_id,weapon_id,marksman,sharpshooter,expert,high_expert from models_totalcredits where active = 1 and person_id = %s"
    #query = "Select lastname, firstname,weapon,weaponcredits from modelview_categorycredits where person_id = %s"

    query = "Select lastname, firstname,weapon,weaponcredits from modelview_categorycredits where person_id = %s and weapon=%s"
    with connection.cursor() as cursor:
        cursor.execute(query,[mbr])
        results = namedtuplefetchall(cursor)
        
    return results
    

def getsessioncredits():
	mbr = 7014
	startdate = datetime(2024,2,1)
	enddate = datetime(2024,4,1)
	#query = "Select person_id,weapon_id,marksman,sharpshooter,expert,high_expert from models_totalcredits where active = 1 and person_id = %s"
	#query = "Select lastname, firstname,weapon,weaponcredits from modelview_categorycredits where person_id = %s"

	query = "select models_sessionparticipants.id as id, models_person.id as person_id, models_person.lastname,models_person.firstname,"\
			"models_chapter.name as chapter, models_fleet.name as fleet, models_weapon.name as weapon, models_weapon.id as weapon_id, "\
			"models_branch.name as branch, sum(models_sessionparticipants.credits) as weaponcredits"\
			"from models_sessionparticipants "\
			"join models_person on ((models_sessionparticipants.person_id = models_person.id) and models_person.active=1) "\
			"join models_branch on ((models_person.branch_id = models_branch.id) and models_branch.active=1) "\
			"join models_chapter on ((models_person.chapter_id = models_chapter.id) and models_chapter.active=1) "\
			"join models_fleet on ((models_chapter.fleet_id = models_fleet.id) and models_fleet.active=1) "\
			"join models_session on ((models_sessionparticipants.session_id = models_session.Id) and (models_session.active=1 and models_session.flagged=0)) "\
			"join models_game on ((models_session.game_id = models_game.id) and (models_game.active=1 and models_game.verified=1)) "\
			"join models_weapon on models_game.weapon_id = models_weapon.Id "\
			" where models_sessionparticipants.active=1 "\
			" and models_session.enddate >= %s and models_session.enddate <= %s group by models_sessionparticipants.person_id, models_game.weapon_id"


	with connection.cursor() as cursor:
		cursor.execute(query,[startdate,enddate])
		results = namedtuplefetchall(cursor)
		
	return results


def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    Assume the column names are unique.
    """
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

