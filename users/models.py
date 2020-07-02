from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20,unique=True,null=False)
    first_name = models.CharField(max_length=20,null=False)
    last_name = models.CharField(max_length=20,null=False)
    email_id = models.EmailField(null=False)
    password = models.CharField(max_length=20,null=False)
    profile_pic = models.ImageField(upload_to='media')
    def __str__(self):
        return self.user_id


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_owner = models.ForeignKey(Users,on_delete=models.CASCADE)
    event_name = models.CharField(max_length=20,unique=True,null=False)
    description = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now=True)
    creation_time = models.TimeField(auto_now=True)
    event_image = models.ImageField(upload_to=None)

    
class Register(models.Model):
    register_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Events,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete = models.CASCADE)