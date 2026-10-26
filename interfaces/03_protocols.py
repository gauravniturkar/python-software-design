"""
PROTOCOLS (typing.Protocol)
"Describe the SHAPE you need. Any class with that shape fits, without inheriting."

Analogy: a power socket.
The socket doesn't care who made your charger. If the plug has the right
shape, it fits. The charger never had to "register" with the socket.

This is duck typing (01_duck_typing.py) with a written-down contract that
type checkers like mypy or pyright can verify BEFORE the code runs.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable  # optional: also allows isinstance() checks at runtime
class Chargeable(Protocol):
    def charge(self, minutes: int) -> str: ...


# Note: none of these classes inherit from Chargeable.
class Phone:
    def charge(self, minutes: int) -> str:
        return f"Phone charged for {minutes} min"


class Laptop:
    def charge(self, minutes: int) -> str:
        return f"Laptop charged for {minutes} min"


class Book:
    def read(self) -> str:
        return "Reading..."


def plug_in(device: Chargeable) -> None:
    # The type hint documents the contract. A type checker would flag
    # plug_in(Book()) as an error before you ever run the program.
    print(device.charge(30))


if __name__ == "__main__":
    plug_in(Phone())
    plug_in(Laptop())

    print("Is Phone chargeable?", isinstance(Phone(), Chargeable))
    print("Is Book chargeable? ", isinstance(Book(), Chargeable))

# TRY IT
#   pip install mypy
#   Add `plug_in(Book())` at the bottom, then run: mypy interfaces/03_protocols.py
#   mypy reports the error without running the code.
#
# TRADE-OFFS
# + Works with classes you don't own (e.g. from third-party libraries).
# + No inheritance needed, so code stays loosely connected.
# - Checking only happens with a type checker (or runtime_checkable, which
#   only checks method NAMES, not their arguments).
