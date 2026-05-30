from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'created_at', 'updated_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'user__username')
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'content_short', 'created_at')
    list_filter = ('role', 'created_at')

    def content_short(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_short.short_description = 'Content'
