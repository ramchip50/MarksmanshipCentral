from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Game)

admin.site.register(Session)

admin.site.register(SessionParticipants)

admin.site.register(NonTRMNParticipants)

admin.site.register(Person)

admin.site.register(TotalCredits)

admin.site.register(Chapter)

admin.site.register(Branch)

admin.site.register(Fleet)

admin.site.register(PeopleAwards)

admin.site.register(Award)

admin.site.register(AwardSubcategory)