"""
WITHOUT DEPENDENCY INJECTION

Analogy: a chef who insists on growing their own vegetables.
Want to try a different supplier? Impossible: the farm is built into the
kitchen. Want to test a recipe without real vegetables? Also impossible.

PROBLEM
`SignupService` creates its own email client and reads the real clock.
  - Tests would send REAL emails.
  - Tests can't control "now", so time-based rules are hard to test.
  - Switching email provider means editing this class.
"""
from datetime import datetime


class SmtpEmailClient:
    def send(self, to: str, subject: str) -> None:
        # Imagine this connects to a real mail server.
        print(f"[REAL SMTP] Sending '{subject}' to {to}")


class SignupService:
    def __init__(self):
        self.email_client = SmtpEmailClient()  # hidden, hard-wired dependency

    def sign_up(self, email: str) -> str:
        now = datetime.now()  # another hidden dependency: the real clock
        greeting = "Good morning" if now.hour < 12 else "Hello"
        self.email_client.send(email, f"{greeting}, welcome aboard!")
        return f"Signed up {email}"


if __name__ == "__main__":
    service = SignupService()
    print(service.sign_up("asha@example.com"))
    # How would you test the "Good morning" branch at 3 pm? You can't easily.
    # How do you test without sending a real email? You can't easily.
    # See 02_with_di.py for the fix.
