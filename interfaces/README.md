# Interfaces and Contracts

An **interface** is a promise: *"anything that has these methods can be used here."*
It's a contract between the code that **uses** something and the code that **provides** it.

> **Everyday analogy:** A USB port. Your laptop doesn't care whether you plug in a
> mouse, a keyboard or a pen drive. Anything that follows the USB "contract" works.

Python gives you three ways to express this:

| Approach | How it works | Everyday example | File |
| --- | --- | --- | --- |
| **Duck typing** | "If it walks like a duck and quacks like a duck, it's a duck." No formal declaration. | A driver doesn't check the car's brand, only that it has a steering wheel and pedals. | [01_duck_typing.py](01_duck_typing.py) |
| **Abstract Base Classes (ABC)** | A parent class says "children MUST implement these methods". Python enforces it when you create an object. | A job contract: you must sign it and follow it to be hired. | [02_abstract_base_classes.py](02_abstract_base_classes.py) |
| **Protocols** | Describe the required shape. Type checkers (mypy, pyright) verify it, with no inheritance needed. | A driving licence test checks *what you can do*, not which school you went to. | [03_protocols.py](03_protocols.py) |

## Which one should I use?

- **Duck typing:** small scripts and quick code.
- **ABC:** you own all the implementations and want a loud error if a method is missing.
- **Protocol:** you want type-checked contracts, or you need to accept classes you don't own (third-party libraries).

## Run the examples

```bash
python interfaces/01_duck_typing.py
python interfaces/02_abstract_base_classes.py
python interfaces/03_protocols.py
```
