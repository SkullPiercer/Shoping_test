from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.product import product_crud


async def check_name_duplicate(
        product_name: str,
        session: AsyncSession,
) -> None:
    room_id = await product_crud.get_product_id_by_name(product_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Продукт с таким именем уже существует!',
        )
