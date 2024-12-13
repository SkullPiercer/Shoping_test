from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Cart, User, Product


class CRUDCart(CRUDBase):
    async def get_user_cart(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Product]:
        user_cart = await session.execute(
            select(Cart).where(
                Cart.user_id == user.id
            )
        )
        return user_cart.scalars().all()


cart_crud = CRUDCart(Cart)
