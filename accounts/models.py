from django.db import models
from django.contrib.auth.models import User


CLASS_CHOICES = [
    ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 7'),
    ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'),
    ('11', 'Class 11'), ('12', 'Class 12'),
]

EXAM_CHOICES = [
    ('BOARD', 'Board Exams'),
]


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES, default='10')
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    target_exam = models.CharField(max_length=20, choices=EXAM_CHOICES, default='BOARD')
    study_streak = models.IntegerField(default=0)
    total_questions_asked = models.IntegerField(default=0)
    total_tests_taken = models.IntegerField(default=0)
    total_study_hours = models.FloatField(default=0.0)
    joined_date = models.DateTimeField(auto_now_add=True)
    avatar_color = models.CharField(max_length=7, default='#FF6B35')

    def __str__(self):
        return f"{self.user.username} — Class {self.student_class}"

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
