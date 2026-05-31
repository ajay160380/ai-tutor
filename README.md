# EduAI - Your AI-Powered Education Tutor

Welcome to the **EduAI** repository! EduAI is an advanced educational platform powered by Artificial Intelligence, built with Django.

## 🌐 Live Demo
Check out the live application here: **[EduAI Live App](https://edu-ai-ko5w.onrender.com)**

---

## 🚀 Features
- **AI Chatbot**: Intelligent virtual tutor to help with your studies.
- **Syllabus Generation & Tracking**: Automatically create and manage your course syllabus.
- **Practice Tests**: Enhance your learning with dynamically generated practice tests.
- **User Dashboard**: Track your progress, manage your profile, and see your stats all in one place.
- **Secure Authentication**: Robust user account management and login system.

---

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL / SQLite (for local development)
- **Server**: Gunicorn, Whitenoise (for static files)
- **Frontend**: HTML, CSS, JavaScript (Django Templates)

---

## ⚙️ Local Development Setup

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/ajay160380/ai-tutor.git
cd eduai_project
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the example environment file and fill in your details:
```bash
cp .env.example .env
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
The app will now be available at `http://127.0.0.1:8000/`.

---

## 📝 License
This project is licensed under the MIT License.
