# Error Handling

Good error handling answers three questions:
1. **What** went wrong? (clear, specific exception)
2. **Where** should it be handled? (the right layer)
3. **What** does the user or caller see? (a helpful message, not a stack trace)

> **Everyday analogy:** A hospital.
> A nurse notices a problem and reports it precisely ("patient's BP is 180/120"),
> not just "something's wrong". The **doctor** decides what to do. And the family
> gets a calm, understandable update, not the raw medical chart.

| Topic | Simple meaning | File |
| --- | --- | --- |
| **Meaningful exceptions** | Create your own exception types that name the problem, e.g. `InsufficientStock` instead of `Exception("error")`. | [custom_exceptions.py](custom_exceptions.py) |
| **Error boundaries** | Catch errors at the edge of the app (API, CLI) and turn them into friendly responses. Don't catch them everywhere. | [error_boundaries.py](error_boundaries.py) |

## Quick rules

- ✅ Raise **specific** exceptions. Catch **specific** exceptions.
- ✅ Let errors travel up to the layer that can actually do something about them.
- ✅ Keep the original cause: `raise NewError(...) from original_error`.
- ❌ Don't use a bare `except:` or `except Exception: pass`. That hides bugs.
- ❌ Don't use exceptions for normal control flow (e.g. "user not found" in a search is often a normal `None`).

## Run the examples

```bash
python error-handling/custom_exceptions.py
python error-handling/error_boundaries.py
```
