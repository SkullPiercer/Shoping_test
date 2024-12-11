from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Product


class CRUDProducts(CRUDBase):
    async def get_product_id_by_name(
            self,
            product_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(Product.id).where(
                Product.name == product_name
            )
        )
        return db_project_id.scalars().first()


product_crud = CRUDProducts(Product)
