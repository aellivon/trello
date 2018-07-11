from datetime import datetime

from django.db import models
from users.models import User
from boards.models import Board,Column,Card

class Activity(models.Model):
    """
        models for activity
        this fields forms a sttring if they have values
        not all values is required in this model
    """
    CHOICES = (
        ('added_list', 'added_list'), ('update_list', 'update_list'),
        ('archived_list','archived_list'), ('added_card','added_card'),
        ('updated_card_title','updated_card_title'),
        ('updated_card_description','updated_card_description'),
        ('add_comment','add_comment'),('deleted_comment','deleted_comment'),
        ('transferred_card','transferred_card'), ('assign_member', 'assign_member')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="initial_user"
    )
    board = models.ForeignKey(Board, on_delete=models.CASCADE) 
    action = models.CharField(max_length=25,choices=CHOICES)
    first_list = models.ForeignKey(
        Column,on_delete=models.CASCADE, related_name="first_list",blank=True,null=True
    )
    first_card =  models.ForeignKey(
        Card,on_delete=models.CASCADE, related_name="card",blank=True,null=True
    )
    second_list = models.ForeignKey(
        Column,on_delete=models.CASCADE, related_name="second_list",blank=True,null=True
    )
    added_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="added_user", blank=True,
        null=True
    )
    
    modified = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return "{}".format(self.user) 

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        