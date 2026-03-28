from fastapi import APIRouter, Depends, HTTPException
from app.schemas import QuizResponse, QuizSubmission, QuizResultOut
from app.auth import get_current_user
from app.db.database import get_note, save_quiz_result, get_quiz_results_by_user
from app.services.quiz_generator import generate_quiz

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.get("/{note_id}", response_model=QuizResponse)
async def get_quiz(note_id: int, user: dict = Depends(get_current_user)):
    note = get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not note["summary"]:
        raise HTTPException(status_code=400, detail="Note has no summary yet")
    questions = await generate_quiz(note["summary"], note["raw_text"])
    return QuizResponse(note_id=note_id, questions=questions)


@router.post("/submit")
def submit_quiz(req: QuizSubmission, user: dict = Depends(get_current_user)):
    result_id = save_quiz_result(user["id"], req.note_id, req.score, req.total, req.answers)
    return {"result_id": result_id, "score": req.score, "total": req.total}


@router.get("", response_model=list[QuizResultOut])
def list_results(user: dict = Depends(get_current_user)):
    results = get_quiz_results_by_user(user["id"])
    return [
        QuizResultOut(
            id=r["id"],
            note_id=r["note_id"],
            score=r["score"],
            total=r["total_questions"],
            created_at=str(r["created_at"]),
        )
        for r in results
    ]