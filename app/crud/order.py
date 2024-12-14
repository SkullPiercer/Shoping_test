from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func

from app.crud.base import CRUDBase
from app.models import Cart, User, Product, Order

from app.core.constants import CART_EMPTY

from app.crud.product import product_crud


class CRUDOrder(CRUDBase):
    async def create_order(
            self,
            session: AsyncSession,
            user: User
    ):
        # Получаем все товары из корзины пользователя
        cart_items = await session.execute(
            select(Cart).where(Cart.user_id == user.id)
        )
        cart_items = cart_items.scalars().all()

        # Высчитываем итоговую стоимость
        total_price = 0
        for item in cart_items:
            product = await product_crud.get(obj_id=item.product_id, session=session)
            total_price += product.price * item.quantity
            product.in_stock -= item.quantity
            session.add(product)
        # Создаем заказ
        order_data = {
            "user_id": user.id,
            "total_price": total_price
        }

        order = self.model(**order_data)
        session.add(order)

        # (Опционально) Очищаем корзину после оформления заказа
        await session.execute(
            delete(Cart).where(Cart.user_id == user.id)
        )
        await session.commit()
        await session.refresh(order)

        return order


order_crud = CRUDOrder(Order)
