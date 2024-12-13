from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func

from app.crud.base import CRUDBase
from app.models import Cart, User, Product

from app.core.constants import CART_EMPTY


class CRUDOrder(CRUDBase):
    async def calculate_total(
            self,
            user: User,
            session: AsyncSession
    ) -> float:
        query = (
            select(Cart, Product.price)
            .join(Product, Product.id == Cart.product_id)
            .where(Cart.user_id == user.id)
        )
        result = await session.execute(query)
        cart_positions = result.all()
        total = 0.0
        for cart, price in cart_positions:
            total += float(price) * cart.quantity

        return total

    async def clear_cart(
            self,
            user: User,
            session: AsyncSession
    ):
        await session.execute(
            delete(Cart).where(Cart.user_id == user.id)
        )
        await session.commit()


order_crud = CRUDOrder(Cart)
