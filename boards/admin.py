from django.contrib import admin

from .models import BoardMember, Board, Referral, Column, Card, CardComment, CardMember

admin.site.register(BoardMember)
admin.site.register(Board)
admin.site.register(Referral)
admin.site.register(Column)
admin.site.register(Card)
admin.site.register(CardComment)
admin.site.register(CardMember)