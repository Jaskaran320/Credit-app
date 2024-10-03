from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    registration_date = Column(Date)
    number_of_employees = Column(Integer)
    contact_number = Column(String)
    contact_email = Column(String)
    company_website = Column(String)

    annual_info = relationship("AnnualInfo", back_populates="company")
    loans = relationship("Loan", back_populates="company")
    credits = relationship("Credit", back_populates="company")
