from django.contrib import admin

from .models import BoardMember, Board, Referral, Column, Card

admin.site.register(BoardMember)
admin.site.register(Board)
admin.site.register(Referral)
admin.site.register(Column)
admin.site.register(Card)