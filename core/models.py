from django.db import models
from django.conf import settings


class Post(models.Model):
    """Post model"""
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """User Profile model for extra info from users"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    dob = models.DateField(blank=True)
    country = models.CharField(max_length=255, default='India')
    aboutme = models.TextField()

    def __str__(self):
        return self.user.username
