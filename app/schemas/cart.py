from pydantic import BaseModel, Field, validator


class CartCreate(BaseModel):
    quantity: int = Field()

    @validator('quantity')
    def quantity_can_not_be_le_zero(cls, value):
        if value <= 0:
            raise ValueError(
                'Кол-во продукта не может быть меньше или равным нулю.'
            )
        return value


class CartDB(CartCreate):
    id: int

    class Config:
        orm_mode = True
