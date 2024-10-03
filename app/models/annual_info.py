from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class AnnualInfo(Base):
    __tablename__ = "annual_info"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.company_id"))
    annual_turnover = Column(Float)
    profit = Column(Float)
    fiscal_year = Column(Integer)
    reported_date = Column(Date)

    company = relationship("Company", back_populates="annual_info")