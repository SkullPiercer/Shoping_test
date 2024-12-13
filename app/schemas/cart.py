from typing import Optional
from fastapi import HTTPException
from http import HTTPStatus
from pydantic import BaseModel, Field, validator, root_validator


class CartCreate(BaseModel):
    product_id: int
    quantity: int

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

class CartUpdate(CartCreate):
    product_id: Optional[int]

    @root_validator(pre=True)
    def check_forbidden_fields(cls, values):
        forbidden_fields = {
            "id", "product_id"
        }
        for field in forbidden_fields:
            if field in values:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f'Нельзя изменять поле {field}',
                )
        return values