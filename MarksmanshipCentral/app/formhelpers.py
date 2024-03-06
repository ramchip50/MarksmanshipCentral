import datetime
from django.forms import BaseModelFormSet
from django.db.models import Value
from django.db.models.functions import Concat
from models.models import *






def player_select_list():

    return Person.active_objects.all().order_by("lastname","firstname").annotate(full_name = Concat('lastname',Value(', '),'firstname')).values_list("id","full_name")
