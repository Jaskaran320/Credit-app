import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

fake = Faker()


@pytest.fixture(scope="function")
def company_data():
    return {
        "name": fake.company(),
        "company_id": fake.uuid4(),
        "address": fake.address(),
        "registration_date": str(fake.date_between(start_date="-2y", end_date="today")),
        "number_of_employees": fake.random_int(min=1, max=10000),
        "contact_number": fake.phone_number(),
        "contact_email": fake.email(),
        "company_website": fake.url()
    }


@pytest.fixture(scope="function")
def annual_info_data(company_data):
    return {
        "id": fake.uuid4(),
        "company_id": company_data["company_id"],
        "annual_turnover": fake.random_int(min=100000, max=10000000),
        "profit": fake.random_int(min=10000, max=1000000),
        "fiscal_year": str(fake.date_between(start_date="-2y", end_date="today").year),
        "reported_date": str(fake.date_between(start_date="-2y", end_date="today"))
    }


@pytest.fixture(scope="function")
def loan_data(company_data):
    return {
        "id": fake.uuid4(),
        "company_id": company_data["company_id"],
        "loan_amount": fake.random_int(min=1000, max=1000000),
        "taken_on": str(fake.date_between(start_date="-2y", end_date="today")),
        "loan_bank_provider": fake.company(),
        "loan_status": "DUE"
    }


@pytest.mark.asyncio
async def test_create_company(client: TestClient, db: AsyncSession, company_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/companies/", json=company_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == company_data["name"]
    assert "company_id" in data


@pytest.mark.asyncio
async def test_create_annual_info(client: TestClient, db: AsyncSession, company_data, annual_info_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/companies/", json=company_data, headers=headers)
    response = client.post("/annual_info/", json=annual_info_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_id"] == annual_info_data["company_id"]


@pytest.mark.asyncio
async def test_create_loan(client: TestClient, db: AsyncSession, company_data, loan_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/companies/", json=company_data, headers=headers)
    response = client.post("/loans/", json=loan_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_id"] == loan_data["company_id"]


@pytest.mark.asyncio
async def test_get_credit(client: TestClient, db: AsyncSession, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/credits/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)