from django.db import models

# Create your models here.
class Registor_User(models.Model):
    Name = models.CharField(max_length=100)
    Password = models.CharField(max_length=500)
    Phone_no = models.IntegerField(unique=True)
    Email = models.CharField(max_length=100,blank=True)

class Registor_Contact(models.Model):
    User_id = models.ForeignKey(Registor_User,on_delete=models.CASCADE,null=True)
    Contact_no = models.IntegerField()
    Name = models.CharField(max_length=100)
    spam = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)


    

