"""
S - SINGLE RESPONSIBILITY PRINCIPLE (SRP)
"A class should have one job, and only one reason to change."

Analogy: a restaurant.
The chef cooks, the cashier bills, the waiter serves. If the billing rules
change (new tax), only the cashier needs retraining, not the chef.

PROBLEM
An invoice class calculates totals, formats the invoice AND saves it to a file.
Changing the PDF layout, the tax rule or the storage location all mean
editing the same class, and each edit risks breaking the other two jobs.
"""
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# BEFORE: one class with three jobs
# ---------------------------------------------------------------------------
class InvoiceDoesEverything:
    def __init__(self, customer: str, items: list[tuple[str, float]]):
        self.customer = customer
        self.items = items

    def total(self) -> float:  # job 1: business math
        return sum(price for _, price in self.items) * 1.18  # 18% tax

    def render(self) -> str:  # job 2: presentation
        lines = [f"Invoice for {self.customer}"]
        lines += [f"  {name}: {price}" for name, price in self.items]
        lines.append(f"  Total (incl. tax): {self.total():.2f}")
        return "\n".join(lines)

    def save(self, path: str) -> None:  # job 3: storage
        with open(path, "w") as f:
            f.write(self.render())


# ---------------------------------------------------------------------------
# AFTER: each class has one job
# ---------------------------------------------------------------------------
@dataclass
class Invoice:
    """Job: hold invoice data and do invoice math."""
    customer: str
    items: list[tuple[str, float]]
    tax_rate: float = 0.18

    def total(self) -> float:
        subtotal = sum(price for _, price in self.items)
        return subtotal * (1 + self.tax_rate)


class InvoiceFormatter:
    """Job: turn an invoice into text. Change this when the layout changes."""

    def render(self, invoice: Invoice) -> str:
        lines = [f"Invoice for {invoice.customer}"]
        lines += [f"  {name}: {price}" for name, price in invoice.items]
        lines.append(f"  Total (incl. tax): {invoice.total():.2f}")
        return "\n".join(lines)


class InvoiceSaver:
    """Job: store the text somewhere. Change this when storage changes."""

    def save(self, text: str, path: str) -> None:
        with open(path, "w") as f:
            f.write(text)


if __name__ == "__main__":
    invoice = Invoice("Asha", [("Keyboard", 1500), ("Mouse", 500)])
    text = InvoiceFormatter().render(invoice)
    print(text)
    # InvoiceSaver().save(text, "invoice.txt")  # uncomment to write a file

# TRADE-OFFS
# + A change to tax, layout or storage touches exactly one class.
# + Invoice math can be tested without creating any files.
# - More classes to find and name.
# - Don't split code that always changes together. "One responsibility"
#   means "one reason to change", not "one method per class".
