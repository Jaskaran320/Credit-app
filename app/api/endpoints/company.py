from fastapi import APIRouter, HTTPException, status
from typing import List

from app.api.dependencies.core import db_dependency
from app.schemas.company import Company
from app.crud import company as company_crud

router = APIRouter()


@router.get("/companies/", response_model=List[Company])
async def read_companies(db: db_dependency, skip: int = 0, limit: int = 100):
    try:
        companies = await company_crud.get_companies(db, skip=skip, limit=limit)
        return companies
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/companies/", response_model=Company)
async def create_company(db: db_dependency, company: Company):
    db_company = await company_crud.get_company_by_id(db, company_id=company.company_id)
    if db_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Company already registered"
        )
    info = await company_crud.create_company(db, company=company)
    return info


@router.put("/companies/{company_id}", response_model=Company)
async def update_company(db: db_dependency, company_id: str, company: Company):
    db_company = await company_crud.update_company(
        db, company_id=company_id, company=company
    )
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return db_company


@router.delete("/companies/{company_id}", response_model=Company)
async def delete_company(db: db_dependency, company_id: str):
    db_company = await company_crud.delete_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return db_company
