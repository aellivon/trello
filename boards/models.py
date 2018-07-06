from django.db import models
from users.models import User
from secrets import token_urlsafe 

class Board(models.Model):
    name = models.TextField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return "{}-{}".format(self.name , self.owner) 


class BoardMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{} in {}".format(self.user, self.board)

class Referral(models.Model):
    board_member = models.ForeignKey(BoardMember,on_delete=models.CASCADE)
    token = models.TextField()
    email = models.TextField()
        
    def generate_token(self):
        # Generating secure token using python 3.6 libraries
        not_found = True
        while(not_found):
            new_token = token_urlsafe(32)
            if not Referral.objects.filter(token=new_token):
                self.token = new_token
                not_found = False

    def __str__(self):
        return "{}-referral".format(email)

class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.TextField()
    position = models.IntegerField()
    archived = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(name)
