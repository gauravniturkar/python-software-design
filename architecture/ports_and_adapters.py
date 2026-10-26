"""
PORTS AND ADAPTERS (also called Hexagonal Architecture)
"Business logic in the centre. The outside world plugs in through sockets."

Analogy: a laptop.
The laptop (core) has ports: USB, HDMI, a charging port. It doesn't care
whether you plug in a Dell monitor or a Samsung TV. Any device with the right
adapter works. You can change devices without opening the laptop.

  PORT    = an interface the core DEFINES ("I need something that can save orders")
  ADAPTER = a concrete implementation that FITS a port (Postgres, in-memory, etc.)

The core never imports a database or web library. Dependencies point INWARD.
"""
from dataclasses import dataclass, field
from typing import Protocol


# ===========================================================================
# CORE (the centre of the hexagon): pure business logic, no frameworks
# ===========================================================================
@dataclass
class Ticket:
    id: str
    movie: str
    seat: str


# PORTS: the core says what it NEEDS, not how it's done.
class TicketStore(Protocol):  # "driven" port (core -> outside)
    def is_seat_taken(self, movie: str, seat: str) -> bool: ...
    def save(self, ticket: Ticket) -> None: ...


class Notifier(Protocol):  # another driven port
    def notify(self, message: str) -> None: ...


class SeatTaken(Exception):
    pass


class BookingService:
    """The use case. Its only dependencies are ports."""

    def __init__(self, store: TicketStore, notifier: Notifier):
        self.store = store
        self.notifier = notifier
        self._counter = 0

    def book(self, movie: str, seat: str) -> Ticket:
        if self.store.is_seat_taken(movie, seat):
            raise SeatTaken(f"Seat {seat} for {movie} is already booked")
        self._counter += 1
        ticket = Ticket(id=f"T{self._counter}", movie=movie, seat=seat)
        self.store.save(ticket)
        self.notifier.notify(f"Booked {seat} for {movie} (ticket {ticket.id})")
        return ticket


# ===========================================================================
# ADAPTERS (outside the hexagon): plug real-world tech into the ports
# ===========================================================================
@dataclass
class InMemoryTicketStore:
    tickets: list[Ticket] = field(default_factory=list)

    def is_seat_taken(self, movie: str, seat: str) -> bool:
        return any(t.movie == movie and t.seat == seat for t in self.tickets)

    def save(self, ticket: Ticket) -> None:
        self.tickets.append(ticket)


class SqlTicketStore:
    """Sketch of a real adapter. In production this would use a DB driver."""

    def is_seat_taken(self, movie: str, seat: str) -> bool:
        print(f"[SQL] SELECT 1 FROM tickets WHERE movie='{movie}' AND seat='{seat}'")
        return False

    def save(self, ticket: Ticket) -> None:
        print(f"[SQL] INSERT INTO tickets VALUES {ticket}")


class ConsoleNotifier:
    def notify(self, message: str) -> None:
        print(f"[notify] {message}")


# "Driving" adapter: something that CALLS the core (a CLI, a web route...)
def cli_adapter(service: BookingService, command: str) -> None:
    _, movie, seat = command.split()  # e.g. "book Inception A1"
    try:
        ticket = service.book(movie, seat)
        print(f"CLI: success -> {ticket}")
    except SeatTaken as error:
        print(f"CLI: sorry -> {error}")


if __name__ == "__main__":
    print("=== With in-memory adapter (great for tests and demos) ===")
    service = BookingService(InMemoryTicketStore(), ConsoleNotifier())
    cli_adapter(service, "book Inception A1")
    cli_adapter(service, "book Inception A1")  # same seat -> rejected

    print("\n=== Same core, SQL adapter plugged in ===")
    service = BookingService(SqlTicketStore(), ConsoleNotifier())
    cli_adapter(service, "book Inception B2")

# TRADE-OFFS
# + The core is 100% testable without databases or web servers.
# + Replace Postgres with DynamoDB, or REST with gRPC, without touching rules.
# - More interfaces and files than a simple layered app.
# - Worth it for long-lived apps with real business rules. Overkill for a
#   simple CRUD app that mostly moves data in and out of a table.
