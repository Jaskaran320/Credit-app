from pydantic import BaseModel, ConfigDict


class Credit(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    company_id: str
    credit_amount: float
