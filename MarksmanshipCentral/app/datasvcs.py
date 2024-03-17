# Home for SQL Queries


from django.db import connection
from collections import namedtuple
from models.models import *
from datetime import *


def gettotal_sql():
    mbr = 7014
    wpn = 'Rifle'
    #query = "Select person_id,weapon_id,marksman,sharpshooter,expert,high_expert from models_totalcredits where active = 1 and person_id = %s"
    query = "Select lastname, firstname,weapon,weaponcredits from modelview_categorycredits where person_id = %s and weapon = %s"
    with connection.cursor() as cursor:
        cursor.execute(query,[mbr,wpn])
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

def get_allsessioncredits_bydate_andchapter(startdate:datetime,enddate:datetime,chapter:Chapter):
    allsessions = get_allsessioncredits_bydate(startdate,enddate)
    result = list()
    for sess in allsessions:
        if sess.chapter == chapter.name:
            result.append(sess)
      
    return result

def get_allsessioncredits_bydate_andfleet(startdate:datetime,enddate:datetime,fleet:Fleet):
    allsessions = get_allsessioncredits_bydate(startdate,enddate)
    result = list()
    for sess in allsessions:
        if sess.fleet == fleet.name:
            result.append(sess)

    return result

def get_allsessioncredits_bydate(startdate:datetime,enddate:datetime):
    
    with connection.cursor() as cursor:
        cursor.callproc('get_all_sessioncredits_bydate',[startdate,enddate])
        results = namedtuplefetchall(cursor)

    return results



    
    