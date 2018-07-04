from django.urls import path
from .views import SignUpView, LogInView, LogOutView


app_name = 'users'

urlpatterns = [
   
    path('sign_up/',SignUpView.as_view(),name='sign_up'),
    path('log_in/',LogInView.as_view(),name='log_in'),
    path('log_out',LogOutView.as_view(),name='log_out'),
]