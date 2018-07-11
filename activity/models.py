from datetime import datetime

from django.db import models
from users.models import User
from boards.models import Board,Column,Card

class Activity(models.Model):
    CHOICES = (('moved', 'moved'), ('added', 'added'), ('on','on'), ('archived','archived'),('to','to'), ('updated','updated'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initial_user")
    action = models.CharField(max_length=25,choices=CHOICES)
    added_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_user",blank=True,null=True)
    from_list = models.ForeignKey(Column,on_delete=models.CASCADE, related_name="from_list",blank=True,null=True)
    card =  models.ForeignKey(Card,on_delete=models.CASCADE, related_name="card",blank=True,null=True)
    comment = models.TextField(blank=True,null=True)
    second_action =  models.CharField(max_length=25,choices=CHOICES, blank=True,null=True)
    to_list = models.ForeignKey(Column,on_delete=models.CASCADE, related_name="to_list",blank=True,null=True)
    to_card =  models.ForeignKey(Card,on_delete=models.CASCADE, related_name="to_card",blank=True,null=True)
    board_name = models.ForeignKey(Board, on_delete=models.CASCADE) 
    modified = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return "{}".format(self.user) 

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        