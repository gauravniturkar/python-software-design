"""
DUCK TYPING
"If it walks like a duck and quacks like a duck, treat it as a duck."

Analogy: hiring a driver.
You don't ask which car brand they learned on. You just need them to
`drive()`. Anyone who can drive gets the job.

Python doesn't check types before running. It only checks that the object
has the method at the moment you call it.
"""


class Duck:
    def speak(self) -> str:
        return "Quack!"


class Robot:
    # Not related to Duck at all, but it also has `speak`.
    def speak(self) -> str:
        return "Beep boop."


class Rock:
    pass  # no `speak` method


def make_it_talk(thing) -> None:
    # No isinstance checks: we simply trust that `thing` can speak.
    print(thing.speak())


if __name__ == "__main__":
    make_it_talk(Duck())
    make_it_talk(Robot())

    try:
        make_it_talk(Rock())
    except AttributeError as error:
        # The downside: mistakes only appear when the code actually runs.
        print(f"Runtime error: {error}")

# REAL PYTHON EXAMPLES OF DUCK TYPING
#   - `for x in something` works with lists, files, generators... anything iterable.
#   - `len(x)` works with anything that has a `__len__` method.
#
# TRADE-OFFS
# + Very flexible, with zero ceremony.
# - Errors show up at runtime, sometimes far from the real mistake.
# - The "contract" is invisible; readers must guess which methods are needed.
#   Protocols (03_protocols.py) fix this while keeping the flexibility.
