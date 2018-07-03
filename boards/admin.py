from django.contrib import admin

from .models import BoardMember, Board

admin.site.register(BoardMember)
admin.site.register(Board)