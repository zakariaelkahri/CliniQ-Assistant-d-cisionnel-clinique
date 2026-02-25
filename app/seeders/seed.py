"""
Database seeder script
Run this to populate the database with sample data
"""
import asyncio
from app.db.session import AsyncSessionLocal
from app.seeders.user_seeder import seed_users
from app.seeders.query_seeder import seed_queries


async def seed_all():
    """Run all seeders"""
    print("🌱 Starting database seeding...")
    
    async with AsyncSessionLocal() as db:
        try:
            # Seed users first (queries depend on users)
            await seed_users(db)
            
            # Seed queries
            await seed_queries(db)
            
            print("✅ Database seeding completed successfully!")
            
        except Exception as e:
            print(f"Error during seeding: {e}")
            await db.rollback()
            raise 


if __name__ == "__main__":
    asyncio.run(seed_all())
