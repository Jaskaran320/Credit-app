from sqlalchemy import Column, Float, Date, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class LoanStatus(enum.Enum):
    PAID = "PAID"
    DUE = "DUE"
    INITIATED = "INITIATED"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.company_id"))
    loan_amount = Column(Float)
    taken_on = Column(Date)
    loan_bank_provider = Column(String)
    loan_status = Column(Enum(LoanStatus))

    company = relationship("Company", back_populates="loans")