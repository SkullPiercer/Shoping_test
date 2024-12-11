from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB

router = APIRouter()


@router.post(
    '/',
    response_model=ProductDB,
    response_model_exclude_none=True,
)
async def create_new_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(product.name, session)
    return await product_crud.create(product, session)
