from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =models.ImageField(upload_to='profile_pictures',default='profile_pictures\\default_profile_picture.png')
    location = models.CharField(max_length=128,null=True,blank=True)
    phone_number = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self) -> str:
         return self.user.username+" | profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.user
    except:
        UserProfile.objects.create(user=instance)
