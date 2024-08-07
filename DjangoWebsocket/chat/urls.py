from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='main'),
    path('activity_report/', activity_report, name='activity_report'),
    path('<str:room_name>/', room, name='room'),
]
