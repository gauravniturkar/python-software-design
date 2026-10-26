# Design Principles

These short rules of thumb help with everyday decisions, beyond SOLID.

| Principle | Simple meaning | Everyday example | File |
| --- | --- | --- | --- |
| **DRY**: Don't Repeat Yourself | Every piece of knowledge should live in one place. | Save a contact's number once in your phone. Don't write it on ten sticky notes. | [dry.py](dry.py) |
| **KISS**: Keep It Simple, Stupid | Pick the simplest solution that works. | To boil water, use a kettle. You don't need a smart IoT kitchen. | [kiss.py](kiss.py) |
| **YAGNI**: You Aren't Gonna Need It | Don't build features "just in case". | Don't buy a 10-seater van because you *might* have more kids someday. | [yagni.py](yagni.py) |
| **Separation of Concerns** | Keep different kinds of work in different places. | In a house, the kitchen is for cooking and the bedroom is for sleeping. | [separation_of_concerns.py](separation_of_concerns.py) |

## How they balance each other

- Too much **DRY** can create confusing shared code. Two things that only *look* alike today may need to change differently tomorrow.
- **KISS** and **YAGNI** stop you from over-applying SOLID and design patterns.
- **Separation of concerns** is the idea behind layered architecture (see [../architecture/](../architecture/)).

## Run the examples

```bash
python design-principles/dry.py
python design-principles/kiss.py
python design-principles/yagni.py
python design-principles/separation_of_concerns.py
```
