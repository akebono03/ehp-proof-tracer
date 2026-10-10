"""Phase 163 R4-R14: literature identity and placement, separate from proof use."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import json
from pathlib import Path


class SourceStatus(str, Enum):
    UNCHECKED = "unchecked"
    VERIFIED = "verified"


class SearchStatus(str, Enum):
    UNCONNECTED = "unconnected"
    CONNECTED = "connected"
    VERIFIED = "verified"


@dataclass(frozen=True)
class LiteratureEntry:
    statement_id: str
    chapter: int
    section: str
    order_key: str
    kind: str
    locator: str
    source_status: SourceStatus = SourceStatus.UNCHECKED
    search_status: SearchStatus = SearchStatus.UNCONNECTED
    statement_type: str | None = None
    hypotheses: str | None = None
    variable_range: str | None = None
    existing_component_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.statement_id or not self.locator or not self.kind:
            raise ValueError("ID, locator and kind are required")
        if not 1 <= self.chapter <= 5:
            raise ValueError("chapter must be 1..5")
        if Fraction(self.order_key) <= 0:
            raise ValueError("order_key must be positive")
        if len(set(self.existing_component_keys)) != len(self.existing_component_keys):
            raise ValueError("duplicate existing component mappings")
        if self.search_status == SearchStatus.VERIFIED and self.source_status != SourceStatus.VERIFIED:
            raise ValueError("search verification requires source verification")


def validate_catalog(entries: tuple[LiteratureEntry, ...]) -> None:
    ids = [e.statement_id for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("statement_id already allocated")
    places = [(e.chapter, e.section, Fraction(e.order_key)) for e in entries]
    if len(places) != len(set(places)):
        raise ValueError("publication position conflict")
    component_keys = [(e.locator, key) for e in entries for key in e.existing_component_keys]
    if len(component_keys) != len(set(component_keys)):
        raise ValueError("duplicate legacy mapping")


def publication_order(entries: tuple[LiteratureEntry, ...]) -> tuple[LiteratureEntry, ...]:
    validate_catalog(entries)
    return tuple(sorted(entries, key=lambda e: (e.chapter, e.section, Fraction(e.order_key))))


def insert_between(left: LiteratureEntry, right: LiteratureEntry) -> str:
    if (left.chapter, left.section) != (right.chapter, right.section):
        raise ValueError("anchors must be in same chapter and section")
    a, b = Fraction(left.order_key), Fraction(right.order_key)
    if a >= b:
        raise ValueError("anchors out of order")
    middle = (a + b) / 2
    return str(middle.numerator) if middle.denominator == 1 else f"{middle.numerator}/{middle.denominator}"


def load_catalog(path: Path) -> tuple[LiteratureEntry, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = tuple(LiteratureEntry(
        **{**row,
           "source_status": SourceStatus(row.get("source_status", "unchecked")),
           "search_status": SearchStatus(row.get("search_status", "unconnected")),
           "existing_component_keys": tuple(row.get("existing_component_keys", ()))})
        for row in payload["entries"])
    validate_catalog(entries)
    return entries


def save_catalog(path: Path, entries: tuple[LiteratureEntry, ...]) -> None:
    from dataclasses import asdict
    validate_catalog(entries)
    path.write_text(json.dumps({"schema_version": 1, "entries": [asdict(e) for e in entries]},
                               indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
