from django.db import models
from django.contrib.auth.models import User


def upload_location(instance, filename):
    return "{}/{}".format(instance.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initials = models.CharField(max_length=8)
    bio = models.CharField(max_length=200)
    

    def __str__(self):
        return self.user
