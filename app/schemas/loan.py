from pydantic import BaseModel, ConfigDict
from datetime import date
from enum import Enum


class LoanStatus(str, Enum):
    PAID = "PAID"
    DUE = "DUE"
    INITIATED = "INITIATED"


class Loan(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    company_id: str
    loan_amount: float
    taken_on: date
    loan_bank_provider: str
    loan_status: LoanStatus