# Design Patterns

A design pattern is a **named, reusable solution to a common problem**.
It's not a library you install. It's a known shape for your code that other developers recognise.

> **Everyday analogy:** Recipes. "Biryani" names a known way of cooking.
> Every chef cooks it a bit differently, but everyone knows what you mean.

| Pattern | Problem it solves | Everyday example | File |
| --- | --- | --- | --- |
| **Strategy** | Choose between different ways of doing the same task. | Going to the airport by cab, metro or bus. Same goal, different method. | [strategy.py](strategy.py) |
| **Factory** | Hide the details of *which* object to create. | At a coffee shop you say "latte" and the barista knows how to make it. | [factory.py](factory.py) |
| **Adapter** | Make an incompatible thing fit what you expect. | A travel plug adapter for foreign sockets. | [adapter.py](adapter.py) |
| **Observer** | Tell many listeners when something happens. | YouTube subscribers get notified when a new video is uploaded. | [observer.py](observer.py) |
| **Decorator** | Add extra behaviour without changing the original. | Adding toppings to a pizza; the base pizza stays the same. | [decorator.py](decorator.py) |

## A warning

Patterns are tools, not goals. Use one when you **feel the problem it solves**.
Adding patterns "to be professional" makes code harder to read (see [YAGNI](../design-principles/yagni.py)).

## Run the examples

```bash
python design-patterns/strategy.py
python design-patterns/factory.py
python design-patterns/adapter.py
python design-patterns/observer.py
python design-patterns/decorator.py
```
