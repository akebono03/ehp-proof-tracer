"""Focused R3 tests; local synthetic review positions do not certify Toda."""
from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase164_r3_registry_search_connection import (
    RegisteredLiteraturePremise,
    reconstruct_phase164_r3_pi5_3,
    select_phase164_r3_pi5_3_leaves,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def make_case(*, available=1, metadata=False, archive=False):
    leaves = build_phase59_3_data()["premise_steps"]
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    exactness = tuple(
        step for step in leaves if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    assert len(literature) == 2 and len(exactness) == 4
    roots = {}
    visited = set()

    def walk(step):
        if id(step) in visited:
            return
        visited.add(id(step))
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        for premise in step.premises:
            walk(premise)

    for step in leaves:
        walk(step)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "fixture:source", ReferenceKind.PROPOSITION, "Fixture source", "test-source",
        publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "fixture:goal", ReferenceKind.PROPOSITION, "Fixture citing", "test-source",
        publication_position=2,
    ))
    records = []
    bindings = []
    for i, step in enumerate(literature):
        identifier = f"fixture:statement:{i}"
        registry.add_assertion(AssertionEntry(
            identifier, "fixture:source", AssertionKind.STATEMENT,
            step.conclusion,
            origin=AssertionOrigin.SOURCE_ARCHIVE if archive else AssertionOrigin.FIXED_STATEMENT,
            available_after_position=available,
        ))
        records.append(MigrationRecord(
            "fixture", identifier, identifier,
            MigrationStatus.METADATA_ONLY if metadata else MigrationStatus.STRUCTURED,
            "Synthetic local test record",
        ))
        bindings.append(RegisteredLiteraturePremise(identifier, step))
    registry.add_assertion(AssertionEntry(
        "fixture:target", "fixture:goal", AssertionKind.STATEMENT, "target",
    ))
    return (
        RegistryBridgeResult(registry, tuple(records), ()),
        tuple(bindings), exactness, tuple(roots.values()),
    )


def invoke(case, *, verified=None):
    bridge, bindings, exactness, roots = case
    if verified is None:
        verified = tuple(item.assertion_id for item in bindings)
    return select_phase164_r3_pi5_3_leaves(
        bridge, "fixture:target", bindings, exactness, roots,
        verified_assertion_ids=verified,
    )


def test_r3_selects_same_existing_six_leaf_objects():
    case = make_case()
    result = invoke(case)
    expected = tuple(item.step for item in case[1]) + case[2]
    assert len(result.available_leaf_steps) == 6
    assert all(a is b for a, b in zip(result.available_leaf_steps, expected))
    assert len(result.accepted_assertion_ids) == 2


def test_r3_reconstructs_pi5_3_with_unchanged_phase161_rules():
    bridge, bindings, exactness, roots = make_case()
    result = reconstruct_phase164_r3_pi5_3(
        bridge, "fixture:target", bindings, exactness, roots,
        verified_assertion_ids=tuple(item.assertion_id for item in bindings),
    )
    assert len(result.reconstruction.derived_steps) == 7
    assert result.reconstruction.final_step is result.reconstruction.derived_steps[-1]
    assert result.provenance.verified_inferences >= 7


def test_r3_rejects_unreviewed_citation():
    with pytest.raises(ValueError, match="independent_verification_not_recorded"):
        invoke(make_case(), verified=())


@pytest.mark.parametrize("options,reason", [
    ({"metadata": True}, "metadata_only"),
    ({"archive": True}, "source_archive_not_verified"),
    ({"available": 2}, "not_available_before_citing_entry"),
    ({"available": None}, "availability_position_unverified"),
])
def test_r3_rejects_metadata_archive_late_or_unknown(options, reason):
    with pytest.raises(ValueError, match=reason):
        invoke(make_case(**options))


def test_r3_rejects_wrong_statement_binding():
    bridge, bindings, exactness, roots = make_case()
    wrong = replace(bindings[0], assertion_id=bindings[1].assertion_id)
    with pytest.raises(ValueError, match="registered conclusion mismatch|duplicate assertion binding"):
        select_phase164_r3_pi5_3_leaves(
            bridge, "fixture:target", (wrong, bindings[1]), exactness, roots,
            verified_assertion_ids=tuple(item.assertion_id for item in bindings),
        )


def test_r3_rejects_missing_exactness():
    bridge, bindings, exactness, roots = make_case()
    with pytest.raises(ValueError, match="four exactness witnesses"):
        select_phase164_r3_pi5_3_leaves(
            bridge, "fixture:target", bindings, exactness[:-1], roots,
            verified_assertion_ids=tuple(item.assertion_id for item in bindings),
        )


def test_r3_rejects_untrusted_given_root():
    bridge, bindings, exactness, roots = make_case()
    with pytest.raises(ValueError, match="Untrusted GIVEN provenance root"):
        select_phase164_r3_pi5_3_leaves(
            bridge, "fixture:target", bindings, exactness, roots[:-1],
            verified_assertion_ids=tuple(item.assertion_id for item in bindings),
        )


def test_r3_rejects_duplicate_step_identity():
    bridge, bindings, exactness, roots = make_case()
    with pytest.raises(ValueError, match="duplicate proof step identity"):
        select_phase164_r3_pi5_3_leaves(
            bridge, "fixture:target", bindings, (exactness[0],) * 4, roots,
            verified_assertion_ids=tuple(item.assertion_id for item in bindings),
        )
