from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String

from app.core.constants import (
    PRICE_PRECISION, PRICE_SCALE
)
from app.core.db import Base


class Order(Base):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_order_user_id_user')
    )

    total_price = Column(
        DECIMAL(PRICE_PRECISION, PRICE_SCALE),
        nullable=False
    )

    status = Column(String, default='pending')
