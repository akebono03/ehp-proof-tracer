"""Focused order, provenance and fail-closed tests for R10E4."""
from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path

import pytest

from proof import ProofRule, ProofStep
from phase169_r10e4_ordered_db_prior.db_prior import (
    DB_LOCATOR_PREFIX,
    admitted_db_step,
    exact_prior_database_result,
    group_coordinates,
    precedes_db_goal,
    verified_db_step,
)


def _csv(tmp_path: Path) -> Path:
    path = tmp_path / "sphere.csv"
    columns = ("id", "n", "k", "orders", "generator", "Element", "gen_coe")
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=columns)
        writer.writeheader()
        writer.writerows((
            {"id": 0, "n": 3, "k": 1, "orders": 2, "generator": "η_3", "Element": "", "gen_coe": ""},
            {"id": 1, "n": 4, "k": 1, "orders": 2, "generator": "η_4", "Element": "", "gen_coe": ""},
            {"id": 2, "n": 2, "k": 2, "orders": 0, "generator": "0", "Element": "", "gen_coe": ""},
        ))
    return path


def test_r10e4_strict_order_by_stem_then_sphere_dimension():
    assert precedes_db_goal(99, 1, 2, 2)
    assert precedes_db_goal(3, 4, 9, 4)
    assert not precedes_db_goal(9, 4, 3, 4)
    assert not precedes_db_goal(3, 4, 3, 4)
    assert not precedes_db_goal(2, 5, 99, 4)
    assert not precedes_db_goal(True, 1, 4, 1)
    assert not precedes_db_goal(1, 1, 4, 1)


def test_r10e4_explicit_db_rows_only_no_stable_fallback(tmp_path):
    source = _csv(tmp_path)
    one_stem = exact_prior_database_result(3, 1, csv_path=source)
    assert group_coordinates(one_stem) == (3, 1)
    assert exact_prior_database_result(10, 1, csv_path=source) is None
    assert exact_prior_database_result(3, 3, csv_path=source) is None


def test_r10e4_prior_same_stem_and_cross_stem_are_admitted(tmp_path):
    source = _csv(tmp_path)
    earlier = exact_prior_database_result(3, 1, csv_path=source)
    later = exact_prior_database_result(4, 1, csv_path=source)
    zero = exact_prior_database_result(2, 2, csv_path=source)
    assert earlier is not None and later is not None and zero is not None
    step = admitted_db_step(earlier, proof_target=later, csv_path=source)
    assert isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
    assert DB_LOCATOR_PREFIX in step.inference_rule.literature_reference.locator
    assert admitted_db_step(later, proof_target=earlier, csv_path=source) is None
    assert admitted_db_step(earlier, proof_target=earlier, csv_path=source) is None
    # A smaller stem may have a larger n and still be an earlier prior result.
    across = admitted_db_step(later, proof_target=zero, csv_path=source)
    assert across is not None


def test_r10e4_same_or_later_db_result_rejected_as_root_given(tmp_path):
    source = _csv(tmp_path)
    one = exact_prior_database_result(3, 1, csv_path=source)
    assert one is not None
    assert admitted_db_step(one, proof_target=one, csv_path=source) is None
    assert admitted_db_step(one, proof_target=object(), csv_path=source) is None


def test_r10e4_db_given_is_distinct_from_toda_citation(tmp_path):
    source = _csv(tmp_path)
    first = exact_prior_database_result(3, 1, csv_path=source)
    later = exact_prior_database_result(4, 1, csv_path=source)
    step = admitted_db_step(first, proof_target=later, csv_path=source)
    assert step is not None
    assert "sphere.csv" in step.inference_rule.literature_reference.locator
    assert "Proposition" not in step.inference_rule.literature_reference.locator
    assert "ADOPTED_DATABASE_PRIOR" in step.note


def test_r10e4_forged_prior_step_rejected_even_if_given(tmp_path, monkeypatch):
    source = _csv(tmp_path)
    first = exact_prior_database_result(3, 1, csv_path=source)
    later = exact_prior_database_result(4, 1, csv_path=source)
    step = admitted_db_step(first, proof_target=later, csv_path=source)
    assert step is not None
    import phase169_r10e4_ordered_db_prior.db_prior as module
    monkeypatch.setattr(module, "DEFAULT_CSV", source)
    assert verified_db_step(step, proof_target=later)
    assert not verified_db_step(replace(step, note="claimed prior"), proof_target=later)
    assert not verified_db_step(replace(step, premises=(step,)), proof_target=later)
    assert not verified_db_step(replace(step, rule=ProofRule.INFERENCE), proof_target=later)
    assert not verified_db_step(step, proof_target=first)


def test_r10e4_db_step_requires_unchanged_typed_db_content(tmp_path, monkeypatch):
    source = _csv(tmp_path)
    first = exact_prior_database_result(3, 1, csv_path=source)
    later = exact_prior_database_result(4, 1, csv_path=source)
    step = admitted_db_step(first, proof_target=later, csv_path=source)
    assert step is not None
    import phase169_r10e4_ordered_db_prior.db_prior as module
    monkeypatch.setattr(module, "DEFAULT_CSV", source)
    assert verified_db_step(step, proof_target=later)
    raw = source.read_text(encoding="utf-8")
    source.write_text(raw.replace("η_3", "ν_3"), encoding="utf-8")
    assert not verified_db_step(step, proof_target=later)


def test_r10e4_patch_is_reversible_and_functions_are_complete():
    from phase169_r10e4_ordered_db_prior.patch import TARGETS, transform
    base = Path(__file__).resolve().parents[2]
    directory = base / "phase169_r10e4_ordered_db_prior" / "output"
    for path in TARGETS:
        before = directory / (Path(path).name + ".before")
        if not before.is_file():
            pytest.skip("patch did not run: test is for the installed workflow")
        raw = before.read_bytes()
        patched, functions = transform(path, raw)
        assert patched != raw
        assert functions
        with pytest.raises(RuntimeError):
            transform(path, patched)


def test_r10e4_trust_boundary_accepts_only_a_revalidated_ordered_db_given(tmp_path, monkeypatch):
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase168_r3_41p13_trust_boundary.verification import (
        UnverifiedProofTree, verify_proof_tree_for_narrative,
    )
    from proof import InferenceRule, PremisePattern, Relation
    from unified_statement_registry import UnifiedStatementRegistry
    import phase169_r10e4_ordered_db_prior.db_prior as db_module

    path = _csv(tmp_path)
    source = exact_prior_database_result(3, 1, csv_path=path)
    target = exact_prior_database_result(4, 1, csv_path=path)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(db_module, "DEFAULT_CSV", path)
    cited_prior = admitted_db_step(source, proof_target=target, bridge=bridge)
    assert cited_prior is not None
    rule = InferenceRule(
        name="test-only typed inference using previously adopted DB group",
        premise_patterns=(PremisePattern(statement_type=Relation, statement_pattern=source),),
        conclusion_pattern=target,
    )
    root_step = ProofStep(
        conclusion=target, premises=(cited_prior,), rule=ProofRule.INFERENCE,
        inference_rule=rule,
    )
    result = make_partial_proof_result(
        n=4, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(cited_prior, root_step), conclusion=target,
    )
    assert verify_proof_tree_for_narrative(
        result, bridge, citing_assertion_id=None,
        derived_target_without_citing_id=True,
    ) == (1, 1)

    fake = replace(cited_prior, note="false data claim")
    bad_root = replace(root_step, premises=(fake,))
    bad = make_partial_proof_result(
        n=4, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fake, bad_root), conclusion=target,
    )
    with pytest.raises(UnverifiedProofTree, match="GIVEN"):
        verify_proof_tree_for_narrative(
            bad, bridge, citing_assertion_id=None,
            derived_target_without_citing_id=True,
        )
