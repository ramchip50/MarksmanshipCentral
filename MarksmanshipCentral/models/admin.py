from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Game,list_display=["name","alias","weapon","verified"])

admin.site.register(Session)

admin.site.register(SessionParticipants)

admin.site.register(NonTRMNParticipants)

admin.site.register(Person)

admin.site.register(TotalCredits, list_display=["person","weapon","weapontotal","marksman","sharpshooter","expert","high_expert"])

admin.site.register(Chapter,list_display=["name","fleet"])

admin.site.register(Branch)

admin.site.register(Fleet)

admin.site.register(Award)

admin.site.register(AwardSubcategory)

#admin.site.register(Weapon,list_display=["id","name"])