from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return "{}/{}".format(self.name , self.owner) 


class BoardMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return "{} in {}".format(self.user, self.board)