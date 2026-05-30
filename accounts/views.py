from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import StudentProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data.get('last_name', '')
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_class=form.cleaned_data['student_class'],
                target_exam=form.cleaned_data['target_exam'],
            )
            login(request, user)
            messages.success(request, f"Swagat hai {user.first_name}! 🎉 EduAI mein aapka account ban gaya. Ab seekhna shuru karo!")
            return redirect('dashboard')
        else:
            messages.error(request, "Kuch fields mein problem hai. Neeche dekho aur fix karo.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                messages.success(request, f"Welcome back, {user.first_name or user.username}! 👋")
                return redirect(next_url)
            else:
                messages.error(request, "Galat username ya password. Dobara try karo.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Aap logout ho gaye. Jaldi wapas aana! 👋")
    return redirect('home')


@login_required
def profile_view(request):
    from .models import CLASS_CHOICES
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Update profile
        profile.student_class = request.POST.get('student_class', profile.student_class)
        profile.target_exam = request.POST.get('target_exam', profile.target_exam)
        profile.city = request.POST.get('city', profile.city)
        profile.save()

        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()

        messages.success(request, "Profile update ho gaya! ✅")
        return redirect('profile')

    from chat.models import ChatMessage
    from practice.models import TestAttempt
    from datetime import timedelta
    from django.utils import timezone

    student_class = profile.student_class

    # Calculate dynamic stats for current class
    tests_taken = TestAttempt.objects.filter(user=request.user, test__class_level=student_class, completed=True).count()
    questions_asked = ChatMessage.objects.filter(session__user=request.user, session__student_class=student_class, role='user').count()
    study_hours = round(questions_asked * 2 / 60, 1)

    # Calculate study streak
    streak = 0
    today = timezone.now().date()
    check_date = today
    for _ in range(365):
        has_activity = ChatMessage.objects.filter(
            session__user=request.user,
            session__student_class=student_class,
            created_at__date=check_date
        ).exists() or TestAttempt.objects.filter(
            user=request.user,
            test__class_level=student_class,
            started_at__date=check_date
        ).exists()

        if has_activity:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'class_choices': CLASS_CHOICES,
        'dynamic_tests_taken': tests_taken,
        'dynamic_questions_asked': questions_asked,
        'dynamic_study_hours': study_hours,
        'dynamic_study_streak': streak,
    })
