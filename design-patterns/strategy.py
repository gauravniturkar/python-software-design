"""
STRATEGY PATTERN
"Put each way of doing a task in its own object, and pick one at runtime."

Analogy: getting to the airport.
The goal is the same (reach the airport), but you can choose a cab, the
metro or a bus depending on time, money and traffic. You can switch your
choice without changing the goal.

PROBLEM
A maps app calculates routes. The route logic for car, bike and walking is
crammed into one function full of if/elif.
"""
from typing import Protocol


# ---------------------------------------------------------------------------
# BEFORE
# ---------------------------------------------------------------------------
def travel_time_before(distance_km: float, mode: str) -> float:
    if mode == "car":
        return distance_km / 40 * 60
    elif mode == "bike":
        return distance_km / 15 * 60
    elif mode == "walk":
        return distance_km / 5 * 60
    raise ValueError("unknown mode")


# ---------------------------------------------------------------------------
# AFTER: each mode is a "strategy"
# ---------------------------------------------------------------------------
class TravelStrategy(Protocol):
    def minutes(self, distance_km: float) -> float: ...


class Car:
    def minutes(self, distance_km: float) -> float:
        return distance_km / 40 * 60


class Bike:
    def minutes(self, distance_km: float) -> float:
        return distance_km / 15 * 60


class Walk:
    def minutes(self, distance_km: float) -> float:
        return distance_km / 5 * 60


class Navigator:
    def __init__(self, strategy: TravelStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: TravelStrategy) -> None:
        self.strategy = strategy  # switch at runtime

    def eta(self, distance_km: float) -> str:
        return f"{self.strategy.minutes(distance_km):.0f} min"


# PYTHON TIP: since a strategy here is just one function, plain functions work
# too. In Python that is often the simplest Strategy pattern.
def metro(distance_km: float) -> float:
    return distance_km / 35 * 60 + 5  # +5 min waiting at the station


if __name__ == "__main__":
    print("[before] car:", travel_time_before(10, "car"))

    nav = Navigator(Car())
    print("[after]  car: ", nav.eta(10))
    nav.set_strategy(Bike())
    print("[after]  bike:", nav.eta(10))
    nav.set_strategy(Walk())
    print("[after]  walk:", nav.eta(10))

    print("[function strategy] metro:", f"{metro(10):.0f} min")

# TRADE-OFFS
# + Add a new mode without touching the Navigator (Open/Closed principle).
# + Each strategy is tiny and testable.
# - More classes. For 2-3 stable options, if/elif is fine.
