# Case Studies

These are realistic backend scenarios. Each one **combines several ideas** from the other folders,
so you can see how they work together in real code.

| Case study | Everyday picture | Concepts used | File |
| --- | --- | --- | --- |
| **Notification service** | A school that informs parents by SMS, email or app, depending on each parent's preference. | Protocols, Strategy, Factory, Observer, DI | [notification_service.py](notification_service.py) |
| **Data import pipeline** | A factory assembly line: unload → inspect → package → store. Each station does one job. | SRP, separation of concerns, error handling, testable design | [data_import_pipeline.py](data_import_pipeline.py) |
| **File storage service** | A locker service that can use a home cupboard, a bank locker or a warehouse. The customer experience is the same. | Ports & adapters, Adapter, DIP, DI | [file_storage_service.py](file_storage_service.py) |
| **Order processing** | An online shop's checkout: check stock, take payment, save the order, send a confirmation. | Layered architecture, Repository, Unit of Work, custom exceptions, fakes | [order_processing.py](order_processing.py) |

## How to study a case

1. Read the docstring at the top. It describes the business problem.
2. Find the **core logic** and notice that it doesn't import any infrastructure.
3. Find the **adapters and fakes** and see how they plug in.
4. Run it, then try the exercise listed at the bottom of each file.

## Run the examples

```bash
python case-studies/notification_service.py
python case-studies/data_import_pipeline.py
python case-studies/file_storage_service.py
python case-studies/order_processing.py
```
