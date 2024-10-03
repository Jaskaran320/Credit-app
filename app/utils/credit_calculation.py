from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.annual_info import AnnualInfo
from app.models.credit import Credit
from app.models.loan import Loan, LoanStatus
from datetime import datetime
import uuid

async def calculate_credit(db: AsyncSession, company_id: str) -> None:
    three_years_ago = datetime.now().year - 3
    annual_info = await db.execute(
        select(AnnualInfo).filter(
            AnnualInfo.company_id == company_id,
            AnnualInfo.fiscal_year >= three_years_ago
        )
    )
    annual_info = annual_info.scalars().all()
    total_turnover = sum(info.annual_turnover for info in annual_info)

    due_loans = await db.execute(
        select(Loan).filter(
            Loan.company_id == company_id,
            Loan.loan_status == LoanStatus.DUE
        )
    )
    due_loans = due_loans.scalars().all()    
    total_due_loans = sum(loan.loan_amount for loan in due_loans)
    
    credit = total_turnover - total_due_loans
    
    result = await db.execute(select(Credit).filter(Credit.company_id == company_id))
    db_credit = result.scalars().first()
    if db_credit:
        db_credit.credit_amount = credit
        await db.commit()
        await db.refresh(db_credit)
    else:
        db_credit = Credit(
            id=str(uuid.uuid4()),
            company_id=company_id,
            credit_amount=credit
        )
        db.add(db_credit)
        await db.commit()
        await db.refresh(db_credit)