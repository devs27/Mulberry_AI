from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.chat.chat_service import process_chat

router = APIRouter(prefix="/api/chat", tags=["chat"])


class DiagnosisContextInput(BaseModel):
    id: Optional[str] = None
    disease: Optional[str] = None
    confidence: Optional[float] = None
    variety: Optional[str] = None
    timestamp: Optional[str] = None


class ChatHistoryItem(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="Farmer's question text")
    language: Optional[str] = Field(None, description="Optional override language ('en' or 'ta')")
    diagnosis_id: Optional[str] = Field(None, description="Optional diagnosis id")
    diagnosis_context: Optional[DiagnosisContextInput] = Field(None, description="Optional diagnosis context")
    session_history: Optional[List[ChatHistoryItem]] = Field(None, description="Recent conversation turns")


class ChatResponse(BaseModel):
    reply: str
    language: str
    topic: str
    intent: Optional[str] = None
    source: Optional[str] = None
    diagnosis_context: Optional[Dict[str, Any]] = None


@router.post("/ask", response_model=ChatResponse)
def ask_mulberrycare(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    lang_override = payload.language
    default_lang = current_user.preferred_language.value

    # Parse session history into dicts
    session_history_dicts = None
    if payload.session_history:
        session_history_dicts = [{"role": h.role, "content": h.content} for h in payload.session_history]

    # Parse diagnosis context
    diagnosis_context_dict = None
    if payload.diagnosis_context:
        if hasattr(payload.diagnosis_context, "model_dump"):
            diagnosis_context_dict = payload.diagnosis_context.model_dump()
        else:
            diagnosis_context_dict = payload.diagnosis_context.dict()

    result = process_chat(
        message=payload.message,
        lang_override=lang_override,
        default_lang=default_lang,
        db=db,
        current_user=current_user,
        diagnosis_id=payload.diagnosis_id,
        diagnosis_context=diagnosis_context_dict,
        session_history=session_history_dicts
    )

    return result
