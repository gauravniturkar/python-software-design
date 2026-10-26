"""
D - DEPENDENCY INVERSION PRINCIPLE (DIP)
"Important code should depend on an idea (abstraction), not on a specific tool."

Analogy: a wall socket.
Your lamp plugs into a standard socket. The lamp doesn't care whether the
power comes from solar, coal or a generator. Both the lamp and the power
source agree on the same "socket shape" (the abstraction).

PROBLEM
An order service creates a MySQL database object inside itself. Switching to
another database, or testing without a real database, means rewriting it.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BEFORE: high-level code is welded to a low-level detail
# ---------------------------------------------------------------------------
class MySQLDatabase:
    def save(self, data: dict) -> None:
        print(f"[MySQL] INSERT {data}")


class OrderServiceBefore:
    def __init__(self):
        self.db = MySQLDatabase()  # hard-wired: can't swap or fake it

    def place_order(self, item: str) -> None:
        self.db.save({"item": item})


# ---------------------------------------------------------------------------
# AFTER: both sides depend on the same abstraction ("the socket")
# ---------------------------------------------------------------------------
class OrderStorage(ABC):
    """The 'socket shape'. The order service only knows about this."""

    @abstractmethod
    def save(self, data: dict) -> None: ...


class MySQLStorage(OrderStorage):
    def save(self, data: dict) -> None:
        print(f"[MySQL] INSERT {data}")


class MongoStorage(OrderStorage):
    def save(self, data: dict) -> None:
        print(f"[Mongo] insert_one {data}")


class InMemoryStorage(OrderStorage):
    """Perfect for tests: no real database needed."""

    def __init__(self):
        self.saved: list[dict] = []

    def save(self, data: dict) -> None:
        self.saved.append(data)


class OrderService:
    def __init__(self, storage: OrderStorage):
        self.storage = storage  # handed in from outside (see dependency-injection/)

    def place_order(self, item: str) -> None:
        self.storage.save({"item": item})


if __name__ == "__main__":
    OrderServiceBefore().place_order("Laptop")

    OrderService(MySQLStorage()).place_order("Laptop")
    OrderService(MongoStorage()).place_order("Laptop")

    fake = InMemoryStorage()
    OrderService(fake).place_order("Laptop")
    print("[test] saved in memory:", fake.saved)

# TRADE-OFFS
# + Swap databases, email providers, payment gateways... without touching
#   business logic.
# + Testing becomes easy because you can plug in a fake.
# - One extra abstraction to maintain.
# - If there will only ever be one implementation and you don't need to test
#   it in isolation, the abstraction may be unnecessary.
