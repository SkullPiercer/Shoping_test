from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.models import Product
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB
from app.core.user import current_superuser


router = APIRouter()


@router.post(
    '/',
    response_model=ProductDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """SuperUser only."""
    await check_name_duplicate(product.name, session)
    return await product_crud.create(product, session)


@router.get(
    '/',
    response_model=list[ProductDB],
    response_model_exclude_none=True,
)
async def get_all_product(
        session: AsyncSession = Depends(get_async_session),
) -> list[Product]:
    return await product_crud.get_multi(session=session)
