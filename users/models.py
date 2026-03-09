from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - Profile'
