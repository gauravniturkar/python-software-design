"""
CASE STUDY: NOTIFICATION SERVICE

Everyday picture: a school informing parents.
Some parents want SMS, some email, some a mobile app push. The school writes
the message once ("School closed tomorrow"), and it reaches every parent the
way they prefer.

Requirements
  - Send the same message through different channels (email, SMS, push).
  - Each user picks their preferred channel.
  - Adding WhatsApp next quarter must NOT require editing the core service.
  - One channel failing must not stop the others.

Concepts used
  Protocol (interfaces/)            -> the Channel contract
  Strategy (design-patterns/)       -> each channel is a strategy
  Factory (design-patterns/)        -> build channels from config names
  Dependency Injection              -> channels passed into the service
  Error boundary (error-handling/)  -> one failure doesn't break the batch
"""
from dataclasses import dataclass
from typing import Protocol


@dataclass
class User:
    name: str
    preferred_channel: str
    contact: str  # email address, phone number or device id


# ---------------------------------------------------------------------------
# Contract: every channel must be able to `send`
# ---------------------------------------------------------------------------
class Channel(Protocol):
    def send(self, contact: str, message: str) -> None: ...


class EmailChannel:
    def send(self, contact: str, message: str) -> None:
        print(f"  [email -> {contact}] {message}")


class SmsChannel:
    MAX_LENGTH = 50  # SMS has a length limit (kept small for the demo)

    def send(self, contact: str, message: str) -> None:
        print(f"  [sms   -> {contact}] {message[: self.MAX_LENGTH]}")


class PushChannel:
    def send(self, contact: str, message: str) -> None:
        if not contact.startswith("device-"):
            raise ConnectionError(f"invalid device token '{contact}'")
        print(f"  [push  -> {contact}] {message}")


# ---------------------------------------------------------------------------
# Factory: config names -> channel objects
# ---------------------------------------------------------------------------
CHANNEL_TYPES = {"email": EmailChannel, "sms": SmsChannel, "push": PushChannel}


def build_channels(enabled: list[str]) -> dict[str, Channel]:
    return {name: CHANNEL_TYPES[name]() for name in enabled}


# ---------------------------------------------------------------------------
# Core service: knows nothing about HOW each channel works
# ---------------------------------------------------------------------------
@dataclass
class DeliveryReport:
    sent: list[str]
    failed: list[tuple[str, str]]


class NotificationService:
    def __init__(self, channels: dict[str, Channel]):
        self.channels = channels

    def broadcast(self, users: list[User], message: str) -> DeliveryReport:
        report = DeliveryReport(sent=[], failed=[])
        for user in users:
            channel = self.channels.get(user.preferred_channel)
            if channel is None:
                report.failed.append((user.name, f"channel '{user.preferred_channel}' not enabled"))
                continue
            try:
                channel.send(user.contact, message)
                report.sent.append(user.name)
            except ConnectionError as error:
                # Boundary: record the failure and keep going for others.
                report.failed.append((user.name, str(error)))
        return report


# ---------------------------------------------------------------------------
# Fake channel for tests
# ---------------------------------------------------------------------------
class RecordingChannel:
    def __init__(self):
        self.messages: list[tuple[str, str]] = []

    def send(self, contact: str, message: str) -> None:
        self.messages.append((contact, message))


if __name__ == "__main__":
    users = [
        User("Asha's parent", "email", "asha.parent@example.com"),
        User("Ravi's parent", "sms", "+91-98xxxxxx01"),
        User("Meera's parent", "push", "device-abc123"),
        User("Kabir's parent", "push", "broken-token"),
        User("Zoya's parent", "whatsapp", "+91-98xxxxxx02"),
    ]

    service = NotificationService(build_channels(["email", "sms", "push"]))
    report = service.broadcast(users, "School will be closed tomorrow due to heavy rain.")

    print("Sent:  ", report.sent)
    print("Failed:", report.failed)

    # Test with a fake: no real emails or SMS
    fake = RecordingChannel()
    NotificationService({"email": fake}).broadcast([User("T", "email", "t@x.com")], "hi")
    assert fake.messages == [("t@x.com", "hi")]
    print("Fake channel test passed")

# EXERCISE
#   Add a WhatsAppChannel. Which lines did you have to change?
#   (Answer: one new class and one entry in CHANNEL_TYPES.
#    NotificationService stays untouched. That's the Open/Closed principle.)
