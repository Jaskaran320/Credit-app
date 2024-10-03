from pydantic import BaseModel, ConfigDict
from datetime import date


class AnnualInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    company_id: str
    annual_turnover: float
    profit: float
    fiscal_year: int
    reported_date: date
