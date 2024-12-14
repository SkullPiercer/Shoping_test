from app.crud.order import order_crud
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.post(
    '/',
)
async def checkout(
    session: AsyncSession =Depends(get_async_session),
    user: User = Depends(current_user)
):
    order = await order_crud.create_order(session=session, user=user)
    return order