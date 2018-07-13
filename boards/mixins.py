
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render
from .models import Column, Card, CardComment, BoardMember, Board
from users.models import User
from activity.models import Activity
import json as simplejson
from django.core import serializers
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None


class AJAXBoardMixIn():
    """
        for returning the necessary data to refresh the board
    """
    def return_board(self):
        board_id = self.kwargs.get('id')
        board = get_object_or_404(Board,pk=self.kwargs.get('id'))
        all_columns = Column.objects.filter(
            board__id=board_id,archived=False).order_by('position')
        cards = Card.objects.filter(
            column__board__id=board_id,archived=False)

        serialized_data_card = serializers.serialize('json', cards)
        serialized_data_column = serializers.serialize('json', all_columns)

        data = { 'column' : serialized_data_column,
            'card' : serialized_data_card
        }
        return data

class AJAXCardMixIn():
    """
        for returning the necessary data to refresh the card
    """
    def return_card(self):
        card_id = 0
        if self.request.method == "GET":
            card_id = self.request.GET.get('card_id')
        else:
            card_id = self.request.POST.get('card_id')
        board = get_object_or_404(Board,pk=self.kwargs.get('id'))
        # brackets are needed since they are single objects
        card = [get_object_or_404(Card,pk=card_id)]
        card_comments = CardComment.objects.filter(
            card__id=card_id, archived=False).select_related('user').order_by('-pk')
        current_user = {'current_user' : self.request.user.username}
        serialized_data_card = serializers.serialize('json', card)

        if card_comments:
            serialized_data_comments = serializers.serialize('json', card_comments, 
                use_natural_foreign_keys=True)
            data = { 'cards' : serialized_data_card,
                     'comments' : serialized_data_comments,
                     'current_user' : current_user
                  }
        else:
            data = { 'cards' : serialized_data_card,
                    'current_user' : current_user
                    }
        return data

class BoardPermissionMixIn():
    """
        Get if the one accessing the url is a board member.
        If not board member, throw bad request.
    """
    error_board = "boards/error_member.html"
    def dispatch(self, request, *args, **kwargs):
        board_id = self.kwargs.get('id')
        # Permission Denied if 404
        exists = get_object_or_None(
            BoardMember, board__id=board_id, user__pk=self.request.user.id,
            archived=False)
        if not exists:
            return render(self.request, self.error_board,
                {"current_user":self.request.user.username})

        return super().dispatch(request, *args, **kwargs)

