from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.product import product_crud
from app.models import Product


async def check_name_duplicate(
        product_name: str,
        session: AsyncSession,
) -> None:
    product_id = await product_crud.get_product_id_by_name(
        product_name, session
    )
    if product_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Продукт с таким именем уже существует!',
        )


async def check_product_exist(
        product_id: int,
        session: AsyncSession
) -> Product:
   product = await product_crud.get(
       product_id, session
   )
   if product is None:
       raise HTTPException(
           status_code=HTTPStatus.NOT_FOUND,
           detail='Продукт не найден!'
       )
   return product