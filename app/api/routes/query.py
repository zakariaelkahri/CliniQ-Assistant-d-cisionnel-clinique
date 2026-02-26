from fastapi import APIRouter, Depends, HTTPException, status
from app.rag.pipeline import answer_question
from app.models.query import Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db



router = APIRouter()

@router.post("/chatbot")
async def chatbot(question: str,  db: AsyncSession = Depends(get_db) )->dict :
    try:
        answer = await answer_question(question)
        add_question = Query()
        return {"question":question, "answer":answer}
    except Exception as e:
        return {"exception":f"Something went wrong :{e}"}
        
    
