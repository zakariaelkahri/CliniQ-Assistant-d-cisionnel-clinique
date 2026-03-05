from fastapi import APIRouter, Depends, HTTPException, status
from app.rag.pipeline import answer_question
from app.models.query import Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user_id
from app.schemas.query import AssistantRequest, QueryResponse
from app.services.query_service import display_user_query
from app.core.metrics import http_requests_total
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/assistant")
async def assistant(
    query: AssistantRequest,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user_id),
) -> dict:
    try:
        question = query.question
        answer = answer_question(question)

        new_query = Query(
            user_id=current_user,
            question=question,
            response=answer
        )

        db.add(new_query)
        await db.commit()
        await db.refresh(new_query)

        http_requests_total.labels(
            method="POST", endpoint="/query/assistant", status_code="200"
        ).inc()

        return {
            "question": question,
            "answer": answer,
            "current_user": current_user,
        }
    except Exception:
        http_requests_total.labels(
            method="POST", endpoint="/query/assistant", status_code="500"
        ).inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while processing your question.",
        )


@router.get("/historiques", response_model=list[QueryResponse])
async def historique(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        result = await display_user_query(db, user_id)
        http_requests_total.labels(
            method="GET", endpoint="/query/historiques", status_code="200"
        ).inc()
        return result
    except Exception:
        http_requests_total.labels(
            method="GET", endpoint="/query/historiques", status_code="500"
        ).inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching query history.",
        )
