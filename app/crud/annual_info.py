from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.annual_info import AnnualInfo
import app.utils.credit_calculation as credit_calculation


async def get_annual_info(db: AsyncSession, skip: int = 0, limit: int = 100) -> list:
    result = await db.execute(select(AnnualInfo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_annual_info(db: AsyncSession, annual_info: AnnualInfo) -> AnnualInfo:
    result = await db.execute(
        select(AnnualInfo).filter(
            AnnualInfo.company_id == annual_info.company_id,
            AnnualInfo.fiscal_year == annual_info.fiscal_year,
        )
    )

    if result.scalars().first():
        raise ValueError(f"Annual info already exists for the fiscal year {annual_info.fiscal_year}")
    db_annual_info = AnnualInfo(**annual_info.model_dump())
    db.add(db_annual_info)
    await db.commit()
    await db.refresh(db_annual_info)
    await credit_calculation.calculate_credit(db, annual_info.company_id)
    return db_annual_info


async def update_annual_info_by_company(
    db: AsyncSession, company_id: str, annual_info: AnnualInfo
) -> AnnualInfo:
    result = await db.execute(
        select(AnnualInfo).filter(AnnualInfo.company_id == company_id)
    )
    db_annual_info = result.scalars().first()
    if db_annual_info:
        for key, value in annual_info.model_dump().items():
            setattr(db_annual_info, key, value)
        await db.commit()
        await db.refresh(db_annual_info)

        await credit_calculation.calculate_credit(db, company_id)
    return db_annual_info
