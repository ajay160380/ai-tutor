from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('not_started', 'Not Started'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('revised', 'Revised'),
]


class SyllabusChapter(models.Model):
    """A chapter in the syllabus."""
    exam = models.CharField(max_length=20, default='JEE_MAIN')
    subject = models.CharField(max_length=50)
    chapter_name = models.CharField(max_length=200)
    chapter_number = models.IntegerField(default=1)
    weightage = models.FloatField(default=5.0)
    detailed_summary = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['subject', 'chapter_number']

    def __str__(self):
        return f"{self.exam} — {self.subject} — {self.chapter_name}"


class ChapterProgress(models.Model):
    """Track a student's progress on a chapter."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapter_progress')
    chapter = models.ForeignKey(SyllabusChapter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} — {self.chapter.chapter_name} — {self.status}"
