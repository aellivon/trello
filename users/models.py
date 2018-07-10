from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_location(instance, filename):
    return "{}/{}".format(instance.id, filename)

class User(AbstractUser):
    """
        Extends the user with a bio field
    """
    bio = models.TextField(max_length=200,default="")
    

    def __str__(self):
        return "{}".format(self.username)

    def get_initials(self):
    	return "{}{}".format(self.first_name,self.last_name)

