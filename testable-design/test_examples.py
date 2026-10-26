"""
Real pytest tests for the examples in this folder.

Run with:   pytest testable-design/

Notice how none of these tests need a database, network, real emails or
waiting for real time to pass. That's what testable design buys you.
"""
from datetime import date

import pytest

from fakes import FakePaymentGateway, InMemorySubscriptionStore, SubscriptionService
from isolating_side_effects import decide_late_fee, process_late_book


# --- Pure logic: just inputs and outputs ------------------------------------
@pytest.mark.parametrize(
    "due, today, expected_fee",
    [
        (date(2026, 1, 10), date(2026, 1, 10), 0),    # returned on time
        (date(2026, 1, 10), date(2026, 1, 11), 5),    # 1 day late
        (date(2026, 1, 10), date(2026, 1, 30), 100),  # 20 days = 100 (the cap)
        (date(2026, 1, 10), date(2026, 6, 1), 100),   # still capped
    ],
)
def test_late_fee(due, today, expected_fee):
    assert decide_late_fee(due, today).fee == expected_fee


def test_shell_sends_email_only_when_late():
    sent = []  # a tiny fake "email sender": just a list
    process_late_book("a@x.com", due=date(2026, 1, 10), today=date(2026, 1, 12), send=sent.append)
    process_late_book("b@x.com", due=date(2026, 1, 10), today=date(2026, 1, 9), send=sent.append)
    assert len(sent) == 1
    assert "a@x.com" in sent[0]


# --- Service with fakes -----------------------------------------------------
@pytest.fixture
def payments():
    return FakePaymentGateway()


@pytest.fixture
def store():
    return InMemorySubscriptionStore()


def test_subscribe_charges_and_activates(payments, store):
    result = SubscriptionService(payments, store).subscribe("u1", "basic")
    assert result == "subscribed to basic"
    assert store.plan_for("u1") == "basic"
    assert payments.charges == [("u1", 199)]


def test_declined_payment_does_not_activate(store):
    declining = FakePaymentGateway(approve=False)
    result = SubscriptionService(declining, store).subscribe("u1", "premium")
    assert result == "payment declined"
    assert store.plan_for("u1") is None


def test_no_double_charge(payments):
    store = InMemorySubscriptionStore({"u1": "premium"})
    SubscriptionService(payments, store).subscribe("u1", "premium")
    assert payments.charges == []
