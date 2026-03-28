# LearnSync — Context-Aware Collaborative Learning Platform

> **Vashisht Hackathon 3.0 | EdTech Track — Problem Statement #1**
> IIITDM Kancheepuram | March 28–29, 2026

## Live URL

**Frontend:** https://learnsync-app.onrender.com
**Backend API:** https://learnsync-api.onrender.com

**Demo login:** username `pavan` / password `test1234`

## Problem

Students take unstructured, context-dependent notes during fast-paced lectures that become difficult to understand over time. Peer learning remains underutilized due to social hesitation and absence of structured collaboration systems.

## Solution

**LearnSync** bridges individual note-taking with collaborative learning through AI:

1. **Summarizes** messy lecture notes into clean summaries using extractive NLP
2. **Extracts key concepts** using KeyBERT (transformer-based keyword extraction)
3. **Generates quizzes** automatically to test understanding
4. **Matches peers** by finding students with overlapping knowledge gaps

## Features

- Upload lecture notes (text paste)
- AI-powered summarization and concept extraction
- Auto-generated MCQ quizzes with instant feedback
- Peer matching based on concept overlap (Jaccard similarity)
- Learning dashboard with progress tracking
- JWT authentication with secure password hashing

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Tailwind CSS, Vite, React Router, Axios |
| Backend | FastAPI, Python 3.12, Uvicorn |
| ML/NLP | KeyBERT, sentence-transformers (all-MiniLM-L6-v2) |
| Database | SQLite |
| Auth | JWT (python-jose), SHA-256 hashing |
| Deployment | Render (frontend + backend) |
| Icons | Lucide React |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup | Create account |
| POST | /api/auth/login | Login |
| POST | /api/notes | Upload note → summary + concepts |
| GET | /api/notes | List user notes |
| GET | /api/quiz/{note_id} | Generate quiz |
| POST | /api/quiz/submit | Submit quiz answers |
| GET | /api/peers | Find peer matches |
| GET | /api/dashboard | User stats |

## Setup Instructions

### Backend
```bash
cd backend
pip install fastapi uvicorn python-jose[cryptography] httpx python-multipart Pillow numpy
python seed_data.py
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Open-Source Libraries

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [React](https://react.dev/) — Frontend library
- [Tailwind CSS](https://tailwindcss.com/) — Styling
- [KeyBERT](https://github.com/MaartenGr/KeyBERT) — Keyword extraction
- [sentence-transformers](https://www.sbert.net/) — Text embeddings
- [python-jose](https://github.com/mpdavis/python-jose) — JWT tokens
- [Axios](https://axios-http.com/) — HTTP client
- [Lucide](https://lucide.dev/) — Icons
- [react-hot-toast](https://react-hot-toast.com/) — Notifications

## Team

| Name | Role | ID |
|------|------|----|
| Pavankumar D | ML Pipeline & Backend | EC23B1063 |
| Soham B | Frontend | EC23B1067 |
| Ashwin Jaishankar | Database, Auth & Deployment | ME23B1027 |