from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Credit(Base):
    __tablename__ = "credits"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.company_id"), unique=True)
    credit_amount = Column(Float)

    company = relationship("Company", back_populates="credits")