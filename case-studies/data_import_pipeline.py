"""
CASE STUDY: DATA IMPORT PIPELINE

Everyday picture: a factory assembly line.
  Station 1 unloads boxes (READ)
  Station 2 inspects for damage (VALIDATE)
  Station 3 repackages (TRANSFORM)
  Station 4 puts them on shelves (SAVE)
Each station does ONE job. A damaged box is set aside with a note, and the
line keeps moving.

Requirements
  - Import employees from CSV.
  - Bad rows must not stop the whole import. Collect them in an error report.
  - Later, the source may become an Excel file or an API, and the destination
    may become a real database.

Concepts used
  Single Responsibility (solid/)            -> one class per station
  Separation of concerns                    -> read / validate / transform / save
  Custom exceptions (error-handling/)       -> InvalidRow
  Isolated side effects (testable-design/)  -> validation and transformation are pure
  Dependency Inversion                      -> the pipeline depends on Source / Sink protocols
"""
import csv
import io
from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass
class Employee:
    email: str
    name: str
    salary: int
    department: str


class InvalidRow(Exception):
    pass


# ---------------------------------------------------------------------------
# Station 1: READ (side effect: reads input)
# ---------------------------------------------------------------------------
class Source(Protocol):
    def rows(self) -> Iterable[dict[str, str]]: ...


class CsvSource:
    def __init__(self, file_obj):
        self.file_obj = file_obj

    def rows(self) -> Iterable[dict[str, str]]:
        return csv.DictReader(self.file_obj)


# ---------------------------------------------------------------------------
# Station 2: VALIDATE (pure: no I/O, easy to test)
# ---------------------------------------------------------------------------
def validate(row: dict[str, str]) -> dict[str, str]:
    if "@" not in row.get("email", ""):
        raise InvalidRow(f"bad email '{row.get('email')}'")
    if not row.get("name", "").strip():
        raise InvalidRow("name is empty")
    if not row.get("salary", "").isdigit():
        raise InvalidRow(f"salary '{row.get('salary')}' is not a number")
    return row


# ---------------------------------------------------------------------------
# Station 3: TRANSFORM (pure)
# ---------------------------------------------------------------------------
def transform(row: dict[str, str]) -> Employee:
    return Employee(
        email=row["email"].strip().lower(),
        name=row["name"].strip().title(),
        salary=int(row["salary"]),
        department=(row.get("department") or "unassigned").strip().upper(),
    )


# ---------------------------------------------------------------------------
# Station 4: SAVE (side effect: writes output)
# ---------------------------------------------------------------------------
class Sink(Protocol):
    def save(self, employee: Employee) -> None: ...


class InMemorySink:
    def __init__(self):
        self.saved: list[Employee] = []

    def save(self, employee: Employee) -> None:
        self.saved.append(employee)


# ---------------------------------------------------------------------------
# The line manager: connects the stations, collects problems
# ---------------------------------------------------------------------------
@dataclass
class ImportReport:
    imported: int
    errors: list[str]


class ImportPipeline:
    def __init__(self, source: Source, sink: Sink):
        self.source = source
        self.sink = sink

    def run(self) -> ImportReport:
        imported, errors = 0, []
        # start=2 because line 1 of the CSV is the header
        for line_number, raw in enumerate(self.source.rows(), start=2):
            try:
                employee = transform(validate(raw))
            except InvalidRow as error:
                errors.append(f"line {line_number}: {error}")
                continue  # set the damaged box aside, keep the line moving
            self.sink.save(employee)
            imported += 1
        return ImportReport(imported, errors)


SAMPLE_CSV = """email,name,salary,department
ASHA@Example.com,  asha rao ,85000,engineering
ravi-at-example.com,Ravi Kumar,60000,sales
meera@example.com,,70000,hr
kabir@example.com,kabir singh,lots,finance
zoya@example.com,zoya khan,92000,
"""

if __name__ == "__main__":
    sink = InMemorySink()
    pipeline = ImportPipeline(CsvSource(io.StringIO(SAMPLE_CSV)), sink)
    report = pipeline.run()

    print(f"Imported {report.imported} employees:")
    for employee in sink.saved:
        print("  ", employee)
    print("Errors:")
    for error in report.errors:
        print("  ", error)

    # Pure stations are trivial to test:
    assert transform({"email": " A@B.COM ", "name": "x y", "salary": "1"}).email == "a@b.com"

# EXERCISE
#   1. Write a JsonSource that reads a list of dicts. The pipeline doesn't change.
#   2. Write a SqliteSink using data-access/repository.py as a guide.
