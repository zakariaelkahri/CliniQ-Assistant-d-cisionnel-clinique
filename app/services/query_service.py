from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.query import Query
from sqlalchemy import select


async def display_user_query(db: AsyncSession, user_id: int):

    stmt = select(Query).join(Query.user).where(User.id == user_id)
    rslt = await db.execute(stmt)
    queries = rslt.scalars().all()
    return queries