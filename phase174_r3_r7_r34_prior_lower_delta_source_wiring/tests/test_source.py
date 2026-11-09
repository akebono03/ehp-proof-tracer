"""R34 source, manifestation, typed generator and forbidden-goal guards."""
from __future__ import annotations

import pytest

from expression import Composition
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase174_r3_r7_r34_prior_lower_delta_source_wiring import source
from proof import ProofRule, Relation
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


def test_real_prior_toda_source_is_pinned_and_ordered():
    text = source.pinned_source_text()
    assert text.index(source.PROP58) < text.index(source.EQ510) < text.index(source.PROP59)
    assert text.count(source.CODOMAIN_CLAUSE) >= 1
    assert text.count(source.IMAGE_CLAUSE) >= 1


def test_manifest_positions_are_exact_and_in_order():
    p58, eq510 = source.reviewed_source_positions()
    assert type(p58) is int and type(eq510) is int
    assert 0 < p58 < eq510


def test_structured_db_generator_is_actual_composition():
    codomain, image = source.checked_prior_statements()
    assert type(codomain) is Relation
    assert codomain.lhs == TodaPrimaryGroup(9, 5)
    assert type(codomain.rhs) is FiniteCyclicGroup
    assert codomain.rhs.order == 2
    assert type(codomain.rhs.generator) is Composition
    assert codomain.rhs.generator.is_type_compatible()
    assert type(image) is TodaDeltaImageUpToSignStatement
    assert image.map == TodaDeltaMap(TodaPrimaryGroup(11, 11), codomain.lhs)
    assert image.positive_value == codomain.rhs.generator
    assert image.element.source == 11 and image.element.target == 11


def test_only_two_earlier_cited_givens_no_kernel_or_root():
    bridge = source.build_cited_lower_delta_sources()
    assert len(bridge.proof_links) == 2
    for link, (_, ref_id, source_id, _) in zip(bridge.proof_links, source.MANIFEST_ROWS):
        step = link.step
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        assert reference.reference_id == ref_id
        assert reference.source_id == source_id
        assert step.rule is ProofRule.GIVEN
        assert not step.premises
        assert step.inference_rule.literature_reference.locator in ("Proposition 5.8", "(5.10)")
        assert bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    assert all("KernelMultiple" not in type(link.step.conclusion).__name__
               and "ZeroStatement" not in type(link.step.conclusion).__name__
               for link in bridge.proof_links)


def test_missing_printed_clauses_rejected(tmp_path):
    path = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    path.parent.mkdir(parents=True)
    real = source.pinned_source_text()
    path.write_text(real.replace(source.IMAGE_CLAUSE, "NOT_AN_EQUATION"), encoding="utf-8")
    with pytest.raises(ValueError):
        source.pinned_source_text(tmp_path)


def test_manifest_rejection_of_swapped_source_id(monkeypatch):
    current = source._load_manifest_reference_order
    def wrong(path):
        positions, rows, manifest = current(path)
        altered = dict(rows)
        key = "toda:(5.10)"
        altered[key] = (dict(rows[key][0], statement_id="forged:id"),)
        return positions, altered, manifest
    monkeypatch.setattr(source, "_load_manifest_reference_order", wrong)
    with pytest.raises(ValueError):
        source.reviewed_source_positions()


def test_cited_source_steps_do_not_prove_the_derived_kernel():
    bridge = source.build_cited_lower_delta_sources()
    assert all(type(link.step.conclusion).__name__ != "KernelMultipleStatement"
               for link in bridge.proof_links)
    assert all(link.step.rule is not ProofRule.INFERENCE
               for link in bridge.proof_links)
