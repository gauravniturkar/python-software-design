# Application Architecture

Architecture is **how you arrange the big pieces** of an application, and which pieces are allowed to talk to which.

> **Everyday analogy:** A restaurant.
> - **Waiters** talk to customers (the API / UI layer).
> - **Chefs** follow recipes (business logic).
> - **The storeroom** holds ingredients (database / storage).
>
> Customers never walk into the storeroom, and the storeroom never takes orders.

## Two common styles

| Style | Simple meaning | File |
| --- | --- | --- |
| **Layered architecture** | Stack the code in layers: presentation → service → data. Each layer only calls the one below it. | [layered.py](layered.py) |
| **Ports and adapters** (Hexagonal) | Business logic sits in the centre and defines "ports" (interfaces). The outside world (DB, web, email) plugs in through "adapters". | [ports_and_adapters.py](ports_and_adapters.py) |

```
Layered                         Ports & Adapters
-------                         ----------------
 [ API / UI ]                       Web API     CLI
      |                                \       /
 [ Services ]                      [  Core business  ]
      |                             (defines ports)
 [ Data access ]                       /       \
      |                          Postgres     Email
 [ Database ]                    adapter      adapter
```

## The key rule: dependencies point inward

Business rules are the most valuable and most stable part of your app.
They should **not** import Flask, SQLAlchemy or boto3. Those tools are details that
plug into the business rules, not the other way round.

## Run the examples

```bash
python architecture/layered.py
python architecture/ports_and_adapters.py
```
