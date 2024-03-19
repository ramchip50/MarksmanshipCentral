# Home for SQL Queries


from django.db import connection
from collections import namedtuple
from models.models import *
from datetime import *




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

def get_earned_awards_bydate(startdate:datetime,enddate:datetime):
    
    with connection.cursor() as cursor:
        cursor.callproc('get_earned_awards_bydate',[startdate,enddate])
        results = namedtuplefetchall(cursor)

    return results

def get_earned_awards_bydate_andchapter(startdate:datetime,enddate:datetime,chapter:Chapter):
    
    allawards = get_earned_awards_bydate(startdate,enddate)
    result = list()
    for award in allawards:
        if award.chapter == chapter.name:
            result.append(award)
      
    return result


def get_earned_awards_bydate_andfleet(startdate:datetime,enddate:datetime,fleet:Fleet):
    
    allawards = get_earned_awards_bydate(startdate,enddate)
    result = list()
    for award in allawards:
        if award.chapter == fleet.name:
            result.append(award)
      
    return result

    
    