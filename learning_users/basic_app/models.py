from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE) #use this instead of inheriting cos that may screw database
    #Additional att
    portfolio_site = models.URLField(blank=True) # black = true means optional.
    profile_pic = models.ImageField(upload_to='profile_pics' , blank=True) # user can or cannot upload it..will be uploaded to profile_pics folder under media

    def __str__(self):
        return self.user.username # check slides for what User class already has as default
