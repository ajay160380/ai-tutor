"""
EduAI — Groq API Service
AI tutoring integration using Groq cloud (llama-3.3-70b-versatile)
"""
import requests
import json
import re
from django.conf import settings


SYSTEM_PROMPT_TEMPLATE = """You are "Vidya-AI", an elite, highly advanced Academic Tutor specifically engineered for Indian students. You combine the deep subject matter expertise of top-tier coaching faculty (Kota/Hyderabad standard) with the patience and clarity of a world-class educator.

## 🎯 CURRENT STUDENT PROFILE:
- Class Level: {class_level}
- Subject: {subject}
- Chapter Name: {chapter_name}
- Target Goal / Exam: {exam_type}

## 🛑 CORE DIRECTIVES & STRICT CONSTRAINTS (MANDATORY):
1. NO HALLUCINATIONS: Confine all concepts, examples, and questions strictly to the bounds of "{chapter_name}". Do not bring in advanced topics unless explicitly required by the {exam_type} syllabus for this specific chapter.
2. TONE & EMPATHY: Be encouraging but rigorous. Use analogies that resonate with Indian students (e.g., local geography, daily life) where appropriate to explain complex concepts.
3. SYLLABUS ALIGNMENT: Strictly adhere to the latest NCERT syllabus as the baseline, scaling up based on the {exam_type}.

## 📈 ADAPTIVE DIFFICULTY CALIBRATION:
You MUST adapt your rigor, depth, and question complexity exactly to the `{exam_type}`:

- If `{exam_type}` is "JEE (Mains/Advanced)":
  - Content: Emphasize edge-case formulas, exceptions, and multi-concept integration.
  - Questions: Generate highly complex, numerical-heavy problems. Include multiple-correct, integer-type, and paragraph-type questions. 
  - Ban: NO basic definition-level or direct formula-plugging questions.

- If `{exam_type}` is "NEET":
  - Content: Focus heavily on NCERT deep-cuts, especially hidden lines in Biology/Chemistry. Emphasize speed, accuracy, and typical examiner traps.
  - Questions: Tricky, conceptual, statement-based (Assertion-Reason), and match-the-following questions. Tricky options designed to test superficial reading.

- If `{exam_type}` is "School Board":
  - Content: Focus on standard NCERT progression, standard derivations, and definitions.
  - Questions: A mix of 1-mark objective, 3-mark short answer, and 5-mark long answer/derivation questions. 

## 📝 OUTPUT STRUCTURE:
Generate your response using the exact structure below, utilizing clean Markdown, clear headings, and bold text for emphasis. Do not deviate from this structure.

### 1️⃣ IN-DEPTH CHAPTER MASTERCLASS ("{chapter_name}")
* **The "Why":** A 2-sentence hook explaining why this chapter is important in real life and its weightage in the {exam_type}.
* **Core Concepts Explained:** Break down the chapter. Use simple analogies before introducing complex terminology.
* **Formula / Reaction Cheat Sheet:** A consolidated, beautifully formatted list of every critical formula, chemical reaction, or key definition. 
* **Examiner's Favorite Targets (High-Weightage):** Explicitly list the sub-topics from this chapter that are most frequently asked in the {exam_type}.

### 2️⃣ THE {exam_type} CHALLENGE: PRACTICE ARENA
*Generate 5 to 7 highly curated, premium quality questions. Ensure the difficulty perfectly matches {exam_type}.*
* (Format each question clearly. If MCQ, ensure options A, B, C, D are highly plausible to test true understanding.)

### 3️⃣ DETAILED SOLUTIONS & THOUGHT PROCESS
*For every question above, provide:*
* **Correct Answer:** 
* **The "Trap":** What mistake do 80% of students make on this specific question?
* **Step-by-Step Solution:** A clear, logical breakdown of how to arrive at the answer, including any shortcuts or elimination techniques specific to {exam_type} (e.g., dimensional analysis, extreme values)."""


def get_ai_response(messages_history, subject="General", user=None, topic="Requested Topic"):
    """
    Call Groq API and return full response text.
    messages_history: list of {'role': 'user'/'assistant', 'content': '...'} dicts
    """
    api_key = settings.GROK_API_KEY
    if not api_key:
        return "⚠️ API key configure nahi hai. Admin se contact karo ya .env file mein GROK_API_KEY set karo."

    class_level = "11"
    exam_type = "School Board"
    
    if user and hasattr(user, 'profile'):
        class_level = user.profile.student_class
        exam_type = user.profile.target_exam

    system_msg = SYSTEM_PROMPT_TEMPLATE.format(
        class_level=class_level,
        subject=subject,
        chapter_name=topic,
        exam_type=exam_type
    )

    if subject.lower() == "hindi":
        system_msg += "\n\nCRITICAL LANGUAGE OVERRIDE: You MUST write the ENTIRE response in pure Hindi language using the Devanagari script. Do not use English."

    payload = {
        "model": settings.GROK_MODEL,
        "messages": [{"role": "system", "content": system_msg}] + messages_history,
        "max_tokens": 1500,
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(
            settings.GROK_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

    except requests.exceptions.Timeout:
        return "⏳ Thoda slow ho gaya AI. Please dobara try karo! Internet speed bhi check kar lena. 🙏"
    except requests.exceptions.ConnectionError:
        return "🌐 Internet connection check karo aur dobara try karo. Agar WiFi pe ho toh ek baar reconnect karo."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "⚠️ Bahut zyada requests ho gayi. Thoda wait karo (1-2 minute) aur phir try karo."
        elif e.response.status_code == 401:
            return "🔑 API key invalid hai. Admin se contact karo."
        return f"❌ Server error aaya (Status: {e.response.status_code}). Thodi der mein try karo."
    except Exception as e:
        return f"❌ Kuch technical problem aa gayi: {str(e)}"


def generate_practice_questions(subject, topic, class_level, count=3):
    """Generate MCQ practice questions for a topic using AI."""
    api_key = settings.GROK_API_KEY
    if not api_key:
        return []

    language_instruction = "standard English language"
    if subject.lower() == "hindi":
        language_instruction = "pure Hindi language (Devanagari script) for EVERYTHING including questions, options, and explanations"

    prompt = f"""Generate exactly {count} multiple choice questions for:
Subject: {subject}
Topic: {topic}
Level: Class {class_level} Board Exams

STRICT INSTRUCTIONS FOR DIFFICULTY & FORMATTING:
1. Make the questions EXTREMELY TOUGH (HOTS - Higher Order Thinking Skills). Target the hardest 10% of Board Exam questions.
2. DO NOT ask simple or direct questions. Every question MUST involve multi-step reasoning, tricky application of concepts, or be an Assertion-Reason / Statement-based question.
3. The options MUST be highly confusing and plausible (common student misconceptions).
4. The 'explanation' must break down the exact trap that students fall into and then give the real answer.
5. LANGUAGE CRITICAL: You must use {language_instruction}. Do not use Hinglish.
6. FORMATTING: Use <b> or <strong> tags to highlight important keywords, concepts, or numbers in the questions and explanations to make them easy to read!

Format your response as a valid JSON array ONLY (no extra text, no markdown):
[
  {{
    "question": "<b>Tough</b> conceptual question text here?",
    "options": {{"A": "plausible option 1", "B": "plausible option 2", "C": "correct option", "D": "plausible option 4"}},
    "correct": "C",
    "explanation": "Detailed <b>step-by-step</b> explanation explaining the trick/concept in {language_instruction}."
  }}
]"""

    try:
        response = requests.post(
            settings.GROK_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.GROK_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000,
                "temperature": 0.5,
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        text = data['choices'][0]['message']['content']

        # Extract JSON from response
        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    return []


def generate_chapter_summary(exam_type, subject, chapter_name):
    """Generate a detailed chapter masterclass summary using AI."""
    api_key = settings.GROK_API_KEY
    if not api_key:
        return "⚠️ API key is not configured."

    # For summaries, we assume standard Class 11/12 level as default, 
    # but the exam_type dictates the depth based on the system prompt.
    system_msg = SYSTEM_PROMPT_TEMPLATE.format(
        class_level="11-12",
        subject=subject,
        chapter_name=chapter_name,
        exam_type=exam_type
    )

    if subject.lower() == "hindi":
        system_msg += "\n\nCRITICAL LANGUAGE OVERRIDE: You MUST write the ENTIRE response in pure Hindi language using the Devanagari script. Do not use English."

    prompt = f"Please provide the detailed chapter masterclass for {chapter_name} ({subject}) focusing on {exam_type}."

    payload = {
        "model": settings.GROK_MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.5,
    }

    try:
        response = requests.post(
            settings.GROK_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=40
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Failed to generate summary: {str(e)}"
