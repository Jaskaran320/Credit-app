import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.core.config import settings
from app.models import company, annual_info, credit, loan

DATABASE_URL = settings.DATABASE_URL
USERNAME = settings.USER_NAME
PASSWORD = settings.PASS_WORD

engine = create_async_engine(DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    expire_on_commit=False, 
    class_=AsyncSession
)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(company.Base.metadata.create_all)
        await conn.run_sync(annual_info.Base.metadata.create_all)
        await conn.run_sync(credit.Base.metadata.create_all)
        await conn.run_sync(loan.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(company.Base.metadata.drop_all)
        await conn.run_sync(annual_info.Base.metadata.drop_all)
        await conn.run_sync(credit.Base.metadata.drop_all)
        await conn.run_sync(loan.Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def db():
    async with TestingSessionLocal() as session:
        yield session
        await session.close()


@pytest.fixture(scope="module")
def auth_token(client: TestClient):
    response = client.post("/token", data={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    return response.json()["access_token"]
