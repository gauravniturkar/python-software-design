"""
KISS - KEEP IT SIMPLE, STUPID
"Pick the simplest solution that solves the problem."

Analogy: boiling water.
You use a kettle. You don't build an app-controlled kitchen robot.
Both boil water, but one is far easier to fix when something goes wrong.

PROBLEM
A task needs "is this year a leap year?". Someone builds a framework for it.
"""

# ---------------------------------------------------------------------------
# BEFORE: over-engineered
# ---------------------------------------------------------------------------
class YearRule:
    def matches(self, year: int) -> bool: ...


class DivisibleBy(YearRule):
    def __init__(self, n: int):
        self.n = n

    def matches(self, year: int) -> bool:
        return year % self.n == 0


class LeapYearRuleEngine:
    def __init__(self):
        self.rules = [
            (DivisibleBy(400), True),
            (DivisibleBy(100), False),
            (DivisibleBy(4), True),
        ]

    def evaluate(self, year: int) -> bool:
        for rule, result in self.rules:
            if rule.matches(year):
                return result
        return False


# ---------------------------------------------------------------------------
# AFTER: one clear function
# ---------------------------------------------------------------------------
def is_leap_year(year: int) -> bool:
    # Divisible by 4, except centuries, unless the century is divisible by 400.
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


if __name__ == "__main__":
    engine = LeapYearRuleEngine()
    for year in [1900, 2000, 2024, 2025]:
        print(year, "before:", engine.evaluate(year), "| after:", is_leap_year(year))

# Even better: Python already has it -> calendar.isleap(year)
#
# TRADE-OFFS
# + Simple code is quicker to read, review, debug and hand over.
# - "Simple" isn't "careless". Still handle real edge cases.
# - Add structure when the problem actually grows, not before.
