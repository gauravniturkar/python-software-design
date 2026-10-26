"""
SEPARATION OF CONCERNS
"Keep different kinds of work in different places."

Analogy: rooms in a house.
You cook in the kitchen, sleep in the bedroom and wash in the bathroom.
Renovating the kitchen doesn't mean tearing down the bedroom.

PROBLEM
One function reads input, validates it, applies business rules, and prints
output. Want a web form instead of console input? You rewrite everything.
"""

# ---------------------------------------------------------------------------
# BEFORE: input, rules and output tangled together
# ---------------------------------------------------------------------------
def register_user_before(raw_age: str, name: str) -> None:
    if not raw_age.isdigit():                      # validation
        print("Error: age must be a number")       # output
        return
    age = int(raw_age)
    category = "adult" if age >= 18 else "minor"   # business rule
    print(f"Registered {name} as {category}")      # output


# ---------------------------------------------------------------------------
# AFTER: each concern in its own function
# ---------------------------------------------------------------------------
def parse_age(raw_age: str) -> int:
    """Concern: turning raw input into clean data."""
    if not raw_age.isdigit():
        raise ValueError("age must be a number")
    return int(raw_age)


def age_category(age: int) -> str:
    """Concern: the business rule. No input or printing here."""
    return "adult" if age >= 18 else "minor"


def show_registration(name: str, category: str) -> str:
    """Concern: presentation. Swap this for HTML or JSON later."""
    return f"Registered {name} as {category}"


def register_user(raw_age: str, name: str) -> str:
    """Glue code that connects the pieces."""
    age = parse_age(raw_age)
    return show_registration(name, age_category(age))


if __name__ == "__main__":
    register_user_before("25", "Asha")
    print(register_user("25", "Asha"))
    print(register_user("12", "Ravi"))
    try:
        register_user("abc", "Bad input")
    except ValueError as error:
        print("Error:", error)

    # The business rule is now trivial to test:
    assert age_category(18) == "adult"
    assert age_category(17) == "minor"

# TRADE-OFFS
# + Change the UI without touching rules, and change rules without touching the UI.
# + Each piece is easy to test on its own.
# - More functions and files. For a 20-line script it can be overkill.
