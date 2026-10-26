"""
I - INTERFACE SEGREGATION PRINCIPLE (ISP)
"Don't force a class to depend on methods it doesn't use."

Analogy: printers.
A cheap home printer only prints. An office machine prints, scans and faxes.
If the rulebook says "every printer must have print, scan and fax buttons",
the cheap printer ends up with fake buttons that do nothing.

PROBLEM
One big interface forces simple classes to implement features they don't have.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BEFORE: one fat interface for all machines
# ---------------------------------------------------------------------------
class OfficeMachine(ABC):
    @abstractmethod
    def print_doc(self, doc: str) -> str: ...

    @abstractmethod
    def scan(self, doc: str) -> str: ...

    @abstractmethod
    def fax(self, doc: str) -> str: ...


class BasicPrinterBefore(OfficeMachine):
    def print_doc(self, doc: str) -> str:
        return f"Printing {doc}"

    # Forced to write methods it can't support. Callers get surprised.
    def scan(self, doc: str) -> str:
        raise NotImplementedError("I can't scan")

    def fax(self, doc: str) -> str:
        raise NotImplementedError("I can't fax")


# ---------------------------------------------------------------------------
# AFTER: small, focused interfaces; pick only what you need
# ---------------------------------------------------------------------------
class Printer(ABC):
    @abstractmethod
    def print_doc(self, doc: str) -> str: ...


class Scanner(ABC):
    @abstractmethod
    def scan(self, doc: str) -> str: ...


class Fax(ABC):
    @abstractmethod
    def fax(self, doc: str) -> str: ...


class BasicPrinter(Printer):
    def print_doc(self, doc: str) -> str:
        return f"Printing {doc}"


class AllInOneMachine(Printer, Scanner, Fax):
    def print_doc(self, doc: str) -> str:
        return f"Printing {doc}"

    def scan(self, doc: str) -> str:
        return f"Scanning {doc}"

    def fax(self, doc: str) -> str:
        return f"Faxing {doc}"


def print_report(printer: Printer) -> None:
    # This function only needs printing, so it only asks for a Printer.
    print(printer.print_doc("monthly-report.pdf"))


if __name__ == "__main__":
    try:
        BasicPrinterBefore().scan("photo.jpg")
    except NotImplementedError as error:
        print(f"[before] Surprise: {error}")

    print("[after]")
    print_report(BasicPrinter())
    print_report(AllInOneMachine())

# TRADE-OFFS
# + Classes only promise what they can really do.
# + Functions ask for exactly the ability they need, which makes testing easy.
# - More small interfaces to name and keep track of.
# - Don't split an interface whose methods are always used together.
