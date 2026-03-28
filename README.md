# 🎓 Context-Aware Collaborative Learning Platform
**Vashisht Hackathon 3.0 - Project EdTech #1**

## 📝 Problem & Solution
* [cite_start]**Problem**: Students struggle with messy lecture notes and identifying their own knowledge gaps[cite: 7, 82].
* [cite_start]**Solution**: An AI-powered app that transforms messy notes into clean summaries, generates quizzes, and matches peers based on shared learning needs[cite: 7, 84, 85].

## 🛠️ Tech Stack
* [cite_start]**Database**: SQLite (optimized for hackathon speed)[cite: 10, 20].
* [cite_start]**Auth**: JWT with `bcrypt` password hashing via FastAPI[cite: 12, 33, 36, 37].
* [cite_start]**Deployment**: Render (Targeted)[cite: 54, 55].

## 👥 Team
* [cite_start]**Ashwin Jaishanker**: DB, Auth, Deployment & Demo Lead[cite: 3].
* [cite_start]**Pavan Kumar**: Backend API & ML Pipeline[cite: 116, 117].
* [cite_start]**Soham B**: Frontend Lead & UI Design[cite: 118, 119].

## ⚙️ Setup Instructions
1. [cite_start]**Install dependencies**: `py -m pip install -r requirements.txt`[cite: 56].
2. [cite_start]**Initialize DB**: `py db_setup.py`[cite: 107].
3. [cite_start]**Start API**: `py -m uvicorn main:app --reload`[cite: 57].
