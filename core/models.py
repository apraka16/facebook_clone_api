from django.db import models
from django.conf import settings


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
