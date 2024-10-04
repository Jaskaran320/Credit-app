from fastapi import APIRouter, HTTPException, status
from typing import List

from app.api.dependencies.core import db_dependency
from app.schemas.annual_info import AnnualInfo
from app.crud import annual_info as annual_info_crud

router = APIRouter()


@router.get("/annual_info/", response_model=List[AnnualInfo])
async def read_annual_info(db: db_dependency, skip: int = 0, limit: int = 100):
    try:
        info = await annual_info_crud.get_annual_info(db, skip=skip, limit=limit)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/annual_info/", response_model=AnnualInfo)
async def create_annual_info(db: db_dependency, annual_info: AnnualInfo):
    try:
        info = await annual_info_crud.create_annual_info(db, annual_info=annual_info)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/annual_info/{company_id}", response_model=AnnualInfo)
async def update_annual_info_by_company(
    db: db_dependency, company_id: str, annual_info: AnnualInfo
):
    info = await annual_info_crud.update_annual_info_by_company(
        db, company_id=company_id, annual_info=annual_info
    )
    if info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return info
