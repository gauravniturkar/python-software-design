"""
THE COMPOSITION ROOT
"Wire all your objects together in ONE place, at startup."

Analogy: the restaurant manager.
Before opening, the manager decides which supplier delivers vegetables,
which bank handles payments and which staff work today. Chefs and waiters
don't make those decisions; they just do their jobs.

If every class receives its dependencies, someone must create them. That
"someone" should be one function near your app's entry point (main.py,
the FastAPI app factory, and so on).
"""
import os
from typing import Protocol


class EmailClient(Protocol):
    def send(self, to: str, body: str) -> None: ...


class SmtpEmailClient:
    def __init__(self, host: str):
        self.host = host

    def send(self, to: str, body: str) -> None:
        print(f"[SMTP {self.host}] -> {to}: {body}")


class ConsoleEmailClient:
    """Used in local development: prints instead of sending."""

    def send(self, to: str, body: str) -> None:
        print(f"[DEV EMAIL] -> {to}: {body}")


class UserRepository:
    def __init__(self):
        self.users: dict[str, str] = {}

    def add(self, email: str, name: str) -> None:
        self.users[email] = name


class SignupService:
    def __init__(self, users: UserRepository, email: EmailClient):
        self.users = users
        self.email = email

    def sign_up(self, email: str, name: str) -> None:
        self.users.add(email, name)
        self.email.send(email, f"Welcome, {name}!")


# ---------------------------------------------------------------------------
# COMPOSITION ROOT: the only place that knows about concrete classes
# ---------------------------------------------------------------------------
def build_app(environment: str) -> SignupService:
    if environment == "production":
        email = SmtpEmailClient(host="smtp.mycompany.com")
    else:
        email = ConsoleEmailClient()

    users = UserRepository()
    return SignupService(users=users, email=email)


if __name__ == "__main__":
    env = os.getenv("APP_ENV", "development")
    app = build_app(env)
    app.sign_up("asha@example.com", "Asha")

    # Try: APP_ENV=production python dependency-injection/03_composition_root.py

# TRADE-OFFS
# + All "which implementation?" decisions live in one easy-to-find place.
# + The rest of the code stays clean and testable.
# - In very large apps this wiring grows. That's when DI libraries
#   (e.g. `dependency-injector`) or framework features (FastAPI `Depends`)
#   can help. Start without them.
