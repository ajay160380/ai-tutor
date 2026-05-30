from django.db import models
from django.contrib.auth.models import User


class DailyProgress(models.Model):
    """Track daily study progress for analytics."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_progress')
    date = models.DateField()
    study_hours = models.FloatField(default=0)
    questions_asked = models.IntegerField(default=0)
    math_score = models.IntegerField(default=0)
    science_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} — {self.date}"
