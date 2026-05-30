from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import PracticeTest, Question, TestAttempt


@login_required
def test_list_view(request):
    profile = getattr(request.user, 'profile', None)
    target_exam = profile.target_exam if profile else 'JEE'
    
    if target_exam == 'JEE':
        test_types = ['JEE_MAIN', 'JEE_ADV', 'CUSTOM']
    elif target_exam == 'NEET':
        test_types = ['NEET', 'CUSTOM']
    else:
        test_types = ['BOARD', 'CUSTOM']

    student_class = profile.student_class if profile else '10'

    tests = PracticeTest.objects.filter(is_active=True, test_type__in=test_types, class_level=student_class).order_by('-created_at')
    past_attempts = TestAttempt.objects.filter(user=request.user, test__class_level=student_class, completed=True).select_related('test').order_by('-completed_at')[:10]
    in_progress_attempts = TestAttempt.objects.filter(user=request.user, test__class_level=student_class, completed=False).select_related('test').order_by('-started_at')

    return render(request, 'practice/test_list.html', {
        'tests': tests,
        'past_attempts': past_attempts,
        'in_progress_attempts': in_progress_attempts,
    })


@login_required
def take_test_view(request, test_id):
    """Take a practice test — displays questions and handles submission."""
    test = get_object_or_404(PracticeTest, id=test_id, is_active=True)
    questions = test.questions.all()

    if not questions.exists():
        # Generic tests might not have questions seeded. We don't want generic math questions everywhere!
        pass

    # Check for in-progress attempt
    attempt = TestAttempt.objects.filter(user=request.user, test=test, completed=False).first()
    if not attempt:
        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            total_marks=test.total_marks,
        )

    questions_data = []
    for q in questions:
        questions_data.append({
            'id': q.id,
            'number': q.question_number,
            'text': q.question_text,
            'options': {
                'A': q.option_a,
                'B': q.option_b,
                'C': q.option_c,
                'D': q.option_d,
            },
            'subject': q.subject,
            'topic': q.topic,
        })

    return render(request, 'practice/take_test.html', {
        'test': test,
        'questions': json.dumps(questions_data),
        'attempt': attempt,
        'duration_seconds': test.duration_minutes * 60,
    })


@login_required
@require_POST
def submit_test(request, attempt_id):
    """Submit test answers and calculate score."""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)

    if attempt.completed:
        return redirect('test_result', attempt_id=attempt.id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid data'}, status=400)

    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)

    test = attempt.test
    questions = test.questions.all()

    correct = 0
    wrong = 0
    unanswered = 0
    score = 0

    for q in questions:
        q_id = str(q.id)
        if q_id in answers and answers[q_id]:
            # Normalize correct answer in case AI returned 'c' or 'Option C'
            db_correct = str(q.correct_answer).strip().upper()
            if db_correct.startswith('OPTION '):
                db_correct = db_correct.replace('OPTION ', '')
            if len(db_correct) > 1 and db_correct[0] in ['A', 'B', 'C', 'D']:
                db_correct = db_correct[0]
                
            user_ans = str(answers[q_id]).strip().upper()
            
            if user_ans == db_correct:
                correct += 1
                score += q.marks
            else:
                wrong += 1
                score -= test.negative_marking
        else:
            unanswered += 1

    attempt.answers = answers
    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.unanswered = unanswered
    attempt.score = max(0, score)
    attempt.time_taken_seconds = time_taken
    attempt.completed = True
    attempt.completed_at = timezone.now()
    attempt.save()

    # Update profile stats
    if hasattr(request.user, 'profile'):
        request.user.profile.total_tests_taken += 1
        request.user.profile.save(update_fields=['total_tests_taken'])

    return JsonResponse({
        'success': True,
        'attempt_id': attempt.id,
        'redirect': f'/tests/result/{attempt.id}/'
    })


@login_required
def test_result_view(request, attempt_id):
    """Show test results."""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user, completed=True)
    test = attempt.test
    questions = test.questions.all()

    # Build detailed results
    results = []
    for q in questions:
        q_id = str(q.id)
        selected = attempt.answers.get(q_id, '')
        
        db_correct = str(q.correct_answer).strip().upper()
        if db_correct.startswith('OPTION '):
            db_correct = db_correct.replace('OPTION ', '')
        if len(db_correct) > 1 and db_correct[0] in ['A', 'B', 'C', 'D']:
            db_correct = db_correct[0]
            
        user_ans = str(selected).strip().upper()
        
        results.append({
            'number': q.question_number,
            'text': q.question_text,
            'options': {'A': q.option_a, 'B': q.option_b, 'C': q.option_c, 'D': q.option_d},
            'correct': db_correct,
            'selected': selected,
            'is_correct': user_ans == db_correct if selected else False,
            'explanation': q.explanation,
            'subject': q.subject,
        })

    accuracy = round((attempt.correct_answers / max(len(questions), 1)) * 100, 1)
    time_min = attempt.time_taken_seconds // 60
    time_sec = attempt.time_taken_seconds % 60

    return render(request, 'practice/result.html', {
        'attempt': attempt,
        'test': test,
        'results': results,
        'accuracy': accuracy,
        'time_display': f"{time_min}m {time_sec}s",
        'total_questions': len(questions),
    })


def _generate_sample_questions(test, chapter_name=None, class_level="10"):
    """Generate questions. If chapter_name is provided, use AI to generate custom questions."""
    from chat.services import generate_practice_questions
    
    if chapter_name:
        # Try to use AI to generate real questions for this chapter
        ai_questions = generate_practice_questions(test.subject, chapter_name, class_level, count=test.total_questions)
        if ai_questions:
            for i, q in enumerate(ai_questions, 1):
                Question.objects.create(
                    test=test,
                    question_number=i,
                    question_text=q.get('question', 'Missing question text'),
                    option_a=q.get('options', {}).get('A', 'Option A'),
                    option_b=q.get('options', {}).get('B', 'Option B'),
                    option_c=q.get('options', {}).get('C', 'Option C'),
                    option_d=q.get('options', {}).get('D', 'Option D'),
                    correct_answer=q.get('correct', 'A'),
                    explanation=q.get('explanation', ''),
                    subject=test.subject,
                    topic=chapter_name,
                )
            return

    # Fallback to hardcoded mock questions if AI fails or if no chapter specified
    sample_questions = [
        {
            'text': 'If f(x) = x² + 3x + 2, then f(2) is equal to:',
            'a': '8', 'b': '10', 'c': '12', 'd': '14',
            'correct': 'C', 'subject': 'Mathematics', 'topic': 'Functions',
            'explanation': 'f(2) = 4 + 6 + 2 = 12. Seedha value put karo x = 2.'
        },
        {
            'text': 'The SI unit of force is:',
            'a': 'Joule', 'b': 'Newton', 'c': 'Watt', 'd': 'Pascal',
            'correct': 'B', 'subject': 'Physics', 'topic': 'Units & Dimensions',
            'explanation': 'Force ka SI unit Newton (N) hai. F = ma, toh kg⋅m/s² = Newton.'
        },
        {
            'text': 'Which of the following is a noble gas?',
            'a': 'Nitrogen', 'b': 'Oxygen', 'c': 'Argon', 'd': 'Chlorine',
            'correct': 'C', 'subject': 'Chemistry', 'topic': 'Periodic Table',
            'explanation': 'Argon (Ar) ek noble gas hai Group 18 mein. Inert gases completely filled electron shells rakhte hain.'
        },
        {
            'text': 'The derivative of sin(x) is:',
            'a': '-cos(x)', 'b': 'cos(x)', 'c': 'tan(x)', 'd': '-sin(x)',
            'correct': 'B', 'subject': 'Mathematics', 'topic': 'Calculus',
            'explanation': 'd/dx [sin(x)] = cos(x). Yeh basic differentiation formula hai.'
        },
        {
            'text': 'Newton\'s second law of motion states that:',
            'a': 'Every action has an equal and opposite reaction',
            'b': 'Force is equal to mass times acceleration',
            'c': 'An object at rest stays at rest',
            'd': 'Energy is conserved',
            'correct': 'B', 'subject': 'Physics', 'topic': 'Laws of Motion',
            'explanation': 'F = ma — Newton ka second law. Force mass aur acceleration ka product hai.'
        },
        {
            'text': 'The pH of pure water at 25°C is:',
            'a': '0', 'b': '1', 'c': '7', 'd': '14',
            'correct': 'C', 'subject': 'Chemistry', 'topic': 'Ionic Equilibrium',
            'explanation': 'Pure water neutral hai, pH = 7. [H⁺] = [OH⁻] = 10⁻⁷ M.'
        },
        {
            'text': 'The integral of 1/x dx is:',
            'a': 'x²', 'b': 'ln|x| + C', 'c': '1/x²', 'd': 'e^x',
            'correct': 'B', 'subject': 'Mathematics', 'topic': 'Integration',
            'explanation': '∫(1/x)dx = ln|x| + C. Standard integration formula.'
        },
        {
            'text': 'Which organelle is called the "powerhouse of the cell"?',
            'a': 'Nucleus', 'b': 'Ribosome', 'c': 'Mitochondria', 'd': 'Golgi body',
            'correct': 'C', 'subject': 'Biology', 'topic': 'Cell Biology',
            'explanation': 'Mitochondria ko "powerhouse" kehte hain kyunki yeh ATP produce karta hai — cell ka energy currency.'
        },
        {
            'text': 'The acceleration due to gravity on earth is approximately:',
            'a': '9.8 m/s²', 'b': '10.8 m/s²', 'c': '8.8 m/s²', 'd': '11 m/s²',
            'correct': 'A', 'subject': 'Physics', 'topic': 'Gravitation',
            'explanation': 'g ≈ 9.8 m/s² (approximate value 10 m/s² bhi use hota hai numericals mein).'
        },
        {
            'text': 'Benzene ka molecular formula kya hai?',
            'a': 'C₅H₆', 'b': 'C₆H₆', 'c': 'C₆H₁₂', 'd': 'C₇H₈',
            'correct': 'B', 'subject': 'Chemistry', 'topic': 'Organic Chemistry',
            'explanation': 'Benzene = C₆H₆. 6 carbon atoms ka hexagonal ring structure hai.'
        },
    ]

    for i, q in enumerate(sample_questions[:test.total_questions], 1):
        Question.objects.create(
            test=test,
            question_number=i,
            question_text=q['text'],
            option_a=q['a'],
            option_b=q['b'],
            option_c=q['c'],
            option_d=q['d'],
            correct_answer=q['correct'],
            explanation=q.get('explanation', ''),
            subject=q.get('subject', 'General'),
            topic=q.get('topic', ''),
        )


@login_required
def create_chapter_test(request, chapter_id):
    """Creates a custom mock test for a specific chapter and redirects to it."""
    from syllabus.models import SyllabusChapter
    chapter = get_object_or_404(SyllabusChapter, id=chapter_id)
    
    # See if a custom test for this chapter already exists for this user
    # Actually, let's just create a shared one or find an existing one by title
    student_class = request.user.profile.student_class if hasattr(request.user, 'profile') else '10'
    test_title = f"{chapter.subject} - {chapter.chapter_name} Test"
    test, created = PracticeTest.objects.get_or_create(
        title=test_title,
        test_type='CUSTOM',
        class_level=student_class,
        defaults={
            'subject': chapter.subject,
            'total_questions': 5,
            'duration_minutes': 5,
            'total_marks': 20,
            'negative_marking': 0.0,
        }
    )
    
    # If the test was just created, generate the questions
    if created or test.questions.count() == 0:
        _generate_sample_questions(test, chapter_name=chapter.chapter_name, class_level=student_class)
    
    return redirect('take_test', test_id=test.id)
