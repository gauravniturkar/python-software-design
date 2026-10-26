"""
MEANINGFUL (CUSTOM) EXCEPTIONS
"Name the problem precisely, so the right person can react correctly."

Analogy: a car dashboard.
A single "something is wrong" light is useless. Separate lights for
"low fuel", "engine hot" and "door open" tell you exactly what to do.

PROBLEM
Code raises a generic Exception("error") for everything. Callers can't tell
"out of stock" (show a message) from "database down" (retry / alert ops).
"""


# ---------------------------------------------------------------------------
# BEFORE: generic errors, so the caller has to read strings to guess
# ---------------------------------------------------------------------------
def place_order_before(item: str, qty: int, stock: dict[str, int]) -> str:
    if item not in stock:
        raise Exception("error")             # what error??
    if stock[item] < qty:
        raise Exception("not enough")        # the caller has to match strings
    return "ok"


# ---------------------------------------------------------------------------
# AFTER: a small family of exceptions
# ---------------------------------------------------------------------------
class ShopError(Exception):
    """Base class: catch this to handle ANY shop problem in one place."""


class ProductNotFound(ShopError):
    def __init__(self, item: str):
        super().__init__(f"Product '{item}' does not exist")
        self.item = item


class InsufficientStock(ShopError):
    def __init__(self, item: str, requested: int, available: int):
        super().__init__(f"Only {available} '{item}' left, you asked for {requested}")
        # Extra data the caller can use (e.g. "buy 3 instead?")
        self.item = item
        self.requested = requested
        self.available = available


class PaymentFailed(ShopError):
    pass


def place_order(item: str, qty: int, stock: dict[str, int]) -> str:
    if item not in stock:
        raise ProductNotFound(item)
    if stock[item] < qty:
        raise InsufficientStock(item, qty, stock[item])
    return f"Ordered {qty} x {item}"


def charge_card(card_number: str) -> None:
    try:
        int(card_number)  # pretend this calls a payment gateway
    except ValueError as error:
        # Wrap a low-level error in a domain error, but KEEP the original
        # cause with `from error` so debugging still shows the root problem.
        raise PaymentFailed("Card number is invalid") from error


if __name__ == "__main__":
    stock = {"pen": 10, "notebook": 2}

    for item, qty in [("pen", 3), ("notebook", 5), ("laptop", 1)]:
        try:
            print(place_order(item, qty, stock))
        except InsufficientStock as error:
            # Specific handling: offer what's available.
            print(f"{error} -> Suggest buying {error.available} instead")
        except ProductNotFound as error:
            print(f"{error} -> Show similar products")

    try:
        charge_card("12AB")
    except PaymentFailed as error:
        print(f"{error} (caused by: {error.__cause__!r})")

    # Catching the base class handles every shop error at once:
    try:
        place_order("laptop", 1, stock)
    except ShopError as error:
        print(f"Generic shop handler: {error}")

# TRADE-OFFS
# + Callers react precisely; logs are clear; tests can assert exact errors.
# - A few extra classes. Don't create one per line of code. Create one per
#   situation a caller would handle DIFFERENTLY.
