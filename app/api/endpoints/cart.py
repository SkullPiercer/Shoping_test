from http import HTTPStatus

from app.api.validators import (
    check_product_exist,
    comparison_of_quantity_with_stock,
    check_cart_position_exist
)
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.cart import cart_crud
from app.crud.product import product_crud
from app.models import User
from app.schemas.cart import CartCreate, CartDB, CartUpdate


router = APIRouter()


@router.get(
    '/',
    response_model=list[CartDB],
    response_model_exclude_none=True,
    response_model_exclude_unset=True,

)
async def get_user_cart(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await cart_crud.get_user_cart(
        session=session, user=user
    )


@router.post(
    '/',
    response_model=CartDB,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,

)
async def add_product_to_cart(
        cart: CartCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    product = await check_product_exist(cart.product_id, session)
    cart_position = await check_cart_position_exist(cart.product_id, user, session)

    if cart_position:
        cart_position.quantity += cart.quantity
        await comparison_of_quantity_with_stock(cart_position.quantity, product.in_stock)
        await session.commit()
        await session.refresh(cart_position)
        return cart_position

    await comparison_of_quantity_with_stock(cart.quantity, product.in_stock)
    new_position_in_cart = await cart_crud.create(obj_in=cart, session=session, user=user)
    return new_position_in_cart


@router.delete(
    '/{product_id}',
    response_model=CartDB,
    response_model_exclude_none=True,
)
async def remove_cart_position(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    cart_position = await check_cart_position_exist(product_id, user, session)
    return await cart_crud.remove(cart_position, session)


@router.patch(
    '/{product_id}',
    response_model=CartDB,
    response_model_exclude_none=True,
)
async def update_cart_position(
        product_id: int,
        obj_in: CartUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    cart_position = await check_cart_position_exist(product_id, user, session)
    if not cart_position:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="У вас в корзине нет такого товара!"
        )
    product = await product_crud.get(product_id, session)
    await comparison_of_quantity_with_stock(obj_in.quantity, product.in_stock)

    return await cart_crud.update(cart_position, obj_in, session)
