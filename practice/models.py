from django.db import models
from django.contrib.auth.models import User


TEST_TYPE_CHOICES = [
    ('JEE_MAIN', 'JEE Main'),
    ('JEE_ADV', 'JEE Advanced'),
    ('NEET', 'NEET'),
    ('BOARD', 'Board Exams'),
    ('CUSTOM', 'Custom'),
]


class PracticeTest(models.Model):
    """A practice test/mock test."""
    title = models.CharField(max_length=200)
    class_level = models.CharField(max_length=10, default='10')
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, default='JEE_MAIN')
    subject = models.CharField(max_length=50, default='All')
    total_questions = models.IntegerField(default=30)
    duration_minutes = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=120)
    negative_marking = models.FloatField(default=1.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.test_type})"


class Question(models.Model):
    """A question in a practice test."""
    test = models.ForeignKey(PracticeTest, on_delete=models.CASCADE, related_name='questions')
    question_number = models.IntegerField()
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True)
    marks = models.IntegerField(default=4)
    subject = models.CharField(max_length=50, default='General')
    topic = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return f"Q{self.question_number}: {self.question_text[:60]}"


class TestAttempt(models.Model):
    """A student's attempt at a test."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(PracticeTest, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    total_marks = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    unanswered = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)
    answers = models.JSONField(default=dict)  # {question_id: selected_option}
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} — {self.test.title} — {self.score}/{self.total_marks}"
