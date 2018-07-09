from django.urls import path
from .views import (IndexView, BoardView, UserValidationView,
 AddColumnView, UpdateColumnView, ArchiveColumnView, AddCardView, GetCardDetails,
 UpdateCardTitle)


app_name = 'boards'

urlpatterns = [
     path('boards/<str:username>/', IndexView.as_view(),name='home'),
     path('board/<int:id>', BoardView.as_view(), name='board'),
     path('boards/validate/<str:token>',UserValidationView.as_view(),name="user_validation"),
     path('add/board/<int:id>', AddColumnView.as_view(),  name="add_column"),
     path('update/board/<int:id>', UpdateColumnView.as_view(),  name="update_column"),
     path('archive/board/<int:id>', ArchiveColumnView.as_view(),  name="archive_column"),
     path('add/card/<int:id>', AddCardView.as_view(),  name="add_card"),
     path('get/card/<int:id>', GetCardDetails.as_view(),  name="get_card_detail"),
     path('update/card_title', UpdateCardTitle.as_view(), name="update_card_title")
]