from pathlib import Path
from dataclasses import replace
import pytest
from phase163_r4_r14_catalog.toda_literature_catalog import (
    LiteratureEntry, SourceStatus, SearchStatus, insert_between,
    load_catalog, publication_order, save_catalog, validate_catalog,
)


def item(sid: str, position: str, **kw) -> LiteratureEntry:
    return LiteratureEntry(sid, 1, "1", position, "Lemma", sid, **kw)


def test_insertion_keeps_original_ids():
    a, b = item("TODA-S000001", "1"), item("TODA-S000002", "2")
    inserted = item("TODA-S000003", insert_between(a, b))
    assert [x.statement_id for x in publication_order((b, inserted, a))] == [
        "TODA-S000001", "TODA-S000003", "TODA-S000002"
    ]


def test_duplicate_id_and_placement_rejected():
    with pytest.raises(ValueError, match="statement_id"):
        validate_catalog((item("x", "1"), item("x", "2")))
    with pytest.raises(ValueError, match="position"):
        validate_catalog((item("x", "1"), item("y", "1")))


def test_unverified_source_cannot_be_search_verified():
    with pytest.raises(ValueError, match="source verification"):
        item("x", "1", search_status=SearchStatus.VERIFIED)


def test_roundtrip_and_legacy_mapping(tmp_path: Path):
    entries = (item("x", "1", source_status=SourceStatus.VERIFIED,
                    existing_component_keys=("old_key",)),)
    filename = tmp_path / "catalog.json"
    save_catalog(filename, entries)
    assert load_catalog(filename) == entries


def test_duplicate_legacy_mapping_rejected():
    with pytest.raises(ValueError, match="legacy mapping"):
        validate_catalog((item("x", "1", existing_component_keys=("k",)),
                          replace(item("y", "2", existing_component_keys=("k",)), locator="x")))
