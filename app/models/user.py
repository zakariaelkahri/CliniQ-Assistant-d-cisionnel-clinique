from app.db.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="technician", nullable=False)
    

    queries = relationship("Query", back_populates="user")