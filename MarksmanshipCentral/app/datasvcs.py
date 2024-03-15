# Home for SQL Queries


from django.db import connection
from collections import namedtuple

def gettotal_sql():
    mbr = 7014
    #query = "Select person_id,weapon_id,marksman,sharpshooter,expert,high_expert from models_totalcredits where active = 1 and person_id = %s"
    query = "Select lastname, firstname,weapon,weaponcredits from modelview_categorycredits where person_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query,[mbr])
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