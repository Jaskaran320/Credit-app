from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    company_id: str
    address: str
    registration_date: date
    number_of_employees: int
    contact_number: str
    contact_email: EmailStr
    company_website: str
