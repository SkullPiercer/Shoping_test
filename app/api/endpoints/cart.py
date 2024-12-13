from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Product
from app.core.db import get_async_session
from app.crud.cart import cart_crud
from app.core.user import current_user, current_superuser
from app.schemas.cart import CartCreate, CartDB
from app.schemas.product import ProductDB
from app.api.validators import (
    check_product_exist,
    comparison_of_quantity_with_stock,
    check_cart_position_exist
)

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
    await comparison_of_quantity_with_stock(cart.quantity, product.in_stock)
    new_position_in_cart = await cart_crud.create(obj_in=cart, session=session, user=user)
    return new_position_in_cart


@router.delete(
    '/{product_id}',
    response_model=CartDB,
    response_model_exclude_none=True,
)
async def remove_project(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    cart_position = await check_cart_position_exist(product_id, user, session)
    return await cart_crud.remove(cart_position, session)
