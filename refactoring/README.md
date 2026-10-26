# Refactoring

**Refactoring** means improving the *structure* of code **without changing what it does**.

> **Everyday analogy:** Reorganising your kitchen.
> You move spices next to the stove and put the plates near the sink. You still cook
> the same meals, just faster and with less mess. If dinner tastes different afterwards,
> that wasn't refactoring. You changed the recipe.

## The safe refactoring loop

1. **Pin the behaviour with tests** before touching anything.
2. Make **one small change** (rename, extract a function, remove duplication...).
3. **Run the tests.** Still green? Continue. Red? Undo the last step.
4. Repeat.

## Files

| File | What it shows |
| --- | --- |
| [before.py](before.py) | A messy but working movie-ticket pricing function. |
| [after.py](after.py) | The same behaviour, refactored step by step (steps explained in comments). |
| [test_behaviour.py](test_behaviour.py) | Tests that run against **both** versions to prove nothing changed. |

## Common refactorings (with plain names)

| Name | What you do |
| --- | --- |
| Rename | Give a variable or function a name that says what it means (`x` → `ticket_price`). |
| Extract function | Move a chunk of code into a well-named function. |
| Replace magic numbers | `0.9` → `SENIOR_DISCOUNT = 0.9`. |
| Guard clauses | Handle special cases early with `return`, to avoid deep nesting. |
| Replace conditional with lookup | Long if/elif chains → a dictionary. |

## Run the examples

```bash
python refactoring/before.py
python refactoring/after.py
pytest refactoring/
```
