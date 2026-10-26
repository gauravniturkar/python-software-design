"""
ERROR BOUNDARIES
"Let errors travel up, and catch them at the EDGE of the app."

Analogy: a call-centre escalation.
A junior agent doesn't make up an answer to a hard problem. They escalate it
to the supervisor, who decides what to tell the customer. The customer
gets a polite, clear reply, never internal notes.

PROBLEM
Every function wraps everything in try/except, prints something and returns
None. Errors get swallowed, callers continue with bad data, and nobody knows
what really went wrong.
"""
import logging

logging.basicConfig(level=logging.INFO, format="  [log %(levelname)s] %(message)s")
log = logging.getLogger("shop")


class ValidationError(Exception):
    pass


class NotFound(Exception):
    pass


# ---------------------------------------------------------------------------
# BEFORE: errors swallowed deep inside the code
# ---------------------------------------------------------------------------
def get_price_before(item: str) -> float | None:
    try:
        return {"pen": 10.0}[item]
    except Exception:
        print("something went wrong")  # swallowed! the caller gets None
        return None


def total_before(item: str, qty: int):
    price = get_price_before(item)
    return price * qty  # crashes later with a confusing TypeError


# ---------------------------------------------------------------------------
# AFTER: inner code RAISES clear errors; only the boundary CATCHES them
# ---------------------------------------------------------------------------
PRICES = {"pen": 10.0, "notebook": 45.0}


def get_price(item: str) -> float:
    # Inner layer: no try/except. Just raise clearly.
    if item not in PRICES:
        raise NotFound(f"Item '{item}' not found")
    return PRICES[item]


def calculate_total(item: str, qty: int) -> float:
    if qty <= 0:
        raise ValidationError("Quantity must be at least 1")
    return get_price(item) * qty


def api_handler(request: dict) -> dict:
    """
    THE BOUNDARY: the one place that turns exceptions into responses.
    In FastAPI or Flask this is usually an exception handler or middleware.
    """
    try:
        total = calculate_total(request["item"], int(request["qty"]))
        return {"status": 200, "total": total}
    except ValidationError as error:
        return {"status": 400, "error": str(error)}
    except NotFound as error:
        return {"status": 404, "error": str(error)}
    except Exception:
        # Truly unexpected: log full details for developers,
        # show a safe generic message to users (never leak internals).
        log.exception("Unexpected error for request %s", request)
        return {"status": 500, "error": "Something went wrong. Please try again."}


if __name__ == "__main__":
    try:
        total_before("laptop", 2)
    except TypeError as error:
        print(f"[before] Confusing crash: {error}")

    print("[after]")
    print(api_handler({"item": "pen", "qty": "3"}))
    print(api_handler({"item": "pen", "qty": "0"}))
    print(api_handler({"item": "laptop", "qty": "1"}))
    print(api_handler({"item": "pen", "qty": "three"}))  # unexpected ValueError

# TRADE-OFFS
# + One place decides how errors look to users; inner code stays clean.
# + Bugs aren't hidden, because unexpected errors are logged with a traceback.
# - You still need to catch errors locally when you can genuinely RECOVER
#   (e.g. retry a network call, or fall back to a cache).
