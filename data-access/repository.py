"""
REPOSITORY PATTERN
"A collection-like object that hides HOW data is stored."

Analogy: a librarian.
You ask "do you have 'Clean Code'?" The librarian knows whether the book is
on shelf 4B, in storage or out on loan. You never deal with shelf numbers.

PROBLEM
SQL strings are scattered across business code. Changing a column name or
moving to another database means editing business logic everywhere, and
testing that logic needs a real database.
"""
import sqlite3
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Customer:
    id: int
    name: str
    city: str


# ---------------------------------------------------------------------------
# BEFORE: SQL mixed straight into the business rule
# ---------------------------------------------------------------------------
def customers_to_invite_before(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT name FROM customers WHERE city = 'Pune'").fetchall()
    return [f"Invite {name}" for (name,) in rows]


# ---------------------------------------------------------------------------
# AFTER: the business rule talks to a repository
# ---------------------------------------------------------------------------
class CustomerRepository(Protocol):
    def add(self, customer: Customer) -> None: ...
    def get(self, customer_id: int) -> Customer | None: ...
    def find_by_city(self, city: str) -> list[Customer]: ...


class SqliteCustomerRepository:
    """Real implementation: the ONLY place that knows the SQL."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, customer: Customer) -> None:
        self.conn.execute(
            "INSERT INTO customers (id, name, city) VALUES (?, ?, ?)",
            (customer.id, customer.name, customer.city),  # "?" prevents SQL injection
        )

    def get(self, customer_id: int) -> Customer | None:
        row = self.conn.execute(
            "SELECT id, name, city FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()
        return Customer(*row) if row else None

    def find_by_city(self, city: str) -> list[Customer]:
        rows = self.conn.execute(
            "SELECT id, name, city FROM customers WHERE city = ?", (city,)
        ).fetchall()
        return [Customer(*row) for row in rows]


class InMemoryCustomerRepository:
    """Fake implementation for tests: just a dictionary."""

    def __init__(self):
        self._data: dict[int, Customer] = {}

    def add(self, customer: Customer) -> None:
        self._data[customer.id] = customer

    def get(self, customer_id: int) -> Customer | None:
        return self._data.get(customer_id)

    def find_by_city(self, city: str) -> list[Customer]:
        return [c for c in self._data.values() if c.city == city]


def customers_to_invite(repo: CustomerRepository, city: str) -> list[str]:
    """Business rule: no SQL, no connection, easy to read."""
    return [f"Invite {c.name}" for c in repo.find_by_city(city)]


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")

    sql_repo = SqliteCustomerRepository(conn)
    sql_repo.add(Customer(1, "Asha", "Pune"))
    sql_repo.add(Customer(2, "Ravi", "Delhi"))
    sql_repo.add(Customer(3, "Meera", "Pune"))

    print("[before]", customers_to_invite_before(conn))
    print("[after] ", customers_to_invite(sql_repo, "Pune"))
    print("[get]   ", sql_repo.get(2))

    # Same business rule, no database at all:
    fake_repo = InMemoryCustomerRepository()
    fake_repo.add(Customer(1, "Test User", "Pune"))
    assert customers_to_invite(fake_repo, "Pune") == ["Invite Test User"]
    print("[test]   in-memory repository works")

# TRADE-OFFS
# + Business code reads like plain English.
# + SQL lives in one place; tests run without a database.
# - Another layer to write. ORMs like SQLAlchemy or Django already act as a
#   kind of repository, so don't wrap them blindly. Add a repository when you
#   want to hide the ORM from business logic or need easy fakes.
