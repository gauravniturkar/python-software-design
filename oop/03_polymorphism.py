"""
POLYMORPHISM: different objects answer the same request in their own way.

Analogy: paying at a shop.
The cashier only says "please pay". You might use cash, a card or UPI.
The cashier does not care which. Each method knows how to pay.
"""


# ---------------------------------------------------------------------------
# BEFORE: the checkout has to know every payment type
# ---------------------------------------------------------------------------
def checkout_before(method: str, amount: float) -> str:
    # Every new payment type means editing this function again.
    if method == "cash":
        return f"Received {amount} in cash"
    elif method == "card":
        return f"Charged {amount} to card"
    elif method == "upi":
        return f"Requested {amount} via UPI"
    else:
        raise ValueError(f"Unknown method {method}")


# ---------------------------------------------------------------------------
# AFTER: every payment type has the same method, `pay`
# ---------------------------------------------------------------------------
class Cash:
    def pay(self, amount: float) -> str:
        return f"Received {amount} in cash"


class Card:
    def __init__(self, last_four: str):
        self.last_four = last_four

    def pay(self, amount: float) -> str:
        return f"Charged {amount} to card ending {self.last_four}"


class Upi:
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> str:
        return f"Requested {amount} from {self.upi_id}"


def checkout(payment_method, amount: float) -> str:
    # The checkout just says "pay". It does not check the type.
    return payment_method.pay(amount)


if __name__ == "__main__":
    print("[before]", checkout_before("card", 250))

    for method in [Cash(), Card("4242"), Upi("asha@bank")]:
        print("[after] ", checkout(method, 250))

# Adding a new type (e.g. GiftCard) means writing a new class with `pay`.
# The checkout function does not change at all.
#
# TRADE-OFFS
# + New behaviour is added by writing new classes, not editing old code.
# + Each class is small and easy to test.
# - For two or three fixed cases that never change, the if/else version is
#   perfectly fine and easier to read.
