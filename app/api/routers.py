from fastapi import APIRouter

from app.api.endpoints import user_router, product_router

main_router = APIRouter()
main_router.include_router(
    product_router, prefix='/products', tags=['Products']
)
main_router.include_router(user_router)
