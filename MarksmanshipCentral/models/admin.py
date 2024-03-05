from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=("name","alias","weapon","verified")
    search_fields=("name__startswith","alias__startswith")
    ordering = ("name",)
    
    pass
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

@admin.register(SessionParticipants)
class SessionParticipantsAdmin(admin.ModelAdmin):
    pass

@admin.register(NonTRMNParticipants)
class NonTRMNParticpantsAdmin(admin.ModelAdmin):
    pass

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

