from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company


async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 100) -> list:
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()


async def get_company_by_id(db: AsyncSession, company_id: str) -> Company:
    result = await db.execute(select(Company).filter(Company.company_id == company_id))
    return result.scalars().first()


async def create_company(db: AsyncSession, company: Company) -> Company:
    db_company = Company(**company.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company


async def update_company(db: AsyncSession, company_id: str, company: Company) -> Company:
    result = await db.execute(select(Company).filter(Company.company_id == company_id))
    db_company = result.scalars().first()
    if db_company:
        for key, value in company.model_dump().items():
            setattr(db_company, key, value)
        await db.commit()
        await db.refresh(db_company)
    return db_company


async def delete_company(db: AsyncSession, company_id: str) -> Company:
    result = await db.execute(select(Company).filter(Company.company_id == company_id))
    db_company = result.scalars().first()
    if db_company:
        await db.delete(db_company)
        await db.commit()
    return db_company