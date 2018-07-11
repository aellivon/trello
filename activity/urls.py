from django.urls import path
from .views import ActivityView


app_name = 'activity'

urlpatterns = [
     path('activity/<str:user>/', ActivityView.as_view(),name='activities'),
]