from django.urls import path
from . import views

urlpatterns = [
    path('', views.syllabus_tracker, name='syllabus_tracker'),
    path('update-status/', views.update_chapter_status, name='update_chapter_status'),
    path('summary/<int:chapter_id>/', views.get_chapter_summary, name='get_chapter_summary'),
]
