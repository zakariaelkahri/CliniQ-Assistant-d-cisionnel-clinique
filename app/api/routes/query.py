import asyncio
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from app.rag.pipeline import answer_question
from app.models.query import Query
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.schemas.query import AssistantRequest
import logging



router = APIRouter()

@router.post("/assistant")
async def assistant(
    query: AssistantRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    try:
        question = query.question
        answer = answer_question(question)

        new_query = Query(
            user_id = current_user,
            question = question,
            response = answer
        )
        
        db.add(new_query)
        await db.commit()
        await db.refresh(new_query)

        return {
            "question": question,
            "answer": answer,
            "current_user": current_user,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while processing your question.",
        )