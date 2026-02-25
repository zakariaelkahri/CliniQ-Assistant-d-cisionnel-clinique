from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.routes import auth
from app.api.routes import query
from app.db.session import engine
from app.db.base import Base
from app.seeders.seed import seed_all

from app.models.user import User  # noqa
from app.models.query import Query  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    
    try:
        await seed_all()
    except Exception as e:
        print(f"error during seeding data {e}")
    
    yield 

        
app = FastAPI(
    title="RAG Lab Support API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    description="Medical equipment technical support with RAG",
    version="1.0.0"
)

app.include_router(auth.router,prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(query.router,prefix=f"{settings.API_V1_STR}/query", tags=["Query"])

@app.get("/")
async def root():
    return {"message": "RAG Lab Support API is running", "status": "healthy"}

