"""
ADAPTER PATTERN
"Wrap something incompatible so it matches the interface you expect."

Analogy: a travel plug adapter.
Your Indian charger won't fit a UK socket. You don't rebuild the charger or
the wall. You put a small adapter in between.

PROBLEM
Our app sends SMS through `send(phone, text)`. We switch to a new vendor
whose SDK has a completely different method and argument names. We don't
want to change the 50 places in our app that call `send`.
"""
from typing import Protocol


# What OUR app expects
class SmsSender(Protocol):
    def send(self, phone: str, text: str) -> str: ...


# Old vendor: already matches our interface
class OldSmsVendor:
    def send(self, phone: str, text: str) -> str:
        return f"[OldVendor] to {phone}: {text}"


# New vendor's third-party SDK: we CAN'T change this code
class FancySmsSDK:
    def dispatch_message(self, payload: dict) -> dict:
        return {"status": "queued", "recipient": payload["msisdn"], "body": payload["content"]}


# ---------------------------------------------------------------------------
# THE ADAPTER: makes FancySmsSDK look like an SmsSender
# ---------------------------------------------------------------------------
class FancySmsAdapter:
    def __init__(self, sdk: FancySmsSDK):
        self.sdk = sdk

    def send(self, phone: str, text: str) -> str:
        # Translate our simple call into the vendor's format...
        response = self.sdk.dispatch_message({"msisdn": phone, "content": text})
        # ...and translate the vendor's response back into what we expect.
        return f"[FancySMS] {response['status']} for {response['recipient']}: {response['body']}"


def notify_customer(sender: SmsSender, phone: str) -> None:
    # This app code never changes, whichever vendor we use.
    print(sender.send(phone, "Your order has shipped!"))


if __name__ == "__main__":
    notify_customer(OldSmsVendor(), "+91-98xxxxxx01")
    notify_customer(FancySmsAdapter(FancySmsSDK()), "+91-98xxxxxx01")

# TRADE-OFFS
# + Switching vendors touches one small class, not the whole app.
# + Vendor-specific details stay out of your business logic.
# - One more layer. If you call the SDK in exactly one place, an adapter
#   may not be worth it.
