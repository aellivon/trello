from django.db import models
from django.contrib.auth.models import User


def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	initials = models.CharField(max_length=8)
	bio = models.CharField(max_length=200)
	is_confirmed = models.BooleanField(default=False)
