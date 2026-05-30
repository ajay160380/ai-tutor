from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('new/', views.new_session, name='new_session'),
    path('delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('history/', views.chat_history, name='chat_history'),
]
