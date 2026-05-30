from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list_view, name='test_list'),
    path('take/<int:test_id>/', views.take_test_view, name='take_test'),
    path('submit/<int:attempt_id>/', views.submit_test, name='submit_test'),
    path('result/<int:attempt_id>/', views.test_result_view, name='test_result'),
    path('chapter-test/<int:chapter_id>/', views.create_chapter_test, name='create_chapter_test'),
]
