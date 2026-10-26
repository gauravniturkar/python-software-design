# Python Software Design

Learn how to write Python code that is **easy to understand, test and change**, explained in
plain language with everyday analogies and small runnable examples.

Every concept answers one question: **"When requirements change, how painful is it to update the code?"**

## Repository structure

```
python-software-design/
├── README.md
├── oop/                     # Objects, encapsulation, inheritance, polymorphism, composition
├── solid/                   # The five SOLID principles
├── design-principles/       # DRY, KISS, YAGNI, separation of concerns
├── interfaces/              # Duck typing, abstract base classes, protocols
├── design-patterns/         # Strategy, Factory, Adapter, Observer, Decorator
├── dependency-injection/    # Passing dependencies in instead of creating them
├── architecture/            # Layered architecture, ports and adapters
├── data-access/             # Repository and Unit of Work
├── error-handling/          # Meaningful exceptions and error boundaries
├── testable-design/         # Isolating side effects, fakes, pytest examples
├── refactoring/             # Improving code without changing behaviour
└── case-studies/            # Realistic scenarios combining everything
```

## Learning path

Follow the topics in this order. Each one builds on the ones before it.

| # | Topic | In one sentence | Everyday analogy |
| --- | --- | --- | --- |
| 1 | [OOP](oop/) | Organise code around objects that hold data and behaviour. | A TV remote: buttons outside, electronics hidden inside. |
| 2 | [Interfaces](interfaces/) | A contract: "anything with these methods can be used here." | A USB port accepts any USB device. |
| 3 | [Design principles](design-principles/) | Simple rules of thumb: don't repeat yourself, keep it simple, don't build for imaginary needs. | Save a phone number once, not on ten sticky notes. |
| 4 | [SOLID](solid/) | Five guidelines that keep classes focused and replaceable. | Chef cooks, cashier bills, and nobody does both jobs. |
| 5 | [Dependency injection](dependency-injection/) | Ask for what you need instead of building it yourself. | Ingredients are delivered to the chef. |
| 6 | [Design patterns](design-patterns/) | Named, proven solutions to common problems. | Recipes everyone recognises. |
| 7 | [Error handling](error-handling/) | Raise specific errors and handle them at the right layer. | Dashboard warning lights, each with one clear meaning. |
| 8 | [Testable design](testable-design/) | Keep logic separate from side effects so it's easy to test. | A flight simulator instead of a real crash. |
| 9 | [Data access](data-access/) | Hide the database behind a clean, collection-like interface. | Ask the librarian instead of searching the shelves. |
| 10 | [Architecture](architecture/) | Arrange the big pieces so business rules don't depend on tools. | A restaurant: waiters, chefs and the storeroom stay separate. |
| 11 | [Refactoring](refactoring/) | Improve structure without changing behaviour, step by safe step. | Reorganising a kitchen: same meals, less mess. |
| 12 | [Case studies](case-studies/) | Real backend scenarios that use everything together. | Notifications, data imports, file storage, checkout. |

## Example format

Each folder has a `README.md` with a plain-English explanation, plus `.py` files that follow the same shape:

1. **Analogy:** an everyday picture of the idea.
2. **Problem:** a concrete requirement that makes naive code painful.
3. **Before:** code that shows the pain.
4. **After:** the improved version, explained with comments.
5. **Trade-offs:** what you gain, what it costs, and **when it's overkill**.

## How to run

You only need Python 3.10+. Every example uses the standard library only.

```bash
# Run any example
python solid/02_open_closed.py

# Run the tests (only these need pytest)
pip install pytest
pytest testable-design/ refactoring/
```

## Design approach

Principles and patterns are **tools, not goals**. Use one when it solves a problem you actually have.
Prefer clear Python over clever abstractions, and always ask: *"Is the simpler version good enough?"*
