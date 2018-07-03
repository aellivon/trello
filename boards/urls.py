from django.urls import path
from .views import IndexView, BoardView


app_name = 'boards'

urlpatterns = [
     path('users/<str:username>/', IndexView.as_view(),name='home'),
     path('boards/<int:id>', BoardView.as_view(), name='board')
    # path('users/validate/<str:uidb64>/<str:token>',user_validation.as_view(),name="user_validation")
]