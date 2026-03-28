from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.schemas import NoteUpload, NoteOut, SummaryResponse, ConceptOut
from app.auth import get_current_user
from app.db.database import save_note, get_note, get_notes_by_user, update_note_ml
from app.services.ml_pipeline import run_pipeline
from app.services.ocr_service import extract_text_from_image

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("", response_model=SummaryResponse)
async def upload_note(req: NoteUpload, user: dict = Depends(get_current_user)):
    if len(req.raw_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Note text too short")
    note_id = save_note(user["id"], req.raw_text)
    result = await run_pipeline(req.raw_text)
    concepts_data = [{"name": c["name"], "score": c["score"]} for c in result["concepts"]]
    update_note_ml(note_id, result["summary"], concepts_data)
    return SummaryResponse(
        note_id=note_id,
        summary=result["summary"],
        concepts=[ConceptOut(**c) for c in concepts_data],
    )


@router.post("/image", response_model=SummaryResponse)
async def upload_image_note(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    allowed = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Use PNG, JPG, or WEBP")
    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    extracted_text = await extract_text_from_image(image_bytes, file.content_type)
    if len(extracted_text.strip()) < 10 or extracted_text.startswith("["):
        raise HTTPException(status_code=400, detail="Could not extract text. Try a clearer photo.")

    note_id = save_note(user["id"], extracted_text)
    result = await run_pipeline(extracted_text)
    concepts_data = [{"name": c["name"], "score": c["score"]} for c in result["concepts"]]
    update_note_ml(note_id, result["summary"], concepts_data)
    return SummaryResponse(
        note_id=note_id,
        summary=result["summary"],
        concepts=[ConceptOut(**c) for c in concepts_data],
    )


@router.get("", response_model=list[NoteOut])
def list_notes(user: dict = Depends(get_current_user)):
    notes = get_notes_by_user(user["id"])
    return [
        NoteOut(
            id=n["id"], raw_text=n["raw_text"], summary=n["summary"],
            concepts=[ConceptOut(**c) for c in n["concepts"]] if n["concepts"] else [],
            created_at=str(n["created_at"]),
        )
        for n in notes
    ]


@router.get("/{note_id}", response_model=NoteOut)
def get_single_note(note_id: int, user: dict = Depends(get_current_user)):
    note = get_note(note_id)
    if not note or note["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut(
        id=note["id"], raw_text=note["raw_text"], summary=note["summary"],
        concepts=[ConceptOut(**c) for c in note["concepts"]] if note["concepts"] else [],
        created_at=str(note["created_at"]),
    )