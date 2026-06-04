from django.shortcuts import render


def home(request):
    """Homepage with all landing page sections."""
    context = {
        'stats': [
            {'number': '50,000+', 'label': 'Students'},
            {'number': '10 Lakh+', 'label': 'Doubts Solved'},
            {'number': '95%', 'label': 'Score Improvement'},
            {'number': '4.9/5', 'label': 'Rating'},
        ],
        'features': [
            {'icon': 'bi-robot', 'title': 'Smart AI Tutor', 'desc': 'Get step-by-step solutions for Maths, Physics, Chemistry & Biology. No more getting stuck!'},
            {'icon': 'bi-clock-history', 'title': '24/7 Available', 'desc': 'Ask doubts anytime, day or night. AI is always ready for you.'},
            {'icon': 'bi-translate', 'title': 'Hinglish Support', 'desc': 'Don\'t understand pure English? No problem! Ask in Hindi or Hinglish.'},
            {'icon': 'bi-journal-check', 'title': 'Syllabus Aligned', 'desc': 'Strictly mapped to CBSE, ICSE, and State Board curriculums.'},
            {'icon': 'bi-clipboard-check', 'title': 'Mock Tests', 'desc': 'Practice in JEE/NEET pattern — with negative marking.'},
            {'icon': 'bi-graph-up', 'title': 'Performance Analytics', 'desc': 'Track your weak points daily and improve.'},
        ],
        'subjects': [
            {'name': 'Mathematics', 'icon': 'bi-calculator', 'topics': 120, 'color': '#FF6B35'},
            {'name': 'Physics', 'icon': 'bi-lightning-fill', 'topics': 95, 'color': '#1A237E'},
            {'name': 'Chemistry', 'icon': 'bi-droplet-fill', 'topics': 110, 'color': '#00C853'},
            {'name': 'Biology', 'icon': 'bi-flower1', 'topics': 130, 'color': '#E91E63'},
            {'name': 'Science', 'icon': 'bi-globe2', 'topics': 80, 'color': '#FF9800'},
            {'name': 'Social Studies', 'icon': 'bi-book-fill', 'topics': 60, 'color': '#9C27B0'},
        ],
        'testimonials': [
            {
                'name': 'Rahul Sharma', 'class_name': 'JEE 2024', 'city': 'Delhi',
                'text': 'Got 98 percentile in JEE! EduAI ended my fear of Physics. Rotational motion is now my favorite topic.',
                'improvement': '+53%'
            },
            {
                'name': 'Priya Singh', 'class_name': 'NEET 2024', 'city': 'Lucknow',
                'text': 'Organic Chemistry is no longer difficult. It explains every reaction mechanism so clearly that I remember everything.',
                'improvement': '+41%'
            },
            {
                'name': 'Amit Kumar', 'class_name': 'Class 9', 'city': 'Patna',
                'text': 'Marks in Maths went from 45 to 87 in just 2 months! I am in love with algebra now. Thank you EduAI!',
                'improvement': '+42%'
            },
            {
                'name': 'Sneha Patel', 'class_name': 'Class 11', 'city': 'Ahmedabad',
                'text': 'EduAI proved that JEE preparation from home is possible. I didn\'t need coaching!',
                'improvement': '+38%'
            }
        ],
        'plans': [
            {
                'name': 'Free', 'price': '0', 'period': 'forever',
                'features': ['20 AI questions/day', 'Basic subjects only', 'Chat history (7 days)', 'No mock tests', 'Community support'],
                'cta': 'Start Free', 'highlighted': False
            },
            {
                'name': 'Pro', 'price': '299', 'period': 'month',
                'features': ['Unlimited AI questions', 'All subjects + JEE/NEET', 'Full chat history', '10 Mock tests/month', 'Performance analytics', 'Formula sheets', 'Priority support'],
                'cta': 'Start Pro', 'highlighted': True
            },
            {
                'name': 'Premium', 'price': '599', 'period': 'month',
                'features': ['Everything in Pro', 'Doubt camera (image upload)', 'Priority AI response', 'Unlimited mock tests', 'Offline notes download', 'Personal study planner', '1-on-1 mentorship'],
                'cta': 'Go Premium', 'highlighted': False
            },
        ],
        'faqs': [
            {
                'q': 'Is EduAI suitable for JEE/NEET preparation?',
                'a': 'Yes absolutely! EduAI covers all JEE Advanced chapters including Integer type, matrix match, and comprehension based questions. Step-by-step solutions for advanced level problems are provided.'
            },
            {
                'q': 'Can I ask in Hindi?',
                'a': 'Sure! You can ask in Hinglish (Hindi + English mix) or pure Hindi. The AI understands both and replies in the language you ask.'
            },
            {
                'q': 'What is included in the free plan?',
                'a': 'In the free plan, you can ask 20 AI questions daily. Basic subjects are available and 7 days of chat history is saved. Upgrade to Pro plan for unlimited access.'
            },
            {
                'q': 'Is there negative marking in mock tests?',
                'a': 'Yes, JEE pattern mock tests have -1 marking for incorrect MCQs, just like the real exam. NEET also follows the same pattern.'
            },
            {
                'q': 'Can I share my account with my sibling?',
                'a': 'No, one account is for one student. This keeps progress tracking accurate and allows the AI to properly understand your strengths and weaknesses.'
            },
            {
                'q': 'What is the refund policy?',
                'a': 'There is a 7-day money-back guarantee for Pro and Premium plans. If you are not satisfied for any reason, you will get a full refund, no questions asked.'
            }
        ]
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page."""
    return render(request, 'core/about.html')


def pricing(request):
    """Pricing page (redirects to home pricing section)."""
    return render(request, 'core/pricing.html')


def blog(request):
    return render(request, 'core/blog.html')

def careers(request):
    return render(request, 'core/careers.html')

def contact(request):
    return render(request, 'core/contact.html')

def press_kit(request):
    return render(request, 'core/press_kit.html')

def privacy_policy(request):
    return render(request, 'core/privacy.html')

def terms_of_service(request):
    return render(request, 'core/terms.html')

def refund_policy(request):
    return render(request, 'core/refund.html')
