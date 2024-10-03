from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.loan import Loan
import app.utils.credit_calculation as credit_calculation


async def get_loans(db: AsyncSession, skip: int = 0, limit: int = 100) -> list:
    result = await db.execute(select(Loan).offset(skip).limit(limit))
    return result.scalars().all()


async def create_loan(db: AsyncSession, loan: Loan) -> Loan:
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    await db.commit()
    await db.refresh(db_loan)
    await credit_calculation.calculate_credit(db, db_loan.company_id)
    return db_loan


async def update_loan_by_company(db: AsyncSession, company_id: str, loan: Loan) -> Loan:
    result = await db.execute(select(Loan).filter(Loan.company_id == company_id))
    db_loan = result.scalars().first()
    if db_loan:
        for key, value in loan.model_dump().items():
            setattr(db_loan, key, value)
        await db.commit()
        await db.refresh(db_loan)

        await credit_calculation.calculate_credit(db, company_id)
    return db_loan
