# SOLID Principles

SOLID is five guidelines that keep code easy to change. Each one answers a simple question:
**"When requirements change, how much code do I have to touch?"**

| Letter | Principle | Simple meaning | Everyday example | File |
| --- | --- | --- | --- | --- |
| S | Single Responsibility | One class, one job, one reason to change. | A chef cooks and a cashier takes money. You don't want the chef doing both. | [01_single_responsibility.py](01_single_responsibility.py) |
| O | Open/Closed | Add new features by adding code, not by editing working code. | A phone gets new features from apps. You don't rebuild the phone. | [02_open_closed.py](02_open_closed.py) |
| L | Liskov Substitution | A replacement must behave the way users expect the original to behave. | A substitute teacher should still teach the class, not cancel it. | [03_liskov_substitution.py](03_liskov_substitution.py) |
| I | Interface Segregation | Don't force anyone to depend on things they don't use. | A basic printer shouldn't be forced to have a "fax" button. | [04_interface_segregation.py](04_interface_segregation.py) |
| D | Dependency Inversion | Important code should depend on an idea, not on a specific tool. | A lamp plugs into a socket, not wired straight into the power plant. | [05_dependency_inversion.py](05_dependency_inversion.py) |

## How to read each file

Every file has the same shape:

1. **Problem:** what change makes the code painful.
2. **Before:** code that breaks the principle.
3. **After:** the same feature written with the principle.
4. **Trade-offs:** what you gain, what it costs, and when it's overkill.

## Run the examples

```bash
python solid/01_single_responsibility.py
python solid/02_open_closed.py
python solid/03_liskov_substitution.py
python solid/04_interface_segregation.py
python solid/05_dependency_inversion.py
```

> SOLID principles are guidelines, not laws. Apply them when they make a real change easier.
> Don't add them to code that is small and stable.
