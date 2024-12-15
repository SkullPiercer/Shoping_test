from pydantic import BaseModel


class OrderCreate(BaseModel):
    total_price: float
    status: str
