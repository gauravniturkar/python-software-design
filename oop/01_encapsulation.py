"""
ENCAPSULATION: hide the inner details and offer a safe set of buttons.

Analogy: an ATM.
You can check your balance and withdraw cash, but you cannot reach in and
change the number stored in the bank's computer. The ATM makes sure every
withdrawal follows the rules (enough money, positive amount, and so on).
"""


# ---------------------------------------------------------------------------
# BEFORE: anyone can change the balance directly
# ---------------------------------------------------------------------------
class OpenBankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance  # fully public: nothing protects it


def before_demo():
    account = OpenBankAccount("Asha", 100)
    # Oops: nothing stops someone from setting a nonsense value.
    account.balance = -5000
    print(f"[before] {account.owner}'s balance is {account.balance}  <-- invalid!")


# ---------------------------------------------------------------------------
# AFTER: the balance can only change through methods that follow the rules
# ---------------------------------------------------------------------------
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        # The leading underscore is a Python convention that means
        # "internal detail, please don't touch this from outside".
        self._balance = balance

    @property
    def balance(self) -> float:
        """Read-only view of the balance, like the ATM screen."""
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Not enough money")
        self._balance -= amount


def after_demo():
    account = BankAccount("Asha", 100)
    account.deposit(50)
    account.withdraw(30)
    print(f"[after]  {account.owner}'s balance is {account.balance}")

    try:
        account.withdraw(1000)
    except ValueError as error:
        print(f"[after]  Blocked: {error}")

    # `balance` is a property without a setter, so this line would fail:
    # account.balance = -5000   -> AttributeError


if __name__ == "__main__":
    before_demo()
    after_demo()

# TRADE-OFFS
# + Rules live in one place, so invalid states are much harder to create.
# + You can change the inside (e.g. store cents instead of rupees) without
#   breaking code that uses the class.
# - A bit more code than a plain attribute.
# - For a simple data holder with no rules, a plain @dataclass is enough.
