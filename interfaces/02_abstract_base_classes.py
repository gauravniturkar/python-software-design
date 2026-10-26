"""
ABSTRACT BASE CLASSES (ABC)
"A parent class that says: every child MUST implement these methods."

Analogy: a franchise rulebook.
Every outlet of a pizza chain must offer `take_order()` and `deliver()`.
You can't open an outlet that skips one. Head office won't let you start.

Python enforces the rule when you try to CREATE an object. If a required
method is missing, you get an error immediately instead of a surprise later.
"""
from abc import ABC, abstractmethod


class PizzaOutlet(ABC):
    """The contract every outlet must follow."""

    @abstractmethod
    def take_order(self, pizza: str) -> str: ...

    @abstractmethod
    def deliver(self, address: str) -> str: ...

    # ABCs can also share ready-made behaviour with every child.
    def greet(self) -> str:
        return "Welcome to PizzaCo!"


class MumbaiOutlet(PizzaOutlet):
    def take_order(self, pizza: str) -> str:
        return f"Mumbai: preparing {pizza}"

    def deliver(self, address: str) -> str:
        return f"Mumbai: delivering by scooter to {address}"


class LazyOutlet(PizzaOutlet):
    def take_order(self, pizza: str) -> str:
        return f"Lazy: preparing {pizza}"
    # forgot to implement deliver()!


if __name__ == "__main__":
    outlet = MumbaiOutlet()
    print(outlet.greet())
    print(outlet.take_order("Margherita"))
    print(outlet.deliver("Bandra"))

    try:
        LazyOutlet()  # fails right here, before any customer is affected
    except TypeError as error:
        print(f"Blocked at creation: {error}")

    try:
        PizzaOutlet()  # the rulebook itself can't be an outlet
    except TypeError as error:
        print(f"Blocked at creation: {error}")

# TRADE-OFFS
# + Missing methods are caught early and loudly.
# + The contract is written down in one obvious place.
# + Can share common helper methods (like `greet`).
# - Implementations must inherit from the ABC, so it can't describe
#   third-party classes you don't control. Use a Protocol for that.
