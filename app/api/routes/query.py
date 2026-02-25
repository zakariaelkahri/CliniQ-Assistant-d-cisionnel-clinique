from fastapi import APIRouter
from app.rag.pipeline import answer_question

router = APIRouter()

@router.post("/chatbot")
async def chatbot(question: str)->dict :
    try:
        answer = answer_question(question)
        return {"question":question, "answer":answer}
    except Exception as e:
        return {"exception":f"Something went wrong :{e}"}
        
    
