import threading
from typing import Optional

from app.schemas.orders import Order, OrderCreate


class OrderService:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}
        self._lock = threading.Lock()

    def create_order(self, order_create: OrderCreate) -> Order:
        order = Order(**order_create.model_dump())
        with self._lock:
            self._orders[order.id] = order
        return order

    def list_orders(self) -> list[Order]:
        with self._lock:
            return list(self._orders.values())

    def get_order(self, order_id: str) -> Optional[Order]:
        with self._lock:
            return self._orders.get(order_id)

    def delete_order(self, order_id: str) -> bool:
        with self._lock:
            if order_id in self._orders:
                del self._orders[order_id]
                return True
            return False

    def order_count(self) -> int:
        with self._lock:
            return len(self._orders)


order_service = OrderService()
