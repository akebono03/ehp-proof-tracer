"""Targeted, read-only R2 tests; never certify a mathematical fact."""
from pathlib import Path

import pytest

from phase166_r2_assertion_binding.audit import ASSERTION_ID, candidate_binding, inspect
from phase165_r4_production_connection import discover_production_registry
from proof import Relation, RelationType


def test_candidate_instantiation_does_not_change_registry():
    registry = discover_production_registry().bridge.registry
    before = registry.assertion(ASSERTION_ID).content
    instance, typing, component = candidate_binding(registry)
    assert isinstance(instance.concrete_content, Relation)
    assert instance.concrete_content.relation_type is RelationType.EQUALITY
    assert instance.assertion_id == ASSERTION_ID
    assert typing["homotopy_group"] == "pi_6^3"
    assert component.component_key == "nu_prime_double_relation"
    assert registry.assertion(ASSERTION_ID).content is before
    assert before != instance.concrete_content


def test_candidate_rows_cannot_grant_permission():
    registry = discover_production_registry().bridge.registry
    source = Path(__file__).resolve().parent.parent / "sphere_relation2.csv"
    if not source.is_file():
        source = Path(__file__).resolve().parent.parent / "phase166_r1_source_registry_audit" / "sphere_relation2.csv"
    result = inspect(source, registry)
    assert result["candidate_count"] == 2
    assert result["proof_permission_granted"] == 0
    assert result["mathematical_identity_confirmed"] == 0
    assert result["proof_step_links_created"] == 0
    assert all(row["status"] == "CANDIDATE_DISPLAY_AND_TYPE_ONLY" for row in result["binding_candidates"])


def test_missing_source_fails_closed(tmp_path):
    registry = discover_production_registry().bridge.registry
    with pytest.raises(FileNotFoundError):
        inspect(tmp_path / "missing.csv", registry)
