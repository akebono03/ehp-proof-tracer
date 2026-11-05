"""Source-screened source-body and public Narrative regression checks."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase168_r3_37c_reference_projection import (
    project_cited_proof_step_reference_bodies,
    project_reference_bodies,
)
from phase174_r3_r6_source_extension.source import build_cited_extension_sources
from proof import InferenceRule, LiteratureReference, ProofRule


def test_cited_given_fallback_matches_registered_reference_body_for_both_sources() -> None:
    bridge = build_cited_extension_sources()
    for locator in ("(4.8)", "(5.5)"):
        assertion_id = "toda:174:r3r6:universal:" + locator
        links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
        assert len(links) == 1 and links[0].step is not None
        reference = LiteratureReference(label="Toda " + locator, locator=locator)
        expected = project_reference_bodies(bridge.registry, (assertion_id,))
        actual = project_cited_proof_step_reference_bodies(reference, (links[0].step,))
        assert actual == expected
        assert len(actual) == 1


def test_cited_given_fallback_rejects_unproved_or_wrongly_cited_statement() -> None:
    bridge = build_cited_extension_sources()
    source = next(link.step for link in bridge.proof_links
                  if link.step is not None and link.assertion_id.endswith("(4.8)"))
    reference = LiteratureReference(label="Toda (4.8)", locator="(4.8)")
    assert project_cited_proof_step_reference_bodies(reference, ()) == ()
    assert project_cited_proof_step_reference_bodies(
        LiteratureReference(label="Toda (5.5)", locator="(5.5)"), (source,),
    ) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, rule=ProofRule.INFERENCE),),
    ) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, inference_rule=None),),
    ) == ()
    assert project_cited_proof_step_reference_bodies(reference, (source, source)) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, inference_rule=InferenceRule(
            name="unrelated", literature_reference=reference,
        )),),
    ) == ()


def test_source_guard_failure_does_not_show_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r6_source_extension.source as source_module
    bridge = build_cited_extension_sources()
    step = next(link.step for link in bridge.proof_links
                if link.step is not None and link.assertion_id.endswith("(5.5)"))
    reference = LiteratureReference(label="Toda (5.5)", locator="(5.5)")

    def unverified() -> None:
        raise ValueError("unverified adopted source")

    monkeypatch.setattr(source_module, "verify_extension_texts", unverified)
    assert project_cited_proof_step_reference_bodies(reference, (step,)) == ()


def test_public_pi85_reference_bodies_and_complete_root_unchanged() -> None:
    from phase174_r3_r6_r2_prop44_lemma54.audit import inspect

    result = inspect()
    narrative = result["narrative"]
    assert result["root_status"] == "complete"
    assert result["root_proven_steps"] == 16
    assert result["new_group_given"] == 0
    assert narrative.count("[R4] (4.8).") == 1
    assert narrative.count("[R7] (5.5).") == 1
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in narrative
    assert r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$." in narrative
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in narrative
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in narrative
    conclusion_lines = [line for line in narrative.splitlines()
                        if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line]
    assert len(conclusion_lines) == 1
