"""
LIGHTWEIGHT FAKES
"A small, working stand-in for a real dependency, used in tests."

Analogy: a crash-test dummy.
Car makers don't crash cars with real people inside. A dummy has the same
size and weight as a person, which is good enough to test the seatbelt.

A fake is a SIMPLE but REAL implementation (e.g. a dict instead of a database).
Unlike a mock, it actually works, so tests check RESULTS, not method calls.
"""
from dataclasses import dataclass, field
from typing import Protocol


# ---------------------------------------------------------------------------
# The code under test
# ---------------------------------------------------------------------------
class PaymentGateway(Protocol):
    def charge(self, user_id: str, amount: int) -> bool: ...


class SubscriptionStore(Protocol):
    def activate(self, user_id: str, plan: str) -> None: ...
    def plan_for(self, user_id: str) -> str | None: ...


class SubscriptionService:
    PRICES = {"basic": 199, "premium": 499}

    def __init__(self, payments: PaymentGateway, store: SubscriptionStore):
        self.payments = payments
        self.store = store

    def subscribe(self, user_id: str, plan: str) -> str:
        if self.store.plan_for(user_id) == plan:
            return "already subscribed"
        if not self.payments.charge(user_id, self.PRICES[plan]):
            return "payment declined"
        self.store.activate(user_id, plan)
        return f"subscribed to {plan}"


# ---------------------------------------------------------------------------
# FAKES: tiny, readable, no network or database
# ---------------------------------------------------------------------------
@dataclass
class FakePaymentGateway:
    approve: bool = True                        # flip to simulate declines
    charges: list[tuple[str, int]] = field(default_factory=list)

    def charge(self, user_id: str, amount: int) -> bool:
        self.charges.append((user_id, amount))  # remember what happened
        return self.approve


@dataclass
class InMemorySubscriptionStore:
    plans: dict[str, str] = field(default_factory=dict)

    def activate(self, user_id: str, plan: str) -> None:
        self.plans[user_id] = plan

    def plan_for(self, user_id: str) -> str | None:
        return self.plans.get(user_id)


if __name__ == "__main__":
    # Scenario 1: happy path
    payments, store = FakePaymentGateway(), InMemorySubscriptionStore()
    service = SubscriptionService(payments, store)
    print(service.subscribe("u1", "premium"))
    assert store.plan_for("u1") == "premium"
    assert payments.charges == [("u1", 499)]

    # Scenario 2: card declined. Easy to simulate with a fake!
    payments, store = FakePaymentGateway(approve=False), InMemorySubscriptionStore()
    service = SubscriptionService(payments, store)
    print(service.subscribe("u2", "basic"))
    assert store.plan_for("u2") is None

    # Scenario 3: already subscribed, so no double charge
    payments, store = FakePaymentGateway(), InMemorySubscriptionStore({"u3": "basic"})
    service = SubscriptionService(payments, store)
    print(service.subscribe("u3", "basic"))
    assert payments.charges == []

    print("All fake-based checks passed")

# TRADE-OFFS
# + Fast, reliable tests that read like real scenarios.
# + Reusable across many tests.
# - Fakes must stay in sync with the real behaviour. Keep them simple and
#   add a few integration tests against the real thing too.
