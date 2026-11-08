from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationRecord, MigrationStatus
from phase174_r3_r7_r26_prop27_source_premise_connection.bridge import Prop27SourceEvidence
from phase174_r3_r7_r27_certified_premise_registry_audit.audit import (
    ALLOWED_CACHE,
    classify_paths,
    inspect_registry,
    matches_checkout,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    Prop27TypedHopfDeltaStatement,
    typed_specialization,
)
from proof import InferenceRule, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def source():
    return Prop27SourceEvidence(
        source_path="sources/toda/Toda_02_2.tex",
        locator="Proposition 2.7",
        theorem_sha256="a" * 64,
        only_even_n=True,
        sign_undetermined=True,
    )


def bridge_with_step(step=None, *, include_assertion=True):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "toda:Proposition 2.7", ReferenceKind.PROPOSITION,
        "Proposition 2.7", source_id="Toda",
    ))
    links = ()
    records = ()
    if include_assertion:
        registry.add_assertion(AssertionEntry(
            "prop27:metadata", "toda:Proposition 2.7",
            AssertionKind.STATEMENT, "source metadata only",
        ))
        records = (MigrationRecord(
            "test", "prop27", "prop27:metadata",
            MigrationStatus.METADATA_ONLY, "No certified step",
        ),)
        if step is not None:
            links = (ProofStepLink("prop27:metadata", step=step),)
    return RegistryBridgeResult(registry, records, links)


def test_r27_metadata_is_not_certified_step():
    result = inspect_registry(bridge_with_step(), source())
    assert result["matching_literature_references"] == 1
    assert result["matching_assertions"] == 1
    assert result["linked_steps"] == 0
    assert result["eligible_certified_source_step"] is False
    assert result["certification_from_metadata"] is False


def test_r27_empty_registry_does_not_fabricate_proof():
    registry = UnifiedStatementRegistry()
    result = inspect_registry(RegistryBridgeResult(registry, (), ()), source())
    assert result["matching_assertions"] == 0
    assert result["eligible_certified_source_step"] is False


def test_r27_rejects_lookalike_source_step_even_with_inference_rule():
    step = ProofStep(
        conclusion=source(), premises=(ProofStep("parent", (), ProofRule.GIVEN),),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule("uncertified source inference"),
    )
    with pytest.raises(RuntimeError, match="certification review"):
        inspect_registry(bridge_with_step(step), source())


def test_r27_rejects_direct_given_of_general_schema():
    step = ProofStep(Prop27GeneralTheoremPremise(), (), ProofRule.GIVEN)
    with pytest.raises(RuntimeError, match="Direct Prop27"):
        inspect_registry(bridge_with_step(step), source())


def test_r27_rejects_direct_given_of_specific_theorem():
    step = ProofStep(typed_specialization(6), (), ProofRule.GIVEN)
    with pytest.raises(RuntimeError, match="Direct Prop27"):
        inspect_registry(bridge_with_step(step), source())


def test_r27_rejects_direct_given_of_source_evidence():
    step = ProofStep(replace(source(), theorem_sha256="b" * 64), (), ProofRule.GIVEN)
    with pytest.raises(RuntimeError, match="Direct Prop27"):
        inspect_registry(bridge_with_step(step), source())


def test_r27_retains_source_first_typing():
    stmt = typed_specialization(6)
    assert isinstance(stmt, Prop27TypedHopfDeltaStatement)
    assert stmt.source_iota_dimension == 13
    assert stmt.target_iota_dimension == 11
    assert stmt.sign_undetermined is True


def test_r27_allows_only_reviewed_phase_directories_and_existing_cache():
    assert classify_paths((
        "phase174_r3_r7_r26_prop27_source_premise_connection/README.md",
        "phase174_r3_r7_r27_certified_premise_registry_audit/audit.py",
        ALLOWED_CACHE,
    ))


@pytest.mark.parametrize("path", (
    "proof.py",
    "sources/toda/Toda_02_2.tex",
    ".pytest_cache/v/cache/lastfailed",
    "phase174_r3_r7_r28_future/rule.py",
))
def test_r27_rejects_unreviewed_changes(path):
    with pytest.raises(RuntimeError, match="Unreviewed paths"):
        classify_paths((path,))


def test_r27_matches_windows_and_unix_line_endings():
    assert matches_checkout(b"one\r\ntwo\r\n", b"one\ntwo\n")
    assert matches_checkout(b"one\ntwo\n", b"one\r\ntwo\r\n")
    assert not matches_checkout(b"unreviewed", b"reviewed")


def test_r27_run_script_preserves_focused_importlib_mode():
    from pathlib import Path
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "--import-mode=importlib" in script
    assert "-p no:cacheprovider" in script
    assert "phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py" in script
