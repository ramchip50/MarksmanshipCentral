from django.contrib import admin

# Register your models here.



#Put in delete action for soft delete
from django.forms import modelformset_factory
from .models import *

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name","alias","weapon","verified")
    search_fields=("name__startswith","alias__startswith")
    ordering = ("name",)
    
    pass

class ParticipantsInLine(admin.StackedInline):
    model = SessionParticipants
    extra = 4
    max_num = 4
    
@admin.register(Session)
@admin.display(description="member",)
class SessionAdmin(admin.ModelAdmin):
    list_display=("game","startdate","enddate","playmode")
    list_select_related=True
    list_filter=("game","playmode")
    date_hierarchy='startdate'
    search_fields=["game__name"]
    ordering=("startdate","game")
    inlines = [ParticipantsInLine]
    pass

# @admin.register(SessionParticipants)
# class SessionParticipantsAdmin(admin.ModelAdmin):
#     list_display=("session","person")
#     pass

# @admin.register(NonTRMNParticipants)
# class NonTRMNParticpantsAdmin(admin.ModelAdmin):
#     pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display=("lastname","firstname","branch","chapter")
    list_select_related=("branch","chapter")
    list_filter=("branch","chapter")
    search_fields=("lastname__startswith",)
    ordering=("lastname","firstname")
    pass

@admin.register(TotalCredits)
class TotalCreditsAdmin(admin.ModelAdmin):
    list_display=("person","weapon","weapontotal","marksman","sharpshooter","expert","high_expert")
    list_select_related=True
    search_fields=["person__lastname"]
    ordering=("person__lastname","person__firstname")
    list_filter=("person__lastname",)
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display=("name","fleet")
    pass

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    pass

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display=("awardname","branch")
    pass

#admin.register(AwardSubcategory)

