from django.urls import path
from .views import (IndexView, BoardView, UserValidationView,
 AddColumnView, UpdateColumnView, ArchiveColumnView, AddCardView, GetCardDetails,
 UpdateCardTitle, GetBoardDetails, UpdateCardDescription, AddCommentCard, DeleteComment,
 AssignMembers, GetMembers, DueDate, ArhiveCard, TransferCard, GetBoardStream,
 ThrowToSpecificPage)


app_name = 'boards'

urlpatterns = [
     path('', ThrowToSpecificPage.as_view(),name='throw'),
     path('boards/<str:username>/', IndexView.as_view(),name='home'),
     path('board/<int:id>', BoardView.as_view(), name='board'),
     path('boards/validate/<str:token>',UserValidationView.as_view(),name="user_validation"),
     path('add/board/<int:id>', AddColumnView.as_view(),  name="add_column"),
     path('update/board/<int:id>', UpdateColumnView.as_view(),  name="update_column"),
     path('archive/board/<int:id>', ArchiveColumnView.as_view(),  name="archive_column"),
     path('add/card/<int:id>', AddCardView.as_view(),  name="add_card"),
     path('get/board/<int:id>', GetBoardDetails.as_view(),  name="get_board"),
     path('get/card/<int:id>', GetCardDetails.as_view(),  name="get_card_detail"),
     path('update/card_title/<int:id>', UpdateCardTitle.as_view(), name="update_card_title"),
     path('update/card_description/<int:id>', UpdateCardDescription.as_view(), name="update_card_description"),
     path('add/comment/<int:id>', AddCommentCard.as_view(), name="add_comment_card"),
     path('delete/comment/<int:id>', DeleteComment.as_view(), name="delete_comment"),
     path('assign/members/<int:id>', AssignMembers.as_view(), name="assign_members"),
     path('get/members/<int:id>', GetMembers.as_view(), name="get_members"),
     path('manipulate/due_date/<int:id>', DueDate.as_view(), name="due_date"),
     path('archived/card/<int:id>', ArhiveCard.as_view(), name="archive_card"),
     path('transfer/card/<int:id>', TransferCard.as_view(), name="transfer_cards"),
     path('get/board_stream/<int:id>', GetBoardStream.as_view(), name="get_board_stream"),

]