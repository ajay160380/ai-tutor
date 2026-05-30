from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_class', 'target_exam', 'city', 'study_streak', 'total_questions_asked', 'joined_date')
    list_filter = ('student_class', 'target_exam')
    search_fields = ('user__username', 'user__email', 'city')
