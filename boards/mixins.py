
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from .models import Column, Card, CardComment, BoardMember
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
        all_columns = Column.objects.filter(
            board__id=board_id,archived=False).order_by('position')
        card = Card.objects.filter(
            column__board__id=board_id,archived=False)
        serialized_data_card = serializers.serialize('json', card)
        serialized_data_column = serializers.serialize('json', all_columns)
        data = { 'column' : serialized_data_column, 'card' : serialized_data_card }
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
        # brackets are needed since they are single objects
        card = [get_object_or_404(Card,pk=card_id)]
        card_comments = CardComment.objects.filter(
            card__id=card_id).select_related('user').order_by('-pk')
        current_user = {'current_user' : self.request.user.username}
        serialized_data_cards = serializers.serialize('json', card)
        if card_comments:
            serialized_data_comments = serializers.serialize('json', card_comments, 
                use_natural_foreign_keys=True)
            data = { 'cards' : serialized_data_cards,
                 'comments' : serialized_data_comments,
                 'current_user' : current_user}
        else:
            data = { 'cards' : serialized_data_cards,
                    'current_user' : current_user }
        return data

class BoardPermissionMixIn():
    """
        Get if the one accessing the url is a board member.
        If not board member, throw bad request.
    """
    def dispatch(self, request, *args, **kwargs):
        board_id = self.kwargs.get('id')
        # Permission Denied if 404
        exists = get_object_or_None(
            BoardMember, board__id=board_id,user__pk=self.request.user.id)
        if not exists:
            return HttpResponseBadRequest()

        return super().dispatch(request, *args, **kwargs)