"""Focused typed-reference projection tests, including negative guards."""
from __future__ import annotations

from dataclasses import replace

from phase168_r3_37c_reference_projection import _verified_source_sentence
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase175_r4r10_cited_58_prop25_public.source import CitedToda58SignedDelta, canonical_toda58


def test_verified_cited_511_reference_body() -> None:
    actual = _verified_source_sentence(CitedToda511(canonical_511()))
    assert actual == r"$\Delta(\eta_9)=E\nu'\eta_7$."


def test_verified_cited_58_reference_body_keeps_sign() -> None:
    actual = _verified_source_sentence(CitedToda58SignedDelta(canonical_toda58()))
    assert actual == r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$."


def test_wrong_typed_reference_never_projects() -> None:
    assert _verified_source_sentence(replace(CitedToda511(canonical_511()), locator="(5.8)")) is None
    assert _verified_source_sentence(replace(CitedToda58SignedDelta(canonical_toda58()), locator="(5.11)")) is None


def test_web_complete_references_are_populated() -> None:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_partial_proof import ProofSearchStatus

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=5, k=4, bridge=bridge, context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, contexts[-1])
    refs = {c.reference.locator: c for c in model.citations if c.reference.locator in ("(5.11)", "(5.8)")}
    assert set(refs) == {"(5.11)", "(5.8)"}
    assert refs["(5.11)"].statement_bodies == (r"$\Delta(\eta_9)=E\nu'\eta_7$.",)
    assert refs["(5.8)"].statement_bodies == (r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$.",)
