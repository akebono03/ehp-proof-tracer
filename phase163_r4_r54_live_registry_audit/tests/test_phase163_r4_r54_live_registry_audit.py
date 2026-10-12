import copy
import json
import sys
from enum import Enum
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_r54_live_registry_audit import audit, observe_bridge, write_results

ROOT = Path(__file__).resolve().parents[2]


def source():
    path = ROOT / "phase163_r4_r53_output" / "overlap_audit.json"
    return json.loads(path.read_text(encoding="utf-8"))


class Status(str, Enum):
    METADATA_ONLY = "metadata_only"
    UNRESOLVED_SOURCE = "unresolved_source"
    STRUCTURED = "structured"


class Origin(str, Enum):
    FIXED_STATEMENT = "fixed_statement"
    PROOF_INTERNAL = "proof_internal"


class Kind(str, Enum):
    STATEMENT = "statement"
    DEFINITION = "definition"


def simulated_bridge(monkeypatch, entries=(('boundary', 'metadata_only', 'statement', 'fixed_statement'), ('theorem_fact', 'unresolved_source', None, None))):
    monkeypatch.setitem(sys.modules, "phase163_r4_registry_bridge", SimpleNamespace(MigrationStatus=Status))
    monkeypatch.setitem(sys.modules, "unified_statement_registry", SimpleNamespace(AssertionKind=Kind, AssertionOrigin=Origin))
    assertions = {}
    refs = {}
    records = []
    for i, (src, stat, kind, origin) in enumerate(entries):
        assertion_id = f"a{i}" if stat != 'unresolved_source' else None
        records.append(SimpleNamespace(source=src, source_key=str(i), assertion_id=assertion_id, status=Status(stat)))
        if assertion_id:
            assertions[assertion_id] = SimpleNamespace(assertion_id=assertion_id, reference_id=f"r{i}",
                origin=Origin(origin), kind=Kind(kind), content=SimpleNamespace())
            refs[f"r{i}"] = SimpleNamespace(locator=f"({i}.1)")
    registry = SimpleNamespace(assertion=lambda k: assertions[k], reference=lambda k: refs[k])
    return SimpleNamespace(records=records, registry=registry)


def test_input_has_all_19_candidates(monkeypatch):
    result = audit(source(), simulated_bridge(monkeypatch))
    assert result["definition_candidate_count"] == 19
    assert result["semantic_overlap_unresolved_count"] == 19
    assert result["live_registry_bridge_constructed"]


def test_metadata_only_never_comparable(monkeypatch):
    result = audit(source(), simulated_bridge(monkeypatch))
    assert result["live_bridge_typed_fixed_definition_count"] == 0
    assert all(row["live_comparison_status"] == "UNRESOLVED_NO_COMPARABLE_FIXED_DEFINITION" for row in result["candidates"])


def test_typed_fixed_definition_requires_comparison(monkeypatch):
    bridge = simulated_bridge(monkeypatch, (("theorem_fact", "structured", "definition", "fixed_statement"),))
    result = audit(source(), bridge)
    assert result["live_bridge_typed_fixed_definition_count"] == 1
    assert all(row["live_comparison_status"] == "UNRESOLVED_TYPED_COMPARISON_REQUIRED" for row in result["candidates"])
    assert result["new_statement_confirmed_count"] == 0


def test_proof_internal_never_counted_as_fixed(monkeypatch):
    bridge = simulated_bridge(monkeypatch, (("proof_repository", "structured", "definition", "proof_internal"),))
    result = audit(source(), bridge)
    assert result["live_bridge_typed_fixed_definition_count"] == 0
    assert not result["proof_repository_included"]


def test_metadata_definition_not_treated_as_typed(monkeypatch):
    bridge = simulated_bridge(monkeypatch, (("boundary", "metadata_only", "definition", "fixed_statement"),))
    result = audit(source(), bridge)
    assert result["live_bridge_typed_fixed_definition_count"] == 0


def test_duplicate_candidate_rejected(monkeypatch):
    data = source()
    data["candidates"][1]["r48_index"] = data["candidates"][0]["r48_index"]
    with pytest.raises(ValueError, match="candidate integrity"):
        audit(data, simulated_bridge(monkeypatch))


def test_mutating_candidate_rejected(monkeypatch):
    data = source()
    data["candidates"][0]["registration_action"] = "ADD"
    with pytest.raises(ValueError, match="mutating candidate"):
        audit(data, simulated_bridge(monkeypatch))


def test_prior_phase_is_required(monkeypatch):
    data = source()
    data["phase"] = "163 R4-R52"
    with pytest.raises(ValueError, match="expected R4-R53"):
        audit(data, simulated_bridge(monkeypatch))


def test_export_and_inputs_unmodified(monkeypatch, tmp_path):
    data = source()
    before = copy.deepcopy(data)
    result = audit(data, simulated_bridge(monkeypatch))
    write_results(result, tmp_path)
    assert data == before
    assert {p.name for p in tmp_path.iterdir()} == {"live_audit.json", "comparison_queue.csv", "report.md"}
    assert len(json.loads((tmp_path / "live_audit.json").read_text(encoding="utf-8"))["candidates"]) == 19
