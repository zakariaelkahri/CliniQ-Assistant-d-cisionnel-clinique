from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default = func.now())

    user = relationship("User", back_populates="queries")

