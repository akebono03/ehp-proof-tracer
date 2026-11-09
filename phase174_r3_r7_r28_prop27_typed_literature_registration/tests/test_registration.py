"""R28 focused proof-eligibility and type-specific inference guards."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization, prop27_typed_specialization_rule,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, REFERENCE_ID, Prop27UniversalLiteratureStatement,
    verified_universal_statement, register_universal_prop27,
    prop27_literature_to_premise_rule, derive_registered_general_premise,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.audit import allowed_paths
from proof import ProofRule, ProofStep, find_inference_match, apply_inference_match
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[2]


def test_primary_source_general_theorem_checked():
    theorem = verified_universal_statement(ROOT)
    assert theorem.locator == "Proposition 2.7"
    assert theorem.minimum_n == 2
    assert theorem.even_n_only is True
    assert theorem.signed_hopf_delta is True


def test_isolated_typed_registration_and_single_general_given():
    bridge = register_universal_prop27(ROOT)
    record = bridge.registry.assertion(ASSERTION_ID)
    assert record.origin is AssertionOrigin.FIXED_STATEMENT
    assert record.reference_id == REFERENCE_ID
    assert isinstance(record.content, Prop27UniversalLiteratureStatement)
    assert len(bridge.proof_links) == 1
    parent = bridge.proof_links[0].step
    assert parent.rule is ProofRule.GIVEN
    assert parent.conclusion == record.content
    assert parent.premises == ()
    assert not isinstance(parent.conclusion, Prop27GeneralTheoremPremise)
    assert parent.conclusion != typed_specialization(6)


def test_real_registered_chain_generates_n6_only_by_inference():
    bridge = register_universal_prop27(ROOT)
    general = derive_registered_general_premise(bridge)
    assert general.rule is ProofRule.INFERENCE
    assert len(general.premises) == 1
    match = find_inference_match(prop27_typed_specialization_rule(6), (general,))
    assert match is not None
    result = apply_inference_match(match)
    assert result.conclusion == typed_specialization(6)
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (general,)
    assert result.inference_rule.literature_reference.locator == "Proposition 2.7"


def test_no_premise_cannot_create_schema():
    assert find_inference_match(prop27_literature_to_premise_rule(), ()) is None


def test_source_given_cannot_be_replaced_with_wrong_statement():
    parent = ProofStep(
        conclusion=replace(Prop27UniversalLiteratureStatement(), source_sha256="0" * 64),
        premises=(), rule=ProofRule.GIVEN,
    )
    assert find_inference_match(prop27_literature_to_premise_rule(), (parent,)) is None


def test_specific_n6_given_cannot_satisfy_universal_rule():
    parent = ProofStep(typed_specialization(6), (), ProofRule.GIVEN)
    assert find_inference_match(prop27_literature_to_premise_rule(), (parent,)) is None


def test_wrong_source_bytes_rejected(tmp_path):
    folder = tmp_path / "sources" / "toda"
    folder.mkdir(parents=True)
    (folder / "Toda_02_2.tex").write_text(
        "\\begin{proposition}\\label{prop:2.7}fake\\end{proposition}",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        verified_universal_statement(tmp_path)


def test_no_public_rules_or_root_claimed():
    bridge = register_universal_prop27(ROOT)
    assert len(bridge.records) == 1
    assert all("n=6" not in str(link.step.conclusion) for link in bridge.proof_links)


def test_source_guard_allowlist_is_narrow():
    assert allowed_paths(("phase174_r3_r7_r27_certified_premise_registry_audit/README.md",
                          "phase174_r3_r7_r28_prop27_typed_literature_registration/audit.py"))
    for path in ("proof.py", "sources/toda/Toda_02_2.tex", ".pytest_cache/v/cache/lastfailed"):
        with pytest.raises(RuntimeError, match="Unreviewed"):
            allowed_paths((path,))
