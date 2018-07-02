from django.urls import path
from .views import sign_up_view,index_view, user_validation,log_in_view, log_out_view


app_name = 'users'

urlpatterns = [
    path('', index_view.as_view(),name='home'),
    path('sign_up/',sign_up_view.as_view(),name='sign_up'),
    path('log_in/',log_in_view.as_view(),name='log_in'),
    path('log_out',log_out_view.as_view(),name='log_out'),
    path('users/validate/<str:uidb64>/<str:token>',user_validation.as_view(),name="user_validation")
]