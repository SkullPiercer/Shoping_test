from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Product
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.order import order_crud
from app.schemas.order import OrderCreate



router = APIRouter()


@router.post(
    '/',
    response_model=OrderCreate,
    response_model_exclude_none=True,
)
async def create_new_product(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    total_price = await order_crud.calculate_total(user, session)
    new_order = await order_crud.create(user=user, obj_in=total_price, session=session)
    await order_crud.clear_cart(user, session)

    return  {
        "total_price": total_price,
        "status": new_order.status
    }
