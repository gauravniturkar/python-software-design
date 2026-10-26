"""
O - OPEN/CLOSED PRINCIPLE (OCP)
"Code should be open for extension but closed for modification."

Analogy: a smartphone.
When you want a new feature, you install an app. You don't open the phone
and resolder its circuits. The phone is "closed" (stable) but "open" to apps.

PROBLEM
A shop calculates discounts. Every new festival offer means editing the same
function, which grows longer and riskier with every if/elif.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BEFORE: every new discount means editing this function
# ---------------------------------------------------------------------------
def discounted_price_before(price: float, discount_type: str) -> float:
    if discount_type == "none":
        return price
    elif discount_type == "diwali":
        return price * 0.80
    elif discount_type == "student":
        return price - 100
    # Next month: "black_friday" -> edit again, retest everything again...
    raise ValueError("Unknown discount")


# ---------------------------------------------------------------------------
# AFTER: new discounts are new classes; the checkout never changes
# ---------------------------------------------------------------------------
class Discount(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...


class NoDiscount(Discount):
    def apply(self, price: float) -> float:
        return price


class PercentageDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FlatDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, price: float) -> float:
        return max(price - self.amount, 0)  # never go below zero


def checkout(price: float, discount: Discount) -> float:
    # "Closed": this function does not change when new discounts appear.
    return discount.apply(price)


# EXTENSION: added later without touching anything above.
class BuyMoreSaveMore(Discount):
    def apply(self, price: float) -> float:
        return price * 0.70 if price > 5000 else price


if __name__ == "__main__":
    print("[before] diwali:", discounted_price_before(1000, "diwali"))

    offers = {
        "none": NoDiscount(),
        "diwali 20%": PercentageDiscount(20),
        "student flat 100": FlatDiscount(100),
        "buy more save more": BuyMoreSaveMore(),
    }
    for name, offer in offers.items():
        print(f"[after]  {name:<20} -> {checkout(6000, offer):.2f}")

# TRADE-OFFS
# + Adding a discount never risks breaking an existing one.
# + Each discount can be tested by itself.
# - More classes than a single if/elif.
# - If you only ever have two discount types, the if/elif is simpler.
#   Use OCP when you can see the list keeps growing.
