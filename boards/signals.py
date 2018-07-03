from .models import Board, BoardMember
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Board)
def add_board_member(sender, instance, **kwargs):
	new_board_member = BoardMember(user=instance.owner,board=instance)
	new_board_member.is_confirmed = True
	new_board_member.save()
