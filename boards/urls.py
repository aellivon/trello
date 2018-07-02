from django.urls import path
from .views import IndexView


app_name = 'boards'

urlpatterns = [
     path('users/<str:username>/', IndexView.as_view(),name='home'),
    # path('users/validate/<str:uidb64>/<str:token>',user_validation.as_view(),name="user_validation")
]