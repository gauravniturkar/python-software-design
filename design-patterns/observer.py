"""
OBSERVER PATTERN
"When something happens, automatically notify everyone who is interested."

Analogy: subscribing to a YouTube channel.
The creator uploads a video once. Every subscriber gets notified. The creator
doesn't phone each subscriber, and new subscribers can join at any time.

PROBLEM
When an order is placed we must send an email, update inventory and log
analytics. Hard-coding all three into `place_order` means editing it every
time a team wants to react to new orders.
"""
from typing import Callable


# ---------------------------------------------------------------------------
# BEFORE: the order code knows about every follow-up task
# ---------------------------------------------------------------------------
def place_order_before(order_id: str) -> None:
    print(f"Order {order_id} placed")
    print(f"  email: confirmation sent for {order_id}")
    print(f"  inventory: stock reduced for {order_id}")
    print(f"  analytics: recorded {order_id}")
    # New requirement "send SMS too" -> edit this function again


# ---------------------------------------------------------------------------
# AFTER: the order code just announces "an order was placed"
# ---------------------------------------------------------------------------
class OrderEvents:
    """The 'channel'. Listeners subscribe; the publisher notifies them."""

    def __init__(self):
        self._subscribers: list[Callable[[str], None]] = []

    def subscribe(self, callback: Callable[[str], None]) -> None:
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str], None]) -> None:
        self._subscribers.remove(callback)

    def publish(self, order_id: str) -> None:
        for callback in self._subscribers:
            callback(order_id)


# Subscribers: each one cares about one thing.
def send_email(order_id: str) -> None:
    print(f"  email: confirmation sent for {order_id}")


def update_inventory(order_id: str) -> None:
    print(f"  inventory: stock reduced for {order_id}")


def record_analytics(order_id: str) -> None:
    print(f"  analytics: recorded {order_id}")


def place_order(events: OrderEvents, order_id: str) -> None:
    print(f"Order {order_id} placed")
    events.publish(order_id)  # "Hey everyone, this happened!"


if __name__ == "__main__":
    place_order_before("A-1")

    events = OrderEvents()
    events.subscribe(send_email)
    events.subscribe(update_inventory)
    events.subscribe(record_analytics)
    place_order(events, "A-2")

    # New requirement: send an SMS. No change to place_order needed.
    events.subscribe(lambda order_id: print(f"  sms: sent for {order_id}"))
    events.unsubscribe(record_analytics)
    place_order(events, "A-3")

# TRADE-OFFS
# + Publishers and subscribers don't know about each other.
# + Add or remove reactions without touching the core code.
# - Harder to see the whole flow ("what happens when an order is placed?").
# - If one subscriber crashes, the others may not run. Decide how to handle
#   errors (see error-handling/).
