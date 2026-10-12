"""Focused R4-R3 checks, including rejection of corrupted typed clauses."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import source_crosswalk
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def inputs():
    manifest = json.loads((ROOT / "phase163_r4_r94_output" / "manifest.json").read_text(encoding="utf-8"))
    leaves = tuple(step for step in build_phase59_3_data()["premise_steps"]
                   if step.rule is ProofRule.INFERENCE
                   and not isinstance(step.conclusion, TodaProp42ExactnessStatement))
    return source_crosswalk(manifest, leaves), leaves


def test_typed_clauses_consistent(inputs):
    report = assess_typed_clauses(*inputs)
    assert report["typed_checks_passed"] == 5
    assert all(report["typed_checks"].values())
    assert report["source_statement_ids"] == ["toda:tex:ch5:0002", "toda:tex:ch5:0005"]


def test_must_not_authorize_citation(inputs):
    report = assess_typed_clauses(*inputs)
    assert not report["citation_eligible"]
    assert not report["typed_registry_binding_written"]
    assert not report["proof_search_connected"]
    assert not report["independent_original_edition_verified"]
    assert not report["independent_mathematical_truth_verified"]
    assert not report["publication_and_availability_verified"]


def test_universal_and_extra_clauses_not_claimed(inputs):
    report = assess_typed_clauses(*inputs)
    assert not report["proposition_5_1_universal_range_verified"]
    assert not report["proposition_5_1_stable_clause_covered"]
    assert not report["equation_5_3_double_nu_clause_covered"]


def test_corrupted_prop51_delta_coefficient_rejected(inputs):
    crosswalk, leaves = inputs
    statement = leaves[0].conclusion
    relation = statement.delta_iota5_relation
    altered = replace(relation, positive_value=replace(relation.positive_value, coefficient=3))
    changed = replace(leaves[0], conclusion=replace(statement, delta_iota5_relation=altered))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        assess_typed_clauses(crosswalk, (changed, leaves[1]))


def test_corrupted_prop51_eta_group_order_rejected(inputs):
    crosswalk, leaves = inputs
    statement = leaves[0].conclusion
    higher = statement.higher_eta_group_relation
    altered = replace(higher, rhs=replace(higher.rhs, order=4))
    changed = replace(leaves[0], conclusion=replace(statement, higher_eta_group_relation=altered))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        assess_typed_clauses(crosswalk, (changed, leaves[1]))


def test_corrupted_nu_prime_generator_rejected(inputs):
    crosswalk, leaves = inputs
    from expression import GeneratorSymbol
    rhs = leaves[1].conclusion.rhs
    altered = replace(rhs, generator=GeneratorSymbol(family="η", index=4))
    changed = replace(leaves[1], conclusion=replace(leaves[1].conclusion, rhs=altered))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        assess_typed_clauses(crosswalk, (leaves[0], changed))


def test_source_locator_tamper_rejected(inputs):
    crosswalk, leaves = inputs
    changed = deepcopy(crosswalk)
    changed["leaves"][0]["source_locator"] = "Proposition 5.2"
    with pytest.raises(ValueError, match="unverified source identity"):
        assess_typed_clauses(changed, leaves)
