from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """A chat conversation session between a user and EduAI."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    student_class = models.CharField(max_length=10, default='10')
    title = models.CharField(max_length=100, default='New Chat')
    subject = models.CharField(max_length=50, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class ChatMessage(models.Model):
    """A single message in a chat session."""
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
