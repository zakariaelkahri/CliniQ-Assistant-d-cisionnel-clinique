from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import pwd_context, get_password_hash


async def seed_users(db: AsyncSession) -> list[User]:
    """Seed users table with sample data"""
    
    # Check if users already exist
    result = await db.execute(select(User).limit(1))
    if result.scalar_one_or_none():
        print("Users already seeded, skipping...")
        return []
    
    users_data = [
        {
            "username": "admin",
            "email": "admin@mediassist.com",
            "password": "Admin@123",
            "role": "admin"
        },
        {
            "username": "john_tech",
            "email": "john.tech@mediassist.com",
            "password": "Tech@123",
            "role": "technician"
        },
        {
            "username": "sarah_tech",
            "email": "sarah.tech@mediassist.com",
            "password": "Tech@123",
            "role": "technician"
        },
        {
            "username": "mike_manager",
            "email": "mike.manager@mediassist.com",
            "password": "tech@123",
            "role": "technician"
        },
        {
            "username": "lisa_tech",
            "email": "lisa.tech@mediassist.com",
            "password": "Tech@123",
            "role": "technician"
        }
    ]
    
    users = []
    for user_data in users_data:
        hashed_password = get_password_hash(user_data["password"])
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            role=user_data["role"]
        )
        db.add(user)
        users.append(user)
    
    await db.commit()
    
    # Refresh to get IDs
    for user in users:
        await db.refresh(user)
    
    print(f"✓ Seeded {len(users)} users")
    return users
