from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.IntegerField(primary_key=True,auto_created=True)
    user_name = models.CharField(max_length=20,unique=True,null=False)
    first_name = models.CharField(max_length=20,null=False)
    last_name = models.CharField(max_length=20,null=False)
    email_id = models.EmailField(null=False)
    password = models.CharField(max_length=20,null=False)
    profile_pic = models.CharField(max_length=20,null=False)

class Events(models.Model):
    event_id = models.IntegerField(primary_key=True,auto_created=True)
    event_name = models.CharField(max_length=20,unique=True,null=False)
    description = models.CharField(max_length=100)
class Register(models.Model):
    register_id = models.IntegerField(primary_key=True,auto_created=True)
    event_id = models.ForeignKey(Events,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete = models.CASCADE)