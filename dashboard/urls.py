from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('focus/', views.focus_room_view, name='focus_room'),
]
