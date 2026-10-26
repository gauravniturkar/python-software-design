# Python Software Design

Practical examples of writing Python code that is easier to understand, test, and change.

This repository explores software design through small examples and realistic backend scenarios. The focus is on understanding the problem a principle or pattern solves, the trade-offs it introduces, and when a simpler approach is enough.

## Project status

This repository is being built incrementally, starting with SOLID principles. The roadmap below describes the intended scope; it does not imply that every topic has been implemented.

## SOLID principles

| Principle | Focus |
| --- | --- |
| Single Responsibility | Group code around one responsibility and reason to change. |
| Open/Closed | Allow new behavior through extension without repeatedly changing stable code. |
| Liskov Substitution | Ensure implementations can replace their abstractions without breaking expected behavior. |
| Interface Segregation | Keep interfaces focused so consumers depend only on what they need. |
| Dependency Inversion | Make high-level policy and low-level details depend on abstractions. |

## Roadmap

- **Object-oriented design:** encapsulation, polymorphism, composition, and inheritance.
- **Design principles:** SOLID, DRY, KISS, YAGNI, and separation of concerns.
- **Interfaces and contracts:** abstract base classes, protocols, and duck typing.
- **Design patterns:** Strategy, Factory, Adapter, Observer, and Decorator.
- **Dependency injection:** providing dependencies explicitly and replacing them in tests.
- **Application architecture:** layered architecture and ports and adapters.
- **Data access:** Repository and Unit of Work patterns.
- **Error handling:** meaningful exceptions and clear error boundaries.
- **Testable design:** isolating side effects and using lightweight fakes.
- **Refactoring:** improving existing code while preserving its behavior.

## Example format

Each example is intended to include:

1. **Problem:** a concrete requirement or change that makes the original design difficult to work with.
2. **Before:** an implementation that demonstrates the difficulty.
3. **After:** a refactored implementation with a clear explanation.
4. **Trade-offs:** what improves, what becomes more complex, and when the approach is unnecessary.
5. **Usage:** instructions for running the example, with focused tests where useful.

## Planned case studies

- **Notification service:** support multiple delivery channels through a common contract.
- **Data import pipeline:** separate reading, validation, transformation, and persistence.
- **File storage service:** switch storage implementations without changing business logic.
- **Order processing:** separate business rules, persistence, and notifications.

## How to use this repository

Start with a topic's README, compare the before and after implementations, and follow its execution instructions as examples are added.

Basic Python knowledge is helpful. Examples will introduce additional concepts where they are needed.

## Design approach

Use principles and patterns to solve concrete problems. Prefer clear Python code, keep abstractions purposeful, and explain the trade-offs behind each design decision.

