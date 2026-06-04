from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import ChatSession, ChatMessage
from .services import get_ai_response


@login_required
def chat_view(request):
    """Main chat page."""
    student_class = request.user.profile.student_class if hasattr(request.user, 'profile') else '10'
    subject = request.GET.get('subject', 'General')
    sessions = ChatSession.objects.filter(user=request.user, student_class=student_class)[:15]

    session_id = request.GET.get('session')
    current_session = None
    messages_list = []

    if session_id:
        try:
            current_session = ChatSession.objects.get(id=session_id, user=request.user)
            messages_list = list(current_session.messages.all())
        except ChatSession.DoesNotExist:
            pass

    # Import SyllabusChapter to get the subjects dynamically
    from syllabus.models import SyllabusChapter
    my_subjects = list(
        SyllabusChapter.objects.filter(exam=f'BOARD_{student_class}')
        .order_by('subject')
        .values_list('subject', flat=True)
        .distinct()
    )
    if not my_subjects:
        my_subjects = ['Mathematics', 'Science', 'English', 'Social Science', 'Hindi']

    # Dynamic quick topics based on class level and selected subject
    try:
        class_num = int(student_class)
    except:
        class_num = 10

    quick_topics = []

    if subject == 'Mathematics':
        if class_num <= 8:
            quick_topics = ["How to solve fractions?", "Teach me how to find LCM and HCF", "Area of circle formula", "Algebraic expressions basics"]
        elif class_num <= 10:
            quick_topics = ["Solve quadratic equations", "Trick to remember trigonometry table", "Surface area and volumes formulas", "Polynomials division"]
        else:
            quick_topics = ["Matrix multiplication trick", "Integration by parts sikhao", "Derivatives of trigonometric functions", "Probability Bayes Theorem"]
            
    elif subject == 'Science':
        if class_num <= 8:
            quick_topics = ["What is photosynthesis?", "Tell me about the solar system", "Explain the water cycle", "Explain types of forces"]
        else:
            quick_topics = ["Explain light reflection & refraction", "Life processes short notes", "Teach how to balance chemical reactions", "Carbon and its compounds"]
            
    if subject == 'Physics':
        quick_topics = ["Explain Newton's laws", "Important derivations for physics", "Kinematics equations", "Thermodynamics laws"]
    elif subject == 'Chemistry':
        quick_topics = ["Organic chemistry basics", "Explain chemical bonding", "Periodic table trends", "Explain equilibrium constant"]
    elif subject == 'Biology':
        quick_topics = ["Cell biology short notes", "Human heart structure", "Genetics mendel laws", "Human reproduction overview"]
        
    elif subject == 'Social Science' or subject == 'Environmental Studies':
        if class_num <= 8:
            quick_topics = ["Mughal empire short summary", "Continents and Oceans", "What is democracy?", "Indian Constitution features"]
        else:
            quick_topics = ["Nationalism in India summary", "French Revolution causes", "Sectors of Indian Economy", "Federalism in India"]
            
    elif subject == 'English':
        quick_topics = ["Explain parts of speech", "Letter writing format", "Active and passive voice rules", "Direct and indirect speech trick"]
    elif subject == 'Hindi':
        quick_topics = ["Teach me Sandhi vichhed", "Tell me the types of Samas", "Patra lekhan format", "How to identify Alankar?"]
        
    elif subject in ['Accountancy', 'Economics', 'Business Studies']:
        if subject == 'Accountancy':
            quick_topics = ["Accounting principles samjhao", "Cash flow statement basics", "Partnership firm rules", "Journal entries examples"]
        elif subject == 'Economics':
            quick_topics = ["Explain Demand and Supply curve", "Microeconomics vs Macroeconomics", "National Income calculation", "Banking system in India"]
        else:
            quick_topics = ["Business environment case studies", "Principles of management", "Marketing mix 4Ps", "Financial markets"]

    # Fallback if General or subject not specifically mapped
    if not quick_topics:
        if class_num <= 8:
            quick_topics = ["How to solve fractions?", "What is photosynthesis?", "Explain parts of speech", "Tell me about the solar system"]
        elif class_num <= 10:
            quick_topics = ["Solve quadratic equations", "Explain light reflection & refraction", "Nationalism in India summary", "Balance chemical reactions"]
        elif 'Commerce' in my_subjects or 'Accountancy' in my_subjects:
            quick_topics = ["Explain accounting principles", "Demand and Supply curve", "Business environment case studies", "Cash flow statement basics"]
        else:
            quick_topics = ["Explain Newton's laws", "Organic chemistry basics", "Teach integration by parts", "Cell biology short notes"]

    return render(request, 'chat/chat.html', {
        'sessions': sessions,
        'current_session': current_session,
        'messages': messages_list,
        'subject': subject,
        'my_subjects': my_subjects,
        'quick_topics': quick_topics,
    })


@login_required
@require_POST
def send_message(request):
    """Handle AJAX message send and return AI response."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_message = data.get('message', '').strip()
    session_id = data.get('session_id')
    subject = data.get('subject', 'General')

    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)

    # Get or create session
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
    else:
        title = user_message[:60] + ('...' if len(user_message) > 60 else '')
        student_class = request.user.profile.student_class if hasattr(request.user, 'profile') else '10'
        session = ChatSession.objects.create(
            user=request.user,
            title=title,
            subject=subject,
            student_class=student_class
        )

    # Save user message
    ChatMessage.objects.create(session=session, role='user', content=user_message)

    # Build message history for API (last 20 messages for context window)
    history = []
    for msg in session.messages.all().order_by('created_at')[:20]:
        history.append({'role': msg.role, 'content': msg.content})

    # Get AI response
    topic_name = session.title if session.title else "Current Topic"
    ai_response = get_ai_response(history, subject, request.user, topic_name)

    # Save AI response
    ChatMessage.objects.create(session=session, role='assistant', content=ai_response)

    # Update user stats
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        profile.total_questions_asked += 1
        profile.save(update_fields=['total_questions_asked'])

    return JsonResponse({
        'response': ai_response,
        'session_id': session.id,
        'session_title': session.title
    })


@login_required
def new_session(request):
    """Create a new chat session."""
    subject = request.GET.get('subject', 'General')
    return redirect(f'/chat/?subject={subject}')


@login_required
def delete_session(request, session_id):
    """Delete a chat session."""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    return redirect('chat')


@login_required
def chat_history(request):
    """View all chat sessions."""
    student_class = request.user.profile.student_class if hasattr(request.user, 'profile') else '10'
    sessions = ChatSession.objects.filter(user=request.user, student_class=student_class)
    return render(request, 'chat/history.html', {'sessions': sessions})
