from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import ChatSession, ChatMessage
from practice.models import PracticeTest, TestAttempt
from datetime import datetime, timedelta
from django.utils import timezone
from syllabus.models import SyllabusChapter
from django.db.models import Avg, Count, Q
import json


@login_required
def dashboard_view(request):
    """Student dashboard with REAL analytics and progress — no fake data."""
    user = request.user
    profile = getattr(user, 'profile', None)

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    student_class = profile.student_class if profile else '10'

    # ---- REAL Chat Stats ----
    total_sessions = ChatSession.objects.filter(user=user, student_class=student_class).count()

    week_questions = ChatMessage.objects.filter(
        session__user=user,
        session__student_class=student_class,
        role='user',
        created_at__date__gte=week_ago
    ).count()

    today_questions = ChatMessage.objects.filter(
        session__user=user,
        session__student_class=student_class,
        role='user',
        created_at__date=today
    ).count()

    # ---- REAL Recent Activity ----
    recent_messages = ChatMessage.objects.filter(
        session__user=user,
        session__student_class=student_class,
        role='user'
    ).select_related('session').order_by('-created_at')[:8]

    recent_activity = []
    for msg in recent_messages:
        recent_activity.append({
            'text': msg.content[:60] + ('...' if len(msg.content) > 60 else ''),
            'subject': msg.session.subject,
            'time': msg.created_at,
            'type': 'question'
        })

    # Also add test attempts to activity
    recent_attempts = TestAttempt.objects.filter(
        user=user, completed=True, test__class_level=student_class
    ).select_related('test').order_by('-completed_at')[:5]

    for att in recent_attempts:
        recent_activity.append({
            'text': f"Mock Test: {att.test.title} — Score: {att.score:.0f}/{att.total_marks}",
            'subject': att.test.subject,
            'time': att.completed_at or att.started_at,
            'type': 'test'
        })

    # Sort by time
    recent_activity.sort(key=lambda x: x['time'], reverse=True)
    recent_activity = recent_activity[:10]

    # ---- REAL Chart Data (daily question counts for 14 days) ----
    chart_labels = []
    chart_questions = []
    chart_tests = []
    has_chart_data = False

    for i in range(13, -1, -1):
        day = today - timedelta(days=i)
        chart_labels.append(day.strftime('%d %b'))

        day_q_count = ChatMessage.objects.filter(
            session__user=user,
            session__student_class=student_class,
            role='user',
            created_at__date=day
        ).count()
        chart_questions.append(day_q_count)

        day_test_count = TestAttempt.objects.filter(
            user=user,
            test__class_level=student_class,
            completed=True,
            completed_at__date=day
        ).count()
        chart_tests.append(day_test_count)

        if day_q_count > 0 or day_test_count > 0:
            has_chart_data = True

    # ---- REAL Subject Distribution (from chat sessions) ----
    subject_counts = (
        ChatSession.objects.filter(user=user, student_class=student_class)
        .values('subject')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    subject_colors = {
        'Physics': '#1A237E', 'Chemistry': '#00C853',
        'Mathematics': '#FF6B35', 'Biology': '#E91E63',
        'General': '#9C27B0', 'JEE': '#FF9800',
        'NEET': '#00BCD4', 'Science': '#795548',
    }

    total_chats = sum(s['count'] for s in subject_counts) or 1
    subject_dist = []
    for s in subject_counts[:6]:
        pct = round((s['count'] / total_chats) * 100)
        subject_dist.append({
            'name': s['subject'],
            'percent': pct,
            'color': subject_colors.get(s['subject'], '#6B7280'),
        })

    has_subject_data = len(subject_dist) > 0

    # ---- REAL Test Stats ----
    completed_tests = TestAttempt.objects.filter(user=user, test__class_level=student_class, completed=True)
    tests_taken = completed_tests.count()

    avg_score = 0
    if tests_taken > 0:
        scores = []
        for att in completed_tests:
            if att.total_marks > 0:
                scores.append((att.score / att.total_marks) * 100)
        avg_score = round(sum(scores) / len(scores)) if scores else 0

    # ---- REAL Weak Topics (from wrong answers in tests) ----
    weak_topics = []
    # Only show if user has taken tests
    if tests_taken > 0:
        # Analyze wrong answers from test attempts
        for att in completed_tests.order_by('-completed_at')[:5]:
            test = att.test
            questions = test.questions.all()
            subject_correct = {}
            subject_total = {}
            for q in questions:
                subj = q.subject or q.topic or 'General'
                if subj not in subject_total:
                    subject_total[subj] = 0
                    subject_correct[subj] = 0
                subject_total[subj] += 1
                q_id = str(q.id)
                if q_id in att.answers and att.answers[q_id] == q.correct_answer:
                    subject_correct[subj] += 1

            for subj, total in subject_total.items():
                if total > 0:
                    accuracy = round((subject_correct.get(subj, 0) / total) * 100)
                    if accuracy < 70:  # Only show weak ones
                        # Avoid duplicates
                        existing = [t['topic'] for t in weak_topics]
                        if subj not in existing:
                            weak_topics.append({
                                'topic': subj,
                                'subject': test.subject,
                                'accuracy': accuracy,
                            })

        weak_topics.sort(key=lambda x: x['accuracy'])
        weak_topics = weak_topics[:5]

    # ---- REAL Available Tests (upcoming = not yet attempted) ----
    target_exam = profile.target_exam if profile else 'BOARD'
    
    if target_exam == 'JEE':
        test_types = ['JEE_MAIN', 'JEE_ADV', 'CUSTOM']
    elif target_exam == 'NEET':
        test_types = ['NEET', 'CUSTOM']
    else:
        test_types = ['BOARD', 'CUSTOM']

    available_tests = PracticeTest.objects.filter(is_active=True, test_type__in=test_types, class_level=student_class)
    attempted_ids = TestAttempt.objects.filter(
        user=user, test__class_level=student_class, completed=True
    ).values_list('test_id', flat=True)

    upcoming_tests = []
    for test in available_tests:
        if test.id not in attempted_ids:
            upcoming_tests.append({
                'name': test.title,
                'date': f'{test.total_questions} Qs · {test.duration_minutes} min',
                'subject': test.subject,
            })

    # ---- Exam Countdown ----
    current_year = today.year
    
    # Calculate target year based on class
    try:
        class_num = int(student_class)
        years_to_add = max(0, 12 - class_num)
        target_year = current_year + years_to_add
    except ValueError:
        target_year = current_year + 1
        
    exam_month, exam_day = 3, 1 # March 1
        
    exam_date = datetime(target_year, exam_month, exam_day)
    days_to_exam = (exam_date.date() - today).days
    
    if days_to_exam < 0:
        target_year += 1
        exam_date = datetime(target_year, exam_month, exam_day)
        days_to_exam = (exam_date.date() - today).days

    target_exam_display = 'Board' if target_exam == 'BOARD' else target_exam
    countdown_text = f"{target_exam_display} {target_year}:"

    # ---- REAL Study Hours (estimate from chat messages — 2 min per question avg) ----
    total_user_msgs_today = today_questions
    study_hours_today = round(total_user_msgs_today * 2 / 60, 1)  # ~2 min per question

    total_user_msgs_all = ChatMessage.objects.filter(
        session__user=user, session__student_class=student_class, role='user'
    ).count()
    study_hours_total = round(total_user_msgs_all * 2 / 60, 1)

    # ---- Study Streak (count consecutive days with activity) ----
    streak = 0
    check_date = today
    for _ in range(365):
        has_activity = ChatMessage.objects.filter(
            session__user=user,
            session__student_class=student_class,
            created_at__date=check_date
        ).exists() or TestAttempt.objects.filter(
            user=user,
            test__class_level=student_class,
            started_at__date=check_date
        ).exists()

        if has_activity:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # ---- My Subjects (For the top row) ----
    my_subjects = list(
        SyllabusChapter.objects.filter(exam=f'BOARD_{student_class}')
        .order_by('subject')
        .values_list('subject', flat=True)
        .distinct()
    )

    context = {
        'profile': profile,
        'total_sessions': total_sessions,
        'week_questions': week_questions,
        'today_questions': today_questions,
        'recent_activity': recent_activity,
        'chart_labels': json.dumps(chart_labels),
        'chart_questions': json.dumps(chart_questions),
        'chart_tests': json.dumps(chart_tests),
        'has_chart_data': has_chart_data,
        'subject_dist': subject_dist,
        'has_subject_data': has_subject_data,
        'weak_topics': weak_topics,
        'upcoming_tests': upcoming_tests,
        'countdown_text': countdown_text,
        'days_to_exam': days_to_exam,
        'study_streak': streak,
        'study_hours': study_hours_today,
        'study_hours_total': study_hours_total,
        'avg_score': avg_score,
        'tests_taken': tests_taken,
        'my_subjects': my_subjects,
    }

    return render(request, 'dashboard/dashboard.html', context)
