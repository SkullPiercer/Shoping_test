from sqlalchemy import Column, ForeignKey, Integer

from app.core.db import Base


class Cart(Base):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_cart_user_id_user')
    )

    product_id = Column(
        Integer, ForeignKey('product.id', name='fk_cart_user_id_product')
    )

    quantity = Column(Integer, nullable=False)
