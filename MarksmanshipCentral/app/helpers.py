#Common Functions Go here. reference = from app.helpers import * 



from django.db.models import Value
from django.db.models.functions import Concat
from models.models import Person, Role




#def has_role(person_pk, role_name):
   # roles = PersonRoles.objects.all()
   
    #     return True
    # else:
    #     return False
    
    
    
def player_select_list():
    plist = Person.objects.all().order_by("lastname","firstname").annotate(full_name = Concat('lastname',Value(', '),'firstname')).values_list("id","full_name")
    i = plist.__len__


def something_good():
    return 'lemon pie'    