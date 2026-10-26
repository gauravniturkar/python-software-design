"""
CASE STUDY: ORDER PROCESSING

Everyday picture: an online shop's checkout counter.
  1. Check the items are in stock.
  2. Take the payment.
  3. Reduce stock and save the order (together, or not at all).
  4. Send a confirmation.
If payment fails, nothing is saved and no stock is lost.

Concepts used
  Layered architecture (architecture/)    -> API -> service -> repositories
  Repository + Unit of Work (data-access/) -> all-or-nothing saving
  Custom exceptions + boundary (error-handling/)
  DI + fakes (dependency-injection/, testable-design/)
  Observer-style notification after success (design-patterns/)
"""
from dataclasses import dataclass, field
from typing import Callable, Protocol


# ===========================================================================
# DOMAIN: data and errors
# ===========================================================================
@dataclass
class OrderLine:
    sku: str
    qty: int


@dataclass
class Order:
    id: str
    customer: str
    lines: list[OrderLine]
    total: int


class OrderError(Exception):
    """Base class for problems the customer should hear about."""


class OutOfStock(OrderError):
    pass


class PaymentDeclined(OrderError):
    pass


# ===========================================================================
# PORTS: what the service needs
# ===========================================================================
class PaymentGateway(Protocol):
    def charge(self, customer: str, amount: int) -> bool: ...


class UnitOfWork(Protocol):
    stock: dict[str, int]
    prices: dict[str, int]
    orders: dict[str, Order]

    def __enter__(self) -> "UnitOfWork": ...
    def __exit__(self, *args) -> None: ...
    def commit(self) -> None: ...


# ===========================================================================
# SERVICE LAYER: the checkout rules
# ===========================================================================
class CheckoutService:
    def __init__(self, uow: UnitOfWork, payments: PaymentGateway,
                 on_order_placed: list[Callable[[Order], None]] | None = None):
        self.uow = uow
        self.payments = payments
        self.on_order_placed = on_order_placed or []
        self._next_id = 1

    def place_order(self, customer: str, lines: list[OrderLine]) -> Order:
        with self.uow as uow:
            # 1. Check stock
            for line in lines:
                if uow.stock.get(line.sku, 0) < line.qty:
                    raise OutOfStock(f"Not enough '{line.sku}' in stock")

            # 2. Take payment
            total = sum(uow.prices[line.sku] * line.qty for line in lines)
            if not self.payments.charge(customer, total):
                raise PaymentDeclined("Your card was declined")

            # 3. Reduce stock and save the order
            for line in lines:
                uow.stock[line.sku] -= line.qty
            order = Order(f"ORD-{self._next_id}", customer, lines, total)
            uow.orders[order.id] = order
            uow.commit()  # all-or-nothing
            self._next_id += 1

        # 4. Notify listeners only AFTER a successful commit
        for listener in self.on_order_placed:
            listener(order)
        return order


# ===========================================================================
# ADAPTERS / FAKES (in-memory, so the demo needs nothing installed)
# ===========================================================================
class InMemoryUnitOfWork:
    """
    Works on COPIES of the data, and only replaces the real data on commit.
    That gives the same all-or-nothing effect as a database transaction.
    """

    def __init__(self, stock: dict[str, int], prices: dict[str, int]):
        self._stock, self._orders = stock, {}
        self.prices = prices

    def __enter__(self):
        self.stock = dict(self._stock)
        self.orders = dict(self._orders)
        self._committed = False
        return self

    def commit(self) -> None:
        self._stock.clear()
        self._stock.update(self.stock)
        self._orders = dict(self.orders)
        self._committed = True

    def __exit__(self, *args) -> None:
        if not self._committed:
            # Rollback: throw the working copies away
            self.stock = dict(self._stock)
            self.orders = dict(self._orders)

    @property
    def saved_orders(self) -> dict[str, Order]:
        return self._orders


@dataclass
class FakePayments:
    declined_customers: set[str] = field(default_factory=set)

    def charge(self, customer: str, amount: int) -> bool:
        return customer not in self.declined_customers


# ===========================================================================
# API LAYER (the error boundary)
# ===========================================================================
def checkout_endpoint(service: CheckoutService, request: dict) -> dict:
    try:
        lines = [OrderLine(sku, qty) for sku, qty in request["items"].items()]
        order = service.place_order(request["customer"], lines)
        return {"status": 201, "order_id": order.id, "total": order.total}
    except OutOfStock as error:
        return {"status": 409, "error": str(error)}
    except PaymentDeclined as error:
        return {"status": 402, "error": str(error)}


if __name__ == "__main__":
    stock = {"tshirt": 5, "mug": 1}
    uow = InMemoryUnitOfWork(stock, prices={"tshirt": 499, "mug": 299})
    service = CheckoutService(
        uow,
        FakePayments(declined_customers={"ravi"}),
        on_order_placed=[lambda o: print(f"  [email] Thanks {o.customer}! Order {o.id} confirmed.")],
    )

    print(checkout_endpoint(service, {"customer": "asha", "items": {"tshirt": 2, "mug": 1}}))
    print("  stock now:", stock)

    print(checkout_endpoint(service, {"customer": "meera", "items": {"mug": 1}}))
    print("  stock now:", stock)

    print(checkout_endpoint(service, {"customer": "ravi", "items": {"tshirt": 1}}))
    print("  stock now:", stock, "<- unchanged, payment failed so nothing was saved")

    print("Saved orders:", list(uow.saved_orders))

# EXERCISE
#   1. Swap InMemoryUnitOfWork for a SQLite version (see data-access/unit_of_work.py).
#   2. What if payment succeeds but commit() fails? Real systems refund the payment
#      or charge only after saving the order as "pending". Try to model that.
