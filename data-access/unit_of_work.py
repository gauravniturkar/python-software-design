"""
UNIT OF WORK PATTERN
"Group several changes so they ALL succeed or ALL fail together."

Analogy: a bank transfer.
Moving Rs 500 from Asha to Ravi is TWO steps: debit Asha, credit Ravi.
If the system crashes in between, Asha loses money and Ravi gets nothing.
A Unit of Work makes both steps one package: done completely, or not at all.

In databases this is a TRANSACTION (commit / rollback). The Unit of Work
pattern wraps it in a clean object so business code doesn't call
conn.commit() and conn.rollback() everywhere.
"""
import sqlite3


class AccountRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def balance(self, name: str) -> int:
        return self.conn.execute("SELECT balance FROM accounts WHERE name = ?", (name,)).fetchone()[0]

    def change_balance(self, name: str, delta: int) -> None:
        self.conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (delta, name))


class UnitOfWork:
    """
    Used with `with`:
        with UnitOfWork(conn) as uow:
            uow.accounts.change_balance(...)
            uow.commit()
    If an error happens, or commit() is never called, everything is undone.
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.accounts = AccountRepository(conn)
        self._committed = False

    def __enter__(self) -> "UnitOfWork":
        return self

    def commit(self) -> None:
        self.conn.commit()
        self._committed = True

    def __exit__(self, exc_type, exc, tb) -> None:
        if not self._committed:
            self.conn.rollback()  # safety net: undo half-finished work


class InsufficientFunds(Exception):
    pass


def transfer(uow: UnitOfWork, sender: str, receiver: str, amount: int, crash_midway: bool = False) -> None:
    with uow:
        uow.accounts.change_balance(sender, -amount)    # step 1: debit
        if crash_midway:
            raise RuntimeError("Server crashed after debit!")
        if uow.accounts.balance(sender) < 0:
            raise InsufficientFunds(f"{sender} doesn't have {amount}")
        uow.accounts.change_balance(receiver, amount)   # step 2: credit
        uow.commit()                                    # both steps saved together


def show(conn: sqlite3.Connection, label: str) -> None:
    rows = conn.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall()
    print(f"{label:<28} {dict(rows)}")


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER)")
    conn.executemany("INSERT INTO accounts VALUES (?, ?)", [("Asha", 1000), ("Ravi", 200)])
    conn.commit()
    show(conn, "Start:")

    transfer(UnitOfWork(conn), "Asha", "Ravi", 500)
    show(conn, "After transfer 500:")

    try:
        transfer(UnitOfWork(conn), "Asha", "Ravi", 100, crash_midway=True)
    except RuntimeError as error:
        print(f"  ! {error}")
    show(conn, "After crash (rolled back):")

    try:
        transfer(UnitOfWork(conn), "Ravi", "Asha", 5000)
    except InsufficientFunds as error:
        print(f"  ! {error}")
    show(conn, "After failed transfer:")

# TRADE-OFFS
# + No more half-saved data: money never disappears.
# + Business code just says "commit" once; rollback is automatic.
# - Adds another object. Many ORMs (SQLAlchemy Session, Django
#   transaction.atomic) already give you this; use theirs when available.
