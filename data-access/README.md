# Data Access Patterns

How should business code talk to a database without getting tangled up in SQL?

> **Everyday analogy:** A library.
> You don't walk into the stacks and search the shelves yourself. You ask the
> **librarian** ("find me books by this author"). The librarian knows where things are.
> That librarian is the **Repository**.

| Pattern | Simple meaning | Everyday example | File |
| --- | --- | --- | --- |
| **Repository** | A collection-like object that hides how data is stored. You call `add()`, `get()` and `list()` and never write SQL in business code. | Asking a librarian instead of searching the shelves yourself. | [repository.py](repository.py) |
| **Unit of Work** | Group several changes so they all succeed or all fail together. | A bank transfer: take money from A **and** give it to B. Never just one half. | [unit_of_work.py](unit_of_work.py) |

## Why bother?

- Business logic stays readable: `orders.get(order_id)` instead of raw SQL strings.
- Tests can use an in-memory repository, which needs no database.
- Changing the database (SQLite → Postgres) only touches the repository.

## Run the examples

```bash
python data-access/repository.py
python data-access/unit_of_work.py
```

Both use Python's built-in `sqlite3` with an in-memory database, so there's nothing to install.
