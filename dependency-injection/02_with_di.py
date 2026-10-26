"""
WITH DEPENDENCY INJECTION

Analogy: a chef whose ingredients are delivered.
The recipe stays the same. You choose the supplier from outside: a real
farm in production, or plastic props for a cooking-show rehearsal (tests).

THE FIX
Pass dependencies in through `__init__` (constructor injection).
"""
from datetime import datetime
from typing import Callable, Protocol


class EmailClient(Protocol):
    def send(self, to: str, subject: str) -> None: ...


class SmtpEmailClient:
    def send(self, to: str, subject: str) -> None:
        print(f"[REAL SMTP] Sending '{subject}' to {to}")


class SignupService:
    def __init__(self, email_client: EmailClient, clock: Callable[[], datetime] = datetime.now):
        # Dependencies come from OUTSIDE. The default keeps normal usage easy.
        self.email_client = email_client
        self.clock = clock

    def sign_up(self, email: str) -> str:
        greeting = "Good morning" if self.clock().hour < 12 else "Hello"
        self.email_client.send(email, f"{greeting}, welcome aboard!")
        return f"Signed up {email}"


# ---------------------------------------------------------------------------
# TESTING: plug in fakes instead of real things
# ---------------------------------------------------------------------------
class FakeEmailClient:
    """Records emails instead of sending them."""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, subject: str) -> None:
        self.sent.append((to, subject))


def test_morning_greeting():
    fake_email = FakeEmailClient()
    nine_am = lambda: datetime(2026, 1, 1, 9, 0)  # we control time!
    service = SignupService(fake_email, clock=nine_am)

    service.sign_up("asha@example.com")

    assert fake_email.sent == [("asha@example.com", "Good morning, welcome aboard!")]


def test_afternoon_greeting():
    fake_email = FakeEmailClient()
    three_pm = lambda: datetime(2026, 1, 1, 15, 0)
    service = SignupService(fake_email, clock=three_pm)

    service.sign_up("ravi@example.com")

    assert fake_email.sent[0][1] == "Hello, welcome aboard!"


if __name__ == "__main__":
    # Production: real email client, real clock
    print(SignupService(SmtpEmailClient()).sign_up("asha@example.com"))

    # Tests: fake email, fake clock. No network, fully predictable.
    test_morning_greeting()
    test_afternoon_greeting()
    print("All tests passed")

# TRADE-OFFS
# + Easy to test, easy to swap implementations.
# + Dependencies are visible in the constructor; nothing is hidden.
# - Someone has to create and pass the dependencies (see 03_composition_root.py).
# - Constructors with 8+ dependencies are a sign the class does too much (SRP).
