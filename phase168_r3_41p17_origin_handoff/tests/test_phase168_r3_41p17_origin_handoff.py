"""R3-41P17: factory origin observations, not an independent certificate."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary import UnverifiedProofTree
from phase168_r3_41p17_origin_handoff.origin_handoff import (
    build_origin_bound_narrative_model,
)
from proof import ProofRule
from proof_origin_capture import capture_search_origins
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


CASES = (
    ("pi3_2", 2, 1, 13, 5, 4),
    ("pi4_3", 3, 1, 19, 6, 4),
    ("pi5_4", 4, 1, 7, 3, 3),
)


def search_with_context(n: int, k: int):
    bridge = build_shared_typed_bridge()
    screened = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=screened.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(screened) >= 1
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    return result, screened[-1], citing_id


@pytest.mark.parametrize("name,n,k,inference,given,references", CASES)
def test_real_search_handoff_preserves_proof_and_reference(
    name, n, k, inference, given, references,
):
    with capture_search_origins() as observation:
        result, screened, citing_id = search_with_context(n, k)
        assert observation.factory_output_count >= inference
        assert observation.accepted_step_count >= inference + given
        with patch("phase165_r3_recursive_search.find_inference_matches_for_rule",
                   side_effect=AssertionError("search matcher replayed")), patch(
            "phase168_r3_41p13_trust_boundary.verification.find_inference_matches_for_rule",
            side_effect=AssertionError("boundary matcher replayed"),
        ):
            model = build_origin_bound_narrative_model(
                result, screened, citing_assertion_id=citing_id,
                observation=observation,
            )
        assert len(model.steps) == inference + given
        assert len(model.citations) == references
        assert tuple(model.steps) == result.proven_steps
        assert all(a is b for a, b in zip(model.steps, result.proven_steps))
        assert sum(s.rule is ProofRule.GIVEN for s in model.steps) == given
        rendered = render_model_backed_narrative_markdown(result, model)
        path = Path(__file__).resolve().parents[2] / (
            "phase168_r3_41p12_publication_boundary_audit/baselines/" + name + ".md"
        )
        assert rendered == path.read_text(encoding="utf-8")
        assert all(citation.statement_bodies for citation in model.citations)


def test_forged_inference_is_rejected_before_factory_origin_check():
    with capture_search_origins() as observation:
        result, screened, citing = search_with_context(2, 1)
        original = next(s for s in result.proven_steps if s.rule is ProofRule.INFERENCE)
        counterfeit = replace(original, note="forged after the search")
        corrupted = replace(result, proven_steps=result.proven_steps + (counterfeit,))
        with pytest.raises(UnverifiedProofTree, match="not accepted by this search"):
            build_origin_bound_narrative_model(
                corrupted, screened, citing_assertion_id=citing,
                observation=observation,
            )


def test_value_equal_given_copy_is_not_the_screened_source():
    with capture_search_origins() as observation:
        result, screened, citing = search_with_context(2, 1)
        original = next(s for s in result.proven_steps if s.rule is ProofRule.GIVEN)
        copied = replace(original)
        assert copied == original and copied is not original
        corrupted = replace(result, proven_steps=result.proven_steps + (copied,))
        with pytest.raises(UnverifiedProofTree, match="not accepted by this search"):
            build_origin_bound_narrative_model(
                corrupted, screened, citing_assertion_id=citing,
                observation=observation,
            )


def test_factory_candidate_without_proved_event_is_not_an_accepted_step():
    # A raw candidate can be constructed, but production search must explicitly
    # select it before it may cross the origin handoff.
    from proof import InferenceMatch, InferenceRule
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    rule = InferenceRule(name="synthetic-only", conclusion_builder=lambda premises: "not-a-proof")
    match = InferenceMatch(inference_rule=rule, premises=(), bindings=())
    with capture_search_origins() as observation:
        candidate = derive_inference_proof_step(match)
        assert observation.contains_factory_step(candidate)
        assert not observation.contains_accepted_step(candidate)


def test_observation_does_not_transfer_to_another_session():
    with capture_search_origins() as original_observation:
        result, screened, citing = search_with_context(2, 1)
    with capture_search_origins():
        with pytest.raises(ValueError, match="active search"):
            build_origin_bound_narrative_model(
                result, screened, citing_assertion_id=citing,
                observation=original_observation,
            )


def test_unpositioned_partial_is_not_promoted():
    partial = make_partial_proof_result(
        n=12, k=9, status=ProofSearchStatus.PARTIAL,
        open_goals=("unresolved",), diagnostics=("no derivation",),
    )
    with capture_search_origins() as observation:
        _, screened, citing = search_with_context(2, 1)
        with pytest.raises(UnverifiedProofTree, match="complete proofs"):
            build_origin_bound_narrative_model(
                partial, screened, citing_assertion_id=citing,
                observation=observation,
            )


def test_scope_is_observational_not_a_cryptographic_certificate():
    # This module must never authorize a direct ProofNarrativeModel or add
    # an is_verified field to an ordinary PartialProofResult.
    import dataclasses
    from phase165_r52_partial_proof import PartialProofResult
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
    assert "is_verified" not in {f.name for f in dataclasses.fields(PartialProofResult)}
    assert "is_verified" not in {f.name for f in dataclasses.fields(ProofNarrativeModel)}


def test_retry_install_after_restore_reuses_only_identical_backups(tmp_path, monkeypatch):
    """A focused failure must not make a restored package impossible to rerun."""
    from phase168_r3_41p17_origin_handoff import install, restore

    root = tmp_path
    output = root / "output"
    output.mkdir()
    factory = root / "phase164_r8_proofstep_factory.py"
    adapter = root / "phase165_r52_r2_search_adapter.py"
    capture = root / "proof_origin_capture.py"
    originals = {}
    for target, name in (
        (factory, "derive_inference_proof_step"),
        (adapter, "search_registered_partial_proof"),
    ):
        original = (
            install.PACKAGE / "full_functions" / (name + "_BEFORE.py")
        ).read_bytes()
        target.write_bytes(original)
        originals[target] = original

    for module in (install, restore):
        monkeypatch.setattr(module, "ROOT", root)
        monkeypatch.setattr(module, "OUTPUT", output)
    monkeypatch.setattr(install, "FACTORY", factory)
    monkeypatch.setattr(install, "ADAPTER", adapter)
    monkeypatch.setattr(install, "CAPTURE", capture)

    install.install()
    assert capture.exists()
    assert all(target.read_bytes() != data for target, data in originals.items())
    restore.main()
    assert not capture.exists()
    assert all(target.read_bytes() == data for target, data in originals.items())
    assert (output / "manifest.restored.json").exists()

    install.install()
    assert capture.exists()
    restore.main()
    assert not capture.exists()
    assert all(target.read_bytes() == data for target, data in originals.items())

    backup = output / (factory.name + ".before")
    backup.write_bytes(b"deliberately corrupt historical backup")
    with pytest.raises(RuntimeError, match="existing backup differs"):
        install.install()
    assert not (output / "manifest.json").exists()
    assert not capture.exists()
    assert all(target.read_bytes() == data for target, data in originals.items())
