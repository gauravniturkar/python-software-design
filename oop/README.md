# Object-Oriented Programming (OOP)

OOP is a way of organising code around **things** (objects) instead of around **steps**.
Each object keeps its own data and knows how to do things with that data.

> **Everyday analogy:** A TV remote. You press "Volume +" and the volume goes up.
> You don't need to know what happens inside the remote. The remote *holds* its
> state (battery, current channel) and *offers* buttons (methods) to use it.

## The four big ideas

| Idea | One-line meaning | Everyday example | File |
| --- | --- | --- | --- |
| Encapsulation | Hide the inner details and offer a safe set of buttons. | An ATM lets you withdraw money, but you can't open the cash box yourself. | [01_encapsulation.py](01_encapsulation.py) |
| Inheritance | A new class reuses and extends an existing class. | An electric car is still a car. It just adds charging. | [02_inheritance.py](02_inheritance.py) |
| Polymorphism | Different objects answer the same request in their own way. | "Pay" works with cash, card or UPI. Each pays differently. | [03_polymorphism.py](03_polymorphism.py) |
| Composition | Build objects out of smaller objects ("has a" instead of "is a"). | A car *has an* engine and *has* wheels. | [04_composition.py](04_composition.py) |

## Rule of thumb

- Use **inheritance** only when "X is a kind of Y" is clearly true.
- Otherwise prefer **composition**, which is easier to change later.

## Run the examples

```bash
python oop/01_encapsulation.py
python oop/02_inheritance.py
python oop/03_polymorphism.py
python oop/04_composition.py
```
