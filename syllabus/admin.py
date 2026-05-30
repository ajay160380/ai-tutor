from django.contrib import admin
from .models import SyllabusChapter, ChapterProgress


@admin.register(SyllabusChapter)
class SyllabusChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'exam', 'subject', 'chapter_number', 'weightage')
    list_filter = ('exam', 'subject')
    search_fields = ('chapter_name',)


@admin.register(ChapterProgress)
class ChapterProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'status', 'updated_at')
    list_filter = ('status',)
