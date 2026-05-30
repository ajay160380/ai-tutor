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
            {'icon': 'bi-clock-history', 'title': '24/7 Available', 'desc': 'Kabhi bhi doubt poocho, raat ho ya din. AI hamesha ready hai tumhare liye.'},
            {'icon': 'bi-mortarboard', 'title': 'JEE + NEET Ready', 'desc': 'Chapter-wise prep with weightage aur shortcuts. Exam pattern ke hisaab se.'},
            {'icon': 'bi-translate', 'title': 'Hinglish Support', 'desc': 'Hindi ya English, jisme comfortable ho waise poocho. AI dono samajhta hai.'},
            {'icon': 'bi-list-ol', 'title': 'Step-by-Step Solutions', 'desc': 'Koi step skip nahi, poora reasoning milega har ek step pe.'},
            {'icon': 'bi-clipboard-check', 'title': 'Mock Tests', 'desc': 'JEE/NEET pattern mein practice karo — negative marking ke saath.'},
            {'icon': 'bi-graph-up', 'title': 'Performance Analytics', 'desc': 'Har din apni weak points track karo aur improve karo.'},
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
                'text': 'JEE mein 98 percentile aaya! EduAI ne Physics ka dar khatam kar diya. Rotational motion ab mera favourite topic hai.',
                'improvement': '+53%'
            },
            {
                'name': 'Priya Singh', 'class_name': 'NEET 2024', 'city': 'Lucknow',
                'text': 'Organic Chemistry ab mushkil nahi lagti. Ek ek reaction mechanism itna clearly explain karta hai ki sab yaad reh jaata hai.',
                'improvement': '+41%'
            },
            {
                'name': 'Amit Kumar', 'class_name': 'Class 9', 'city': 'Patna',
                'text': 'Maths mein 45 se 87 ho gaye marks sirf 2 mahine mein! Ab mujhe algebra se pyaar ho gaya hai. Thank you EduAI!',
                'improvement': '+42%'
            },
            {
                'name': 'Sneha Patel', 'class_name': 'Class 11', 'city': 'Ahmedabad',
                'text': 'Ghar se JEE ki preparation possible hai, EduAI ne prove kar diya. Coaching ki zaroorat nahi padi!',
                'improvement': '+38%'
            },
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
                'q': 'Kya EduAI JEE Advanced ke liye bhi kaam karta hai?',
                'a': 'Haan bilkul! EduAI JEE Advanced ke sare chapters cover karta hai including Integer type, matrix match, aur comprehension based questions. Advanced level problems ke step-by-step solutions milte hain.'
            },
            {
                'q': 'Kya Hindi mein puch sakte hain?',
                'a': 'Zaroor! Aap Hinglish (Hindi + English mix) ya pure Hindi mein bhi puch sakte ho. AI dono samajhta hai aur usi bhasha mein jawab deta hai jisme tum puchte ho.'
            },
            {
                'q': 'Free plan mein kitna milega?',
                'a': 'Free plan mein roz 20 AI questions puch sakte ho. Basic subjects available hain aur 7 din ki chat history save hoti hai. Upgrade karo Pro plan ke liye unlimited access.'
            },
            {
                'q': 'Mock tests mein negative marking hoti hai?',
                'a': 'Haan, JEE pattern ke mock tests mein -1 marking hai galat MCQ ke liye, bilkul real exam jaisa. NEET mein bhi same pattern follow hota hai.'
            },
            {
                'q': 'Kya ek account se multiple students use kar sakte hain?',
                'a': 'Nahi, ek account ek student ke liye hota hai. Isse progress tracking accurate rehta hai aur AI tumhari strengths aur weaknesses ko properly samajh paata hai.'
            },
            {
                'q': 'Refund policy kya hai?',
                'a': '7 din ka money-back guarantee hai Pro aur Premium plans ke liye. Agar koi bhi reason se satisfy nahi ho, toh poora paisa wapas mil jayega, koi sawaal nahi poochha jayega.'
            },
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
