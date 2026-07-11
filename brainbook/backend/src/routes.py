from fastapi import APIRouter, Depends, HTTPException
from src.services.services import ask_question
from config.database.database import AsyncSession, get_db

router = APIRouter(prefix="/main", tags=["Main"])

@router.post("/ask")
async def ask(query: str, db: AsyncSession = Depends(get_db)):
    if not query:
        raise HTTPException(status_code = 400, detail = "Введите вопрос или текст")
    answer = await ask_question(query, db)
    return answer