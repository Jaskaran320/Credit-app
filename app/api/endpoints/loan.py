from fastapi import APIRouter, HTTPException, status
from typing import List

from app.api.dependencies.core import db_dependency
from app.schemas.loan import Loan
from app.crud import loan as loan_crud

router = APIRouter()


@router.get("/loans/", response_model=List[Loan])
async def read_loans(db: db_dependency, skip: int = 0, limit: int = 100):
    try:
        info = await loan_crud.get_loans(db, skip=skip, limit=limit)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/loans/", response_model=Loan)
async def create_loan(db: db_dependency, loan: Loan):
    try:
        info = await loan_crud.create_loan(db, loan=loan)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/loans/{company_id}", response_model=Loan)
async def update_loan_by_company(db: db_dependency, company_id: str, loan: Loan):
    info = await loan_crud.update_loan_by_company(db, company_id=company_id, loan=loan)
    if info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return info
