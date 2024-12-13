from fastapi import APIRouter

from app.api.endpoints import user_router, product_router, cart_router, order_router

main_router = APIRouter()
main_router.include_router(
    product_router, prefix='/products', tags=['Products']
)
main_router.include_router(
    cart_router, prefix='/cart', tags=['Cart']
)
main_router.include_router(
    order_router, prefix='/checkout', tags=['Order']
)
main_router.include_router(user_router)
