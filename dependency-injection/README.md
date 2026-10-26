# Dependency Injection (DI)

**Dependency injection** means: *don't create the things you need yourself. Ask for them.*

A "dependency" is anything your code needs to do its job: a database, an email client, a clock, a config.

> **Everyday analogy:** A chef in a restaurant doesn't grow vegetables or raise chickens.
> Ingredients are **delivered** to the kitchen. Need organic tomatoes this week? Change
> the supplier. The chef's recipe stays the same.

## Why it matters

| Without DI | With DI |
| --- | --- |
| Class creates its own database connection. | Database connection is passed in. |
| Tests hit the real database or email server. | Tests pass in a fake. |
| Switching providers means editing the class. | Switching providers means passing a different object. |

## Files

| File | What it shows |
| --- | --- |
| [01_without_di.py](01_without_di.py) | A class that creates its own dependencies, and why that hurts. |
| [02_with_di.py](02_with_di.py) | The same class with constructor injection, plus a test using fakes. |
| [03_composition_root.py](03_composition_root.py) | Where to wire everything together: one place at app startup. |

## Key idea: you don't need a framework

In Python, DI is usually just **passing arguments to `__init__`**. Frameworks such as
FastAPI's `Depends` exist, but the core idea is plain function arguments.

## Run the examples

```bash
python dependency-injection/01_without_di.py
python dependency-injection/02_with_di.py
python dependency-injection/03_composition_root.py
```
