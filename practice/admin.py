from django.contrib import admin
from .models import PracticeTest, Question, TestAttempt


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(PracticeTest)
class PracticeTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_type', 'subject', 'total_questions', 'duration_minutes', 'is_active')
    list_filter = ('test_type', 'subject', 'is_active')
    inlines = [QuestionInline]


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'total_marks', 'correct_answers', 'wrong_answers', 'completed')
    list_filter = ('completed', 'test__test_type')
