# Testable Design

Code is **testable** when you can check its behaviour quickly, reliably, and without
real emails, real databases, real money or real time passing.

> **Everyday analogy:** A flight simulator.
> Pilots practise engine failures in a simulator, not on a real plane full of passengers.
> To make that possible, the cockpit controls have to work with both the real plane *and* the simulator.

## Two key ideas

| Idea | Simple meaning | File |
| --- | --- | --- |
| **Isolate side effects** | Keep "thinking" code (calculations, decisions) separate from "doing" code (network, files, clock, randomness). Pure logic is easy to test. | [isolating_side_effects.py](isolating_side_effects.py) |
| **Lightweight fakes** | Small hand-written stand-ins (an in-memory DB, a fake email sender) that behave like the real thing for tests. | [fakes.py](fakes.py) |
| **Real tests** | A pytest file that tests the code above. | [test_examples.py](test_examples.py) |

## Fakes vs mocks, in one line each

- **Fake:** a simple working version (e.g. a dictionary instead of a database). Tests check the *result*.
- **Mock:** an object that records calls (`unittest.mock`). Tests check *how* it was called. Useful, but overusing mocks ties tests to implementation details.

Prefer fakes for your own interfaces. Use mocks for awkward third-party code.

## Run the examples

```bash
python testable-design/isolating_side_effects.py
python testable-design/fakes.py

pip install pytest
pytest testable-design/
```
