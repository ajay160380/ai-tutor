from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.shortcuts import get_object_or_404
from .models import SyllabusChapter, ChapterProgress
from chat.services import generate_chapter_summary


from .data import DEFAULT_SYLLABUS

def _seed_syllabus():
    """Create default syllabus chapters if none exist."""
    if SyllabusChapter.objects.exists():
        return

    for exam, subjects in DEFAULT_SYLLABUS.items():
        for subject, chapters in subjects.items():
            for i, (name, weightage) in enumerate(chapters, 1):
                SyllabusChapter.objects.create(
                    exam=exam,
                    subject=subject,
                    chapter_name=name,
                    chapter_number=i,
                    weightage=weightage,
                )


@login_required
def syllabus_tracker(request):
    """Syllabus tracker page with chapter-wise progress."""
    # Seed data if empty
    _seed_syllabus()

    # Filter available exams based on user profile
    profile = getattr(request.user, 'profile', None)
    student_class = profile.student_class if profile else '10'
    
    # We are removing JEE/NEET. Everyone is a Board student now.
    exam_choices = [(f'BOARD_{student_class}', f'Class {student_class}')]
    default_exam = f'BOARD_{student_class}'

    exam = request.GET.get('exam', default_exam)
    subject = request.GET.get('subject')

    chapters = SyllabusChapter.objects.filter(exam=exam)
    if subject:
        chapters = chapters.filter(subject=subject)
    else:
        # Default to first subject
        first_subject = chapters.values_list('subject', flat=True).first()
        if first_subject:
            subject = first_subject
            chapters = chapters.filter(subject=subject)

    # Get user progress
    progress_map = {}
    user_progress = ChapterProgress.objects.filter(user=request.user, chapter__in=chapters)
    for p in user_progress:
        progress_map[p.chapter_id] = p.status

    # Get completed tests for chapters
    from practice.models import TestAttempt
    test_titles = [f"{ch.subject} - {ch.chapter_name} Test" for ch in chapters]
    completed_test_titles = set(TestAttempt.objects.filter(
        user=request.user,
        completed=True,
        test__title__in=test_titles
    ).values_list('test__title', flat=True))

    chapter_data = []
    completed_count = 0
    for ch in chapters:
        status = progress_map.get(ch.id, 'not_started')
        if status in ('completed', 'revised'):
            completed_count += 1
            
        test_title = f"{ch.subject} - {ch.chapter_name} Test"
        chapter_data.append({
            'id': ch.id,
            'name': ch.chapter_name,
            'number': ch.chapter_number,
            'weightage': ch.weightage,
            'status': status,
            'test_completed': test_title in completed_test_titles,
        })

    total = len(chapter_data)
    progress_percent = round((completed_count / max(total, 1)) * 100)

    # Make sure we don't overwrite our dynamic exam_choices
    # We already defined exam_choices above based on profile

    subject_choices = list(
        SyllabusChapter.objects.filter(exam=exam)
        .order_by('subject')
        .values_list('subject', flat=True)
        .distinct()
    )

    return render(request, 'syllabus/tracker.html', {
        'chapters': chapter_data,
        'exam': exam,
        'subject': subject,
        'exam_choices': exam_choices,
        'subject_choices': subject_choices,
        'progress_percent': progress_percent,
        'completed_count': completed_count,
        'total_chapters': total,
    })


@login_required
@require_POST
def update_chapter_status(request):
    """AJAX endpoint to update chapter progress status."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid data'}, status=400)

    chapter_id = data.get('chapter_id')
    new_status = data.get('status')

    if not chapter_id or new_status not in dict(ChapterProgress._meta.get_field('status').choices):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    chapter = SyllabusChapter.objects.get(id=chapter_id)
    progress, created = ChapterProgress.objects.get_or_create(
        user=request.user,
        chapter=chapter,
        defaults={'status': new_status}
    )
    if not created:
        progress.status = new_status
        progress.save()

    # Calculate new progress stats for the same exam & subject
    exam = chapter.exam
    subject = chapter.subject
    
    chapters = SyllabusChapter.objects.filter(exam=exam, subject=subject)
    total_chapters = chapters.count()
    
    user_progress = ChapterProgress.objects.filter(
        user=request.user, 
        chapter__in=chapters, 
        status__in=['completed', 'revised']
    ).count()
    
    progress_percent = round((user_progress / max(total_chapters, 1)) * 100)

    return JsonResponse({
        'success': True, 
        'status': new_status,
        'completed_count': user_progress,
        'total_chapters': total_chapters,
        'progress_percent': progress_percent
    })


@login_required
def get_chapter_summary(request, chapter_id):
    """Fetch or generate a chapter summary."""
    chapter = get_object_or_404(SyllabusChapter, id=chapter_id)
    
    if not chapter.detailed_summary:
        # Generate it dynamically
        exam_type = chapter.exam
        if exam_type == 'JEE_MAIN':
            exam_type = 'JEE Mains'
        summary = generate_chapter_summary(exam_type, chapter.subject, chapter.chapter_name)
        if not summary.startswith("❌") and not summary.startswith("⚠️"):
            chapter.detailed_summary = summary
            chapter.save(update_fields=['detailed_summary'])
        else:
            return JsonResponse({'error': summary}, status=500)

    return JsonResponse({'summary': chapter.detailed_summary})
