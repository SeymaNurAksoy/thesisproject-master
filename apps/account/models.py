from http.client import FAILED_DEPENDENCY
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank = True)
    name = models.CharField(max_length=200,blank=True,null = True)
    email = models.EmailField(max_length=200,blank=True,null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

def profileUpdated(sender,instance,created,**kwargs):
    print('Profile Saved')
    print('Instance:',instance)
    print('Created:',created)

post_save.connect(profileUpdated,sender=Profile)