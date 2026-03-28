from pydantic import BaseModel
from typing import Optional


class SignupRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class NoteUpload(BaseModel):
    raw_text: str

class ConceptOut(BaseModel):
    name: str
    score: float

class SummaryResponse(BaseModel):
    note_id: int
    summary: str
    concepts: list[ConceptOut]

class NoteOut(BaseModel):
    id: int
    raw_text: str
    summary: Optional[str] = None
    concepts: list[ConceptOut] = []
    created_at: str

class QuizOption(BaseModel):
    label: str
    text: str

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: list[QuizOption]
    correct: str

class QuizResponse(BaseModel):
    note_id: int
    questions: list[QuizQuestion]

class QuizSubmission(BaseModel):
    note_id: int
    answers: list[dict]
    score: int
    total: int

class QuizResultOut(BaseModel):
    id: int
    note_id: int
    score: int
    total: int
    created_at: str

class PeerMatch(BaseModel):
    user_id: int
    username: str
    shared_concepts: list[str]
    match_score: float

class PeerResponse(BaseModel):
    matches: list[PeerMatch]