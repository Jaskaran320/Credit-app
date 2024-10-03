from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.credit import Credit


async def get_credits(db: AsyncSession, skip: int = 0, limit: int = 100) -> list:
    result = await db.execute(select(Credit).offset(skip).limit(limit))
    return result.scalars().all()


async def get_credits_by_company(db: AsyncSession, company_id: str) -> Credit:
    result = await db.execute(select(Credit).filter(Credit.company_id == company_id))
    return result.scalars().first()