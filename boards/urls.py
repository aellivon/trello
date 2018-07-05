from django.urls import path
from .views import (IndexView, BoardView, UserValidationView,
 AddColumnView, UpdateColumnView, ArchiveColumnView)


app_name = 'boards'

urlpatterns = [
     path('boards/<str:username>/', IndexView.as_view(),name='home'),
     path('board/<int:id>', BoardView.as_view(), name='board'),
     path('boards/validate/<str:token>',UserValidationView.as_view(),name="user_validation"),
     path('add/board/<int:id>', AddColumnView.as_view(),  name="add_column"),
     path('update/board', UpdateColumnView.as_view(),  name="update_column"),
     path('archive/board', ArchiveColumnView.as_view(),  name="archive_column"),
]