from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.orders import Order, OrderCreate
from app.services.order_service import order_service
from app.observability.prometheus import ORDERS_CREATED_TOTAL, APPLICATION_ERRORS_TOTAL

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_create: OrderCreate) -> Order:
    try:
        order = order_service.create_order(order_create)
        ORDERS_CREATED_TOTAL.inc()
        return order
    except Exception:
        APPLICATION_ERRORS_TOTAL.inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order",
        )


@router.get("/", response_model=List[Order])
async def list_orders() -> List[Order]:
    return order_service.list_orders()


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str) -> Order:
    order = order_service.get_order(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str) -> None:
    deleted = order_service.delete_order(order_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
