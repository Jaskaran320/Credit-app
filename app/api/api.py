from fastapi import APIRouter, Depends
from app.api.endpoints import company, annual_info, credit, loan, token
from app.api.dependencies.auth import get_current_user

api_router = APIRouter()

api_router.include_router(token.router, tags=["token"])
auth_dependencies = [Depends(get_current_user)]

api_router.include_router(company.router, tags=["companies"], dependencies=auth_dependencies)
api_router.include_router(annual_info.router, tags=["annual_info"], dependencies=auth_dependencies)
api_router.include_router(loan.router, tags=["loans"], dependencies=auth_dependencies)
api_router.include_router(credit.router, tags=["credits"], dependencies=auth_dependencies)