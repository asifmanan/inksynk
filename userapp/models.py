from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
# Create your models here.
# asifm samepassword
# class UserProfile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pictures',blank=True)
#     def __str__(self):
#         return self.user.username

class Gender(models.TextChoices):
    Male = "MALE", _('Male')
    Female = "FEMALE", _('Female')
    NotSpecified = "NOTSPECIFIED", _('Not Specified')

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30,unique=True,null=True,blank=True)
    slug = AutoSlugField(unique=True,populate_from="user")
    is_author = models.BooleanField(default=False)
    brief_intro = models.CharField(max_length=1024, blank=True)
    gender = models.CharField(max_length=12, choices=Gender.choices, default=Gender.NotSpecified)
    profile_picture = models.ImageField(upload_to='profile_pictures',blank=True)
    def __str__(self):
        return self.user.username



# class User(auth.models.User,auth.models.PermissionsMixin):
#     def __str__(self):
#         return self.username
