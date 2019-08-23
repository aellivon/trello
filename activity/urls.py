from django.urls import path
from .views import ActivityView


app_name = 'activity'

urlpatterns = [
     path('activity', ActivityView.as_view(), name='activities'),
]