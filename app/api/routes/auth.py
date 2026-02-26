from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import AsyncSessionLocal 
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.api.deps import get_db

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def create_user(user_in: UserCreate, db: AsyncSession=Depends(get_db))->Any:
    # email verifier
    resault = await db.execute(select(User).filter(User.email == user_in.email))
    
    existing_user = resault.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="this User(email) already exist"
        )

    user = User(
        email = user_in.email,
        username = user_in.username,
        hashed_password = security.get_password_hash(user_in.password),
        role = "technician",
        
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login",response_model=Token)

async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db))->Any:
    
    resault = await db.execute(select(User).filter(User.username == form_data.username ))
    user = resault.scalars().first()
    
    hashed_password = security.get_password_hash(form_data.password)
    if not user or not security.verify_password(form_data.password,hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password or email incorrect"  
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": security.create_access_token(
            user.id,
            expires_delta=access_token_expires
            ),
        "token_type": "bearer",
    }