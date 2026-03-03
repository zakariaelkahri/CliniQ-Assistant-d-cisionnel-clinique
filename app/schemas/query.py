from pydantic import BaseModel
from datetime import datetime

class AssistantRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    id: int 
    question: str
    response: str
    created_at: datetime
    
    class Config:
        from_attributes = True