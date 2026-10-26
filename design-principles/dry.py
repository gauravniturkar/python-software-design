"""
DRY - DON'T REPEAT YOURSELF
"Every piece of knowledge should have one home."

Analogy: your phone's contact list.
If a friend changes their number, you update ONE contact. If you had written
it on ten sticky notes, you'd surely forget to update one of them.

PROBLEM
The same GST rule is copied into three functions. When the rate changes,
someone updates two and forgets the third, and the bills don't match.
"""

# ---------------------------------------------------------------------------
# BEFORE: the same rule copied three times
# ---------------------------------------------------------------------------
def cart_total_before(prices: list[float]) -> float:
    return sum(prices) * 1.18


def invoice_total_before(prices: list[float]) -> float:
    return sum(prices) * 1.18


def refund_amount_before(prices: list[float]) -> float:
    return sum(prices) * 1.12  # <-- someone forgot to update this copy!


# ---------------------------------------------------------------------------
# AFTER: one home for the rule
# ---------------------------------------------------------------------------
GST_RATE = 0.18


def with_gst(amount: float) -> float:
    """The ONLY place that knows how GST is applied."""
    return amount * (1 + GST_RATE)


def cart_total(prices: list[float]) -> float:
    return with_gst(sum(prices))


def invoice_total(prices: list[float]) -> float:
    return with_gst(sum(prices))


def refund_amount(prices: list[float]) -> float:
    return with_gst(sum(prices))


if __name__ == "__main__":
    prices = [100, 200]
    print("[before]", cart_total_before(prices), refund_amount_before(prices), "<-- mismatch")
    print("[after] ", cart_total(prices), refund_amount(prices))

# CAREFUL: DRY is about duplicated KNOWLEDGE, not duplicated-looking CODE.
#   validate_username() and validate_city() might both check "len > 2" today,
#   but they are different rules that may change for different reasons.
#   Merging them into one function would tie them together by accident.
#
# TRADE-OFFS
# + One change, one place, no forgotten copies.
# - Shared code creates a dependency; changing it affects every user.
# - A little duplication is better than the wrong abstraction.
