from fastapi import APIRouter, HTTPException, status
from typing import List
from app.api.dependencies.core import db_dependency
from app.crud import credit as credit_crud
from app.schemas.credit import Credit

router = APIRouter()


@router.get("/credits", response_model=List[Credit])
async def get_all_credits(db: db_dependency, skip: int = 0, limit: int = 100):
    try:
        credit_info = await credit_crud.get_credits(db, skip=skip, limit=limit)
        return credit_info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/credits/{company_id}", response_model=Credit)
async def get_credit(db: db_dependency, company_id: str):
    credit_info = await credit_crud.get_credits_by_company(db, company_id=company_id)
    if credit_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit info not found")
    return credit_info


@router.post("/credits", response_model=Credit)
def add_credit(db: db_dependency, credit_info: Credit):
    return credit_info
