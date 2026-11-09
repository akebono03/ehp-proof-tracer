"""R32 source-first audit and non-completion contract."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r32_lower_delta_kernel_audit.audit import (
    EQ510, EQ510_IMAGE, PINS, PROP58, PROP58_CODOMAIN, PROP59,
    R31_AUDIT, R31_SHA256, ROOT, SOURCE, git_blob_sha,
    inspect_toda_citations, inspect_typed_contract, matches_pin, report,
    verify_checkout,
)


def test_local_source_guard_respects_r30_and_r31():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r30_preserved"] is True
    assert state["r31_preserved"] is True
    assert state["tracked_changes"] == 0
    assert (ROOT / R31_AUDIT).exists()
    assert len(R31_SHA256) == 64


def test_source_pins_allow_whole_file_crlf_but_no_mutations():
    for file, sha in PINS.items():
        assert matches_pin((ROOT / file).read_bytes(), sha)
    original = b"a\nb\n"
    assert matches_pin(original.replace(b"\n", b"\r\n"), git_blob_sha(original))
    assert not matches_pin(b"different", git_blob_sha(original))


def test_toda_prior_statements_precede_proposition_59():
    source = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    info = inspect_toda_citations(source)
    assert info["prop58_codomain_precedes_prop59"] is True
    assert info["equation_510_precedes_prop59"] is True
    assert info["prop59_kernel_is_derived_not_given"] is True
    assert info["printed_claim_is_verified_proof_step"] is False
    assert source.index(PROP58) < source.index(EQ510) < source.index(PROP59)


def test_source_mutations_are_not_misread_as_proof():
    source = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    for marker in (PROP58_CODOMAIN, EQ510_IMAGE):
        altered = source.replace(marker, "NOT_CERTIFIED_SOURCE", 1)
        with pytest.raises(ValueError):
            inspect_toda_citations(altered)


def test_general_kernel_is_conditional_and_db_prior_not_literature():
    info = inspect_typed_contract()
    assert info["conditional_premise_types"] == [
        "Relation", "Relation", "TodaDeltaImageUpToSignStatement",
    ]
    assert info["hypothetical_premises_not_certified"] is True
    assert info["db_prior_is_independent_literature_reference"] is False
    assert info["general_rule_registered"] is False
    assert info["kernel_direct_given_inserted"] is False


def test_public_source_screen_cannot_insert_kernel_or_root_given():
    result = report(dry_run=False)
    assert result["screened"]["screened_direct_kernel_given"] == 0
    assert result["screened"]["screened_direct_root_given"] == 0
    assert result["new_givens"] == 0
    assert result["new_rules"] == 0
    assert result["production_files_changed"] == 0
    assert result["lower_delta_kernel_proved"] is False
    assert result["delta_surjectivity_proved"] is False
    assert result["root_complete"] is False
    assert result["full_pytest"] is False
    assert result["gate"].endswith("TYPED_PROOF_PENDING")


def test_r32_dry_run_keeps_proof_unfinished():
    r = report(dry_run=True)
    assert r["typed"] is None
    assert r["screened"] is None
    assert r["lower_delta_kernel_proved"] is False
    assert r["root_complete"] is False
    assert r["gate"] == "PASS_R32_SOURCE_PREFLIGHT_ONLY"
