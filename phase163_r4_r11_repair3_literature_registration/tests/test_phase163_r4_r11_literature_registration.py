from dataclasses import replace

import pytest

from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r11_literature_registration import (
    ALL_KEYS,
    LiteratureAssertionInput,
    existing_prop56_candidates,
    register_prop56_literature_statements,
)
from proof import Relation
from scalar_rules import ScalarGreaterEqualStatement


def _base_and_inputs():
    return build_registry_bridge(), existing_prop56_candidates()


def test_r4_r11_repair3_registers_five_typed_literature_candidates():
    base, candidates = _base_and_inputs()
    result = register_prop56_literature_statements(base, candidates)
    assert tuple(item.component_key for item in candidates) == ALL_KEYS
    assert len(result.evidence) == 5
    for candidate in candidates:
        assertion_id = f"boundary:Proposition 5.6:{candidate.component_key}"
        assertion = result.snapshot.registry.assertion(assertion_id)
        assert assertion.content is candidate.statement
        assert any(
            record.assertion_id == assertion_id and record.status is MigrationStatus.STRUCTURED
            for record in result.snapshot.records
        )
    assert all(e.verification_status == "SOURCE_UNVERIFIED" for e in result.evidence)
    assert all(e.proof_status == "PROOF_ANCESTRY_NOT_CHECKED" for e in result.evidence)


def test_r4_r11_repair3_does_not_modify_base_or_add_proof_links():
    base, candidates = _base_and_inputs()
    original_links = base.proof_links
    result = register_prop56_literature_statements(base, candidates)
    assert result.snapshot.proof_links == original_links
    for candidate in candidates:
        assertion_id = f"boundary:Proposition 5.6:{candidate.component_key}"
        assert any(
            record.assertion_id == assertion_id and record.status is MigrationStatus.METADATA_ONLY
            for record in base.records
        )
        assert base.registry.assertion(assertion_id).content != candidate.statement


def test_r4_r11_repair3_rejects_missing_component():
    base, candidates = _base_and_inputs()
    with pytest.raises(ValueError, match="five distinct"):
        register_prop56_literature_statements(base, candidates[:-1])


def test_r4_r11_repair3_rejects_duplicate_component():
    base, candidates = _base_and_inputs()
    with pytest.raises(ValueError, match="five distinct"):
        register_prop56_literature_statements(base, candidates[:-1] + (candidates[0],))


def test_r4_r11_repair3_rejects_wrong_generator():
    base, candidates = _base_and_inputs()
    bad = candidates[1]
    relation = bad.statement
    assert isinstance(relation, Relation)
    changed = replace(relation, rhs=FiniteCyclicGroup(order=4, generator="wrong"))
    inputs = candidates[:1] + (replace(bad, statement=changed),) + candidates[2:]
    with pytest.raises(ValueError, match="generator"):
        register_prop56_literature_statements(base, inputs)


def test_r4_r11_repair3_requires_typed_higher_scope():
    base, candidates = _base_and_inputs()
    changed = candidates[:-1] + (replace(candidates[-1], scope_statement=None),)
    with pytest.raises(ValueError, match="typed scope"):
        register_prop56_literature_statements(base, changed)


def test_r4_r11_repair3_rejects_false_scope():
    base, candidates = _base_and_inputs()
    scope = candidates[-1].scope_statement
    assert isinstance(scope, ScalarGreaterEqualStatement)
    changed = candidates[:-1] + (
        replace(candidates[-1], scope_statement=replace(scope, right=5)),
    )
    with pytest.raises(ValueError, match="scope"):
        register_prop56_literature_statements(base, changed)


def test_r4_r11_repair3_rejects_prior_structured_target():
    base, candidates = _base_and_inputs()
    result = register_prop56_literature_statements(base, candidates)
    with pytest.raises(ValueError, match="metadata-only"):
        register_prop56_literature_statements(result.snapshot, candidates)
