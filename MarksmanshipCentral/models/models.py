from typing import Required
from django.db import models

# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)



class Fleet(models.Model):
    name = models.CharField(max_length=125)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    
    def __str__(self):
        return f"{self.name}"


class Chapter(models.Model):
    name = models.CharField(max_length=125)
    fleet = models.ForeignKey(Fleet,on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()


    def __str__(self):
        return f"{self.name}"


    
class Branch(models.Model):
    name = models.CharField(max_length=125)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.name}"


class Weapon(models.Model):
    name=models.CharField(max_length=25,editable=False)
   
    def __str__(self):
        return f"{self.name}"

class Role(models.Model):
    name = models.CharField(max_length=50)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.name}"

class Person(models.Model):
    memberid = models.CharField(max_length=10,unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    emailaddress = models.CharField(max_length=255)
    passwrd = models.CharField(max_length=50)
    role = models.ForeignKey(Role,on_delete=models.CASCADE,default=0)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()


    def __str__(self):
        return f"{self.lastname}, {self.firstname}"



class TotalCredits(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon,on_delete=models.CASCADE,default=0)
    weapontotal = models.DecimalField(decimal_places=2,max_digits=10)
    marksman = models.DateField(null=True, blank=True)
    sharpshooter = models.DateField(null=True, blank=True)
    expert = models.DateField(null=True, blank=True)
    high_expert = models.DateField(null=True, blank=True)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()


class Game(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=255)
    weapon = models.ForeignKey(Weapon,on_delete=models.CASCADE,default=0)
    verified = models.BooleanField(default=False)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
        
    def __str__(self):
        return f"{self.name}"

    
class Session(models.Model):
    game = models.ForeignKey(Game,on_delete=models.DO_NOTHING)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    playmode = models.CharField(max_length=10)
    turnsplayed = models.IntegerField()
    flagged = models.BooleanField(default=False)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
        
class SessionParticipants(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    minutes = models.IntegerField()
    credits = models.DecimalField(decimal_places=2,max_digits=10)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    

    
class NonTRMNParticipants(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    emailaddress = models.CharField(max_length=255)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()


class Award(models.Model):
    branch = models.ForeignKey(Branch,on_delete=models.DO_NOTHING)
    awardname = models.CharField(max_length=25)
    weapon = models.ForeignKey(Weapon,on_delete=models.CASCADE,default=0)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    
    def __str__(self):
        return f"{self.awardname}"    


  
class AwardSubcategory(models.Model):
    award = models.ForeignKey(Award,on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon,on_delete=models.CASCADE,default=0)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    


