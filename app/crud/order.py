from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import CART_EMPTY
from app.crud.base import CRUDBase
from app.crud.product import product_crud
from app.models import Cart, User, Order


class CRUDOrder(CRUDBase):
    async def create_order(
            self,
            session: AsyncSession,
            user: User
    ):
        cart_items = await session.execute(
            select(Cart).where(Cart.user_id == user.id)
        )
        cart_items = cart_items.scalars().all()

        total_price = 0
        for item in cart_items:
            product = await product_crud.get(obj_id=item.product_id, session=session)
            total_price += product.price * item.quantity
            product.in_stock -= item.quantity
            if product.in_stock <= CART_EMPTY:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Пока продукт находился в корзине yfkbxbt товара:{product} изменилось!',
                )
            session.add(product)

        order_data = {
            "user_id": user.id,
            "total_price": total_price
        }

        order = self.model(**order_data)
        session.add(order)

        await session.execute(
            delete(Cart).where(Cart.user_id == user.id)
        )
        await session.commit()
        await session.refresh(order)

        return order

    async def get_my_orders(
            self,
            user: User,
            session: AsyncSession
    ):
        user_orders = await session.execute(
            select(Order).where(Order.user_id == user.id)
        )
        return user_orders.scalars().all()
order_crud = CRUDOrder(Order)
