from django.urls import path
from .views import SignUpView,IndexView,LogInView, LogOutView


app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(),name='home'),
    path('sign_up/',SignUpView.as_view(),name='sign_up'),
    path('log_in/',LogInView.as_view(),name='log_in'),
    path('log_out',LogOutView.as_view(),name='log_out'),
    # path('users/validate/<str:uidb64>/<str:token>',user_validation.as_view(),name="user_validation")
]