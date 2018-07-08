
from django.http import HttpResponse
from django.urls import reverse
from .models import Column, Card
import json as simplejson
from django.core import serializers


class AJAXBoardMixIn():
    def return_board(self):
        board_id = self.kwargs.get('id')
        all_columns = Column.objects.filter(
            board__id=board_id,archived=False).order_by('position')
        card = Card.objects.filter(
            column__board__id=board_id,archived=False)
        serialized_data_card = serializers.serialize('json', card)
        serialized_data_column = serializers.serialize('json', all_columns)
        data = { 'column' : serialized_data_column, 'card' : serialized_data_card }
        return simplejson.dumps(data)