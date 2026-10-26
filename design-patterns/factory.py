"""
FACTORY PATTERN
"One place decides WHICH object to create, so callers don't have to."

Analogy: ordering at a coffee shop.
You say "one latte". You don't tell the barista how much milk, which beans
or what temperature. The barista (the factory) knows how to make it.

PROBLEM
Code all over the app does `if type == "pdf": PdfExporter() elif ...`.
Adding a new format means hunting down every one of those places.
"""
from typing import Protocol


class Exporter(Protocol):
    def export(self, data: dict) -> str: ...


class JsonExporter:
    def export(self, data: dict) -> str:
        import json
        return json.dumps(data)


class CsvExporter:
    def export(self, data: dict) -> str:
        header = ",".join(data.keys())
        row = ",".join(str(v) for v in data.values())
        return f"{header}\n{row}"


class XmlExporter:
    def export(self, data: dict) -> str:
        fields = "".join(f"<{k}>{v}</{k}>" for k, v in data.items())
        return f"<record>{fields}</record>"


# ---------------------------------------------------------------------------
# THE FACTORY: the only place that maps a name to a class
# ---------------------------------------------------------------------------
_EXPORTERS: dict[str, type] = {
    "json": JsonExporter,
    "csv": CsvExporter,
    "xml": XmlExporter,
}


def create_exporter(file_format: str) -> Exporter:
    try:
        return _EXPORTERS[file_format.lower()]()
    except KeyError:
        supported = ", ".join(_EXPORTERS)
        raise ValueError(f"Unsupported format '{file_format}'. Use: {supported}")


if __name__ == "__main__":
    report = {"name": "Asha", "orders": 3}

    # The caller only knows the format name, which could come from a
    # config file or a user's dropdown choice.
    for fmt in ["json", "csv", "xml"]:
        exporter = create_exporter(fmt)
        print(f"{fmt}: {exporter.export(report)}")

    try:
        create_exporter("pdf")
    except ValueError as error:
        print("Error:", error)

# TRADE-OFFS
# + New format = new class + one line in the dictionary.
# + Creation logic (config, setup) lives in one place.
# - An extra layer of indirection. If you always know the class at write
#   time, just call it directly: JsonExporter().
