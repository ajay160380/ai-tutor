<div align="center">

# 🧠 EduAI - Next-Gen AI Education Tutor

**Revolutionizing the way you learn with Artificial Intelligence.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[**Live Demo**](https://edu-ai-ko5w.onrender.com) • [**Report Bug**](#) • [**Request Feature**](#)

</div>

---

## ⚡ Overview

**EduAI** is a state-of-the-art educational platform that leverages AI to act as a personalized virtual tutor. Designed to accelerate learning, it dynamically tracks your syllabus, generates practice tests on the fly, and offers an intelligent conversational bot to resolve your doubts 24/7. 

Whether you're a student preparing for exams or a lifelong learner, EduAI adapts to your pace and curriculum.

---

## ✨ Key Features

* 🤖 **AI-Powered Chatbot**: Instant, context-aware answers to complex academic questions.
* 📚 **Smart Syllabus Tracker**: Automatically generate, organize, and track your course progress.
* 📝 **Dynamic Practice Tests**: Get customized quizzes based on your weak points and current syllabus.
* 📊 **Interactive Dashboard**: Real-time analytics and visual insights into your learning journey.
* 🔐 **Secure & Scalable**: Robust user authentication and session management built on modern standards.

---

## 🛠️ Technology Stack

| Category         | Technologies Used                                                                 |
| ---------------- | --------------------------------------------------------------------------------- |
| **Backend**      | Python, Django, Gunicorn                                                          |
| **Database**     | PostgreSQL (Production), SQLite (Development)                                     |
| **Frontend**     | HTML5, CSS3, JavaScript (Django Templates), Bootstrap/Tailwind (if applicable)    |
| **Deployment**   | Render, Whitenoise (Static File Serving)                                          |
| **Version Ctrl** | Git, GitHub                                                                       |

---

## 🚀 Quick Start Guide

Want to run EduAI on your local machine? Follow these steps to get a development environment up and running in minutes.

### Prerequisites
* Python 3.10+
* Git
* pip (Python package manager)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ajay160380/ai-tutor.git
cd eduai_project
```

### 2️⃣ Virtual Environment Setup
It is recommended to use a virtual environment to manage dependencies.
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration
Create a `.env` file from the provided example template and configure your secrets (Database URL, Secret Key, API Keys, etc.).
```bash
cp .env.example .env
```

### 5️⃣ Database Migration
Apply all database schema changes.
```bash
python manage.py migrate
```

### 6️⃣ Launch the Application!
Start the Django development server.
```bash
python manage.py runserver
```
🎉 Your app should now be running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <b>Built with ❤️ by <a href="https://github.com/ajay160380">Ajay Vishwakarma</a></b>
</div>
