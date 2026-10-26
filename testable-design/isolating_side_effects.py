"""
ISOLATING SIDE EFFECTS
"Separate THINKING (pure logic) from DOING (I/O, clock, randomness, network)."

Analogy: a recipe vs cooking.
Writing a recipe ("double the sugar for 8 people") is pure thinking. You can
check it on paper. Actually cooking needs a stove, gas and ingredients.
Test the recipe on paper; only cook when you need to.

A SIDE EFFECT is anything that touches the outside world:
  reading or writing files, network calls, databases, printing,
  reading the current time, generating random numbers.

PROBLEM
A late-fee function reads today's date and sends an email. To test the
"10 days late" case you'd have to wait 10 days, and you'd send real emails.
"""
from dataclasses import dataclass
from datetime import date


# ---------------------------------------------------------------------------
# BEFORE: logic and side effects tangled
# ---------------------------------------------------------------------------
def process_late_book_before(borrower_email: str, due: date) -> None:
    today = date.today()                         # side effect: real clock
    days_late = (today - due).days
    fee = 0 if days_late <= 0 else min(days_late * 5, 100)
    if fee > 0:
        print(f"[REAL EMAIL] to {borrower_email}: you owe Rs {fee}")  # side effect


# ---------------------------------------------------------------------------
# AFTER: "functional core, imperative shell"
# ---------------------------------------------------------------------------
@dataclass
class LateFeeDecision:
    days_late: int
    fee: int
    should_notify: bool


def decide_late_fee(due: date, today: date) -> LateFeeDecision:
    """
    PURE FUNCTION (the core): same inputs always give the same output.
    No clock, no email, no printing. Trivial to test.
    Rule: Rs 5 per day late, capped at Rs 100.
    """
    days_late = max((today - due).days, 0)
    fee = min(days_late * 5, 100)
    return LateFeeDecision(days_late, fee, should_notify=fee > 0)


def process_late_book(borrower_email: str, due: date, today: date | None = None, send=print) -> None:
    """
    THE SHELL: a thin wrapper that gathers inputs and performs side effects.
    It has almost no logic, so it barely needs testing.
    """
    decision = decide_late_fee(due, today or date.today())
    if decision.should_notify:
        send(f"[EMAIL] to {borrower_email}: {decision.days_late} days late, you owe Rs {decision.fee}")


if __name__ == "__main__":
    process_late_book_before("asha@example.com", date(2026, 1, 1))

    # Testing the core: any date we want, instantly, no emails.
    assert decide_late_fee(date(2026, 1, 10), date(2026, 1, 10)).fee == 0     # on time
    assert decide_late_fee(date(2026, 1, 10), date(2026, 1, 13)).fee == 15    # 3 days
    assert decide_late_fee(date(2026, 1, 10), date(2026, 3, 1)).fee == 100    # capped
    assert decide_late_fee(date(2026, 1, 10), date(2026, 1, 5)).fee == 0      # early return
    print("Core logic tests passed")

    # Running the shell for real:
    process_late_book("asha@example.com", due=date(2026, 1, 10), today=date(2026, 1, 14))

# TRADE-OFFS
# + Most of your logic becomes pure and testable in milliseconds.
# + Bugs are easier to reproduce: just pass the same inputs.
# - You have to think about where the boundary between core and shell goes.
