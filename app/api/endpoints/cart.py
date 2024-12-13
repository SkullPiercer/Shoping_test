from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.crud.cart import cart_crud
from app.core.user import current_user, current_superuser
from app.schemas.cart import CartCreate
from app.schemas.product import ProductDB
from app.api.validators import check_product_exist

router = APIRouter()

@router.get(
    '/',
    response_model=list[ProductDB],
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
    response_model=ProductDB,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,

)
async def add_product_to_cart(
        product: CartCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    a = await check_product_exist(product.product_id, session)
    return a