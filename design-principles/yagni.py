"""
YAGNI - YOU AREN'T GONNA NEED IT
"Don't build features until you actually need them."

Analogy: buying a car.
Don't buy a 10-seater van because you *might* have a big family one day.
You pay for fuel, parking and maintenance on seats nobody uses.

PROBLEM
The requirement is "send a welcome email". The code is built to support
SMS, WhatsApp, push, retries, priorities and templates in 12 languages, all
"for the future". None of it is used, but all of it must be maintained.
"""

# ---------------------------------------------------------------------------
# BEFORE: building for imaginary future requirements
# ---------------------------------------------------------------------------
class NotificationSender:
    def __init__(self, channel="email", retries=3, priority="normal",
                 language="en", template_engine="jinja", fallback_channel=None):
        self.channel = channel
        self.retries = retries
        self.priority = priority
        self.language = language
        self.template_engine = template_engine
        self.fallback_channel = fallback_channel

    def send(self, to: str, message: str) -> str:
        if self.channel == "email":
            return f"Email to {to}: {message}"
        elif self.channel == "sms":
            raise NotImplementedError  # "we'll add it later"
        elif self.channel == "whatsapp":
            raise NotImplementedError
        raise ValueError("unknown channel")


# ---------------------------------------------------------------------------
# AFTER: build exactly what was asked
# ---------------------------------------------------------------------------
def send_welcome_email(to: str, name: str) -> str:
    return f"Email to {to}: Welcome, {name}!"


if __name__ == "__main__":
    print("[before]", NotificationSender().send("asha@example.com", "Welcome, Asha!"))
    print("[after] ", send_welcome_email("asha@example.com", "Asha"))

# When SMS is REALLY needed, refactor then. You'll know the real requirements
# by that time (see design-patterns/strategy.py for how it might grow).
#
# YAGNI is NOT an excuse to skip:
#   - tests, input validation, error handling, security
#   - keeping code clean enough to change later
#
# TRADE-OFFS
# + Less code, fewer bugs, faster delivery.
# - Occasionally you'll refactor when the need arrives. That's usually
#   cheaper than maintaining guesses for months.
