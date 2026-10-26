"""
AFTER REFACTORING: same behaviour, much clearer.

Steps taken (each one small and checked with tests):
  1. RENAME:            t, a, d, r -> ticket_type, age, day, recliner
  2. NAME MAGIC NUMBERS: 0.5 -> CHILD_DISCOUNT, 50 -> TUESDAY_OFFER, ...
  3. LOOKUP TABLE:      if/elif on ticket type -> BASE_PRICES dictionary
  4. EXTRACT FUNCTION:  repeated age logic -> age_multiplier()
  5. GUARD CLAUSE:      unknown type handled first, at the top
  6. KEEP QUIRKS:       the old code returns -1 for unknown types and
                        doesn't give the Tuesday offer on IMAX. Refactoring
                        must NOT change that, even if it looks odd.
                        Changing behaviour is a separate, deliberate decision.
"""

BASE_PRICES = {"2d": 200, "3d": 300, "imax": 450}
TUESDAY_OFFER_TYPES = {"2d", "3d"}

CHILD_MAX_AGE = 12      # under 12
SENIOR_MIN_AGE = 60     # 60 and above
CHILD_DISCOUNT = 0.5    # pay 50%
SENIOR_DISCOUNT = 0.8   # pay 80%
TUESDAY_OFFER = 50      # Rs off
RECLINER_SURCHARGE = 150
UNKNOWN_TICKET = -1     # kept for backward compatibility with callers


def age_multiplier(age: int) -> float:
    if age < CHILD_MAX_AGE:
        return CHILD_DISCOUNT
    if age >= SENIOR_MIN_AGE:
        return SENIOR_DISCOUNT
    return 1.0


def ticket_price(ticket_type: str, age: int, day: str, recliner: bool) -> float:
    if ticket_type not in BASE_PRICES:
        return UNKNOWN_TICKET

    price = BASE_PRICES[ticket_type] * age_multiplier(age)

    if day == "tue" and ticket_type in TUESDAY_OFFER_TYPES:
        price -= TUESDAY_OFFER
    if recliner:
        price += RECLINER_SURCHARGE

    return max(price, 0)


if __name__ == "__main__":
    print(ticket_price("2d", 30, "mon", False))
    print(ticket_price("3d", 8, "tue", True))
    print(ticket_price("imax", 65, "tue", False))
    print(ticket_price("4dx", 30, "mon", False))

# WHAT'S NEXT (not refactoring any more, but now easy to do):
#   - Raise an exception instead of returning -1 (see error-handling/)
#   - Add "4dx" by adding one line to BASE_PRICES
