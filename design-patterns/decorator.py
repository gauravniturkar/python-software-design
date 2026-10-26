"""
DECORATOR PATTERN
"Wrap an object or function to add behaviour, without changing the original."

Analogy: pizza toppings.
You start with a plain pizza. Add cheese, then olives. Each topping adds to
the price and description, but the base pizza recipe never changes.

Python has two flavours:
  1. The classic OOP decorator: wrapping objects.
  2. Python's @decorator syntax: wrapping functions (used everywhere).
"""
import functools
import time


# ---------------------------------------------------------------------------
# 1. OBJECT DECORATOR: pizza toppings
# ---------------------------------------------------------------------------
class Pizza:
    def cost(self) -> int:
        return 200

    def description(self) -> str:
        return "Plain pizza"


class Topping:
    """Wraps any pizza and behaves like a pizza itself."""

    def __init__(self, pizza, name: str, price: int):
        self.pizza = pizza
        self.name = name
        self.price = price

    def cost(self) -> int:
        return self.pizza.cost() + self.price

    def description(self) -> str:
        return f"{self.pizza.description()} + {self.name}"


# ---------------------------------------------------------------------------
# 2. FUNCTION DECORATOR: add timing and logging to any function
# ---------------------------------------------------------------------------
def log_calls(func):
    @functools.wraps(func)  # keeps the original function's name and docstring
    def wrapper(*args, **kwargs):
        print(f"  -> calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"  <- {func.__name__} returned {result}")
        return result
    return wrapper


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"  {func.__name__} took {elapsed_ms:.2f} ms")
        return result
    return wrapper


@timed
@log_calls  # stacked: timed(log_calls(calculate_bill))
def calculate_bill(amount: float, tip_percent: float) -> float:
    return round(amount * (1 + tip_percent / 100), 2)


if __name__ == "__main__":
    pizza = Pizza()
    pizza = Topping(pizza, "cheese", 50)
    pizza = Topping(pizza, "olives", 30)
    print(f"{pizza.description()} = Rs {pizza.cost()}")

    print("Function decorator:")
    calculate_bill(1000, 10)

# TRADE-OFFS
# + Add features (logging, caching, retries, auth checks) without editing
#   the original code.
# + Mix and match by stacking.
# - Deep stacks are hard to debug ("which wrapper did that?").
# - The order of decorators matters.
