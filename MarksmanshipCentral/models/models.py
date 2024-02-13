from django.db import models

# Create your models here.

class Fleet(models.Model):
    name = models.CharField(max_length=125)

class Chapter(models.Model):
    name = models.CharField(max_length=125)
    fleet = models.ForeignKey(Fleet,on_delete=models.CASCADE)
    
class Branch(models.Model):
    name = models.CharField(max_length=125)
   
   

class Person(models.Model):
    memberid = models.CharField(max_length=10,unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    emailaddress = models.CharField(max_length=255)
    passwrd = models.CharField(max_length=50)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    


class TotalCredits(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    weaponsubcategory = models.CharField(max_length=25)
    weapontotal = models.DecimalField(decimal_places=2,max_digits=10)
