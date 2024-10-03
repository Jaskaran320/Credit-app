from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine
from app.core.config import settings
from app.models import company, annual_info, credit, loan
from app.api.api import api_router
import uvicorn


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(company.Base.metadata.create_all)
        await conn.run_sync(annual_info.Base.metadata.create_all)
        await conn.run_sync(loan.Base.metadata.create_all)
        await conn.run_sync(credit.Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Credit Information API service"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
