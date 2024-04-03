from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from datetime import datetime

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

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

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
    role = models.ForeignKey(Role,on_delete=models.CASCADE,default=1)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    active_objects = ActiveManager()
    objects = models.Manager()


    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"
    
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon = datetime.now()
        super().save(**kwargs)
    
    def save(self,*args, **kwargs):
        self.modifiedon = datetime.now()
        super().save(**kwargs)



class TotalCredits(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon,on_delete=models.DO_NOTHING,default=0)
    weapontotal = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    marksman = models.DateField(null=True, blank=True)
    sharpshooter = models.DateField(null=True, blank=True)
    expert = models.DateField(null=True, blank=True)
    high_expert = models.DateField(null=True, blank=True)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    active_objects = ActiveManager()
    objects = models.Manager()
    
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon = datetime.now()
        super().save(**kwargs)
    
    def save(self,*args, **kwargs):
        self.modifiedon = datetime.now()
        super().save(**kwargs)

    def clear(self):
        self.modifiedon = datetime.now()
        self.marksman = None
        self.sharpshooter = None
        self.expert = None
        self.high_expert = None
        self.weapontotal = 0
        self.save()

    class Meta:
        verbose_name = 'Total Credit Log'
        verbose_name_plural= 'Total Credit Logs'


class Game(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=255)
    weapon = models.ForeignKey(Weapon,on_delete=models.CASCADE,default=0)
    verified = models.BooleanField(default=False)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    active_objects = ActiveManager()
    objects = models.Manager()
  
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon = datetime.now()
        super().save(**kwargs)
    
    def save(self,*args, **kwargs):
        self.modifiedon = datetime.now()
        super().save(**kwargs)

    def __str__(self):
        return f"{self.name}"

    
class Session(models.Model):
    game = models.ForeignKey(Game,on_delete=models.DO_NOTHING)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    playmode = models.CharField(max_length=10)
    turnsplayed = models.IntegerField(null=True)
    dupsessid = models.IntegerField(null=True)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    active_objects = ActiveManager()
    objects = models.Manager()
    
    class Meta:
        verbose_name = "Game Session"
        verbose_name_plural = "Game Sessions"
     
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon = datetime.now()
        super().save(**kwargs)
    
    def save(self,*args, **kwargs):
        self.modifiedon = datetime.now()
        super().save(**kwargs)
        
    def fill(self,game, startdate, enddate, playmode, turnsplayed):
        self.game = game
        self.startdate = startdate
        self.enddate = enddate
        self.playmode = playmode
        self.turnsplayed = turnsplayed

        
class SessionParticipants(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    minutes = models.IntegerField()
    credits = models.DecimalField(decimal_places=2,max_digits=10)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    active_objects = ActiveManager()
    objects = models.Manager()
    
    class Meta:
        verbose_name = "Game Session Player"
        verbose_name_plural = "Game Session Players"
        
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon = datetime.now()
        super().save(**kwargs)
    
    def save(self,*args, **kwargs):
        self.modifiedon = datetime.now()
        super().save(**kwargs)        

    def __str__(self):
        return f"{self.person.lastname}, {self.person.firstname}"

class CategoryCredits(models.Model):
    id = models.IntegerField(primary_key=True)
    person_id = models.IntegerField()
    lastname = models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    weapon=models.CharField(max_length=50)
    weapon_id=models.IntegerField()
    weaponcredits=models.DecimalField(max_digits=10,decimal_places=2)
    
    class Meta:
        managed=False
        db_table='modelview_categorycredits'

class NonTRMNParticipants(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, null=True)
    createdon = models.DateTimeField(auto_now=True)
    modifiedon = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def save(self, **kwargs):
        self.modifiedon=datetime.now()
        super().save(**kwargs)
        
    def delete(self, **kwargs):
        self.active=False
        self.modifiedon=datetime.now()
        super().save(**kwargs)

    objects = models.Manager()
    active_objects = ActiveManager()


   


  

    


