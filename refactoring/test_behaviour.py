"""
"Characterisation tests": they pin down what the OLD code does, then check
that the NEW code does exactly the same thing.

Run with:   pytest refactoring/

Tip: when refactoring real legacy code, write these tests FIRST, against the
old code, before changing a single line.
"""
import itertools

import pytest

from after import ticket_price
from before import calc

TICKET_TYPES = ["2d", "3d", "imax", "4dx"]
AGES = [5, 11, 12, 30, 59, 60, 80]
DAYS = ["mon", "tue", "sun"]
RECLINER = [True, False]


@pytest.mark.parametrize(
    "ticket_type, age, day, recliner",
    list(itertools.product(TICKET_TYPES, AGES, DAYS, RECLINER)),
)
def test_new_code_matches_old_code(ticket_type, age, day, recliner):
    # Every combination: 4 x 7 x 3 x 2 = 168 checks.
    assert ticket_price(ticket_type, age, day, recliner) == calc(ticket_type, age, day, recliner)
