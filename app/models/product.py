from sqlalchemy import Column, DECIMAL, String, Integer

from app.core.constants import (
    CATEGORY_MAX_LEN, PRICE_PRECISION, PRICE_SCALE, PRODUCT_NAME_MAX_LEN
)
from app.core.db import Base


class Product(Base):
    name = Column(
        String(PRODUCT_NAME_MAX_LEN),
        unique=True,
        nullable=False
    )
    price = Column(
        DECIMAL(PRICE_PRECISION, PRICE_SCALE),
        nullable=False
    )
    category = Column(
        String(CATEGORY_MAX_LEN),
        nullable=False
    )

    in_stock = Column(
        Integer(),
        nullable=False
    )
