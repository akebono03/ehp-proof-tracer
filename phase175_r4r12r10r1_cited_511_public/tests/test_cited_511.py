"""Focused R4R12R10R1 contracts; no recursive whole-suite search."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r12r10r1_cited_511_public import installer, provider, source
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def test_canonical_citation_matches_typed_delta_orientation() -> None:
    from phase165_r14_r6_generic_iso import GeneratorImage
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality

    equality = source.canonical_511()
    delta = TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4))
    image = GeneratorImage(delta, equality.lhs.expression, equality.rhs)
    assert delta_image_equality(image) == equality


def test_cited_511_requires_exact_given() -> None:
    statement = source.canonical_511()
    citation = source.CitedToda511(statement)
    options = provider.expand_cited_511(statement, (citation,))
    assert len(options) == 1
    assert options[0].subgoals == (citation,)
    assert not provider.expand_cited_511(statement, ())
    assert not provider.expand_cited_511(statement, (citation, citation))
    assert not provider.expand_cited_511(source.CitedToda511(statement), (citation,))


def test_cited_511_inferred_relation_requires_given_parent() -> None:
    statement = source.canonical_511()
    citation = source.CitedToda511(statement)
    expansion = provider.expand_cited_511(statement, (citation,))[0]
    parent = ProofStep(citation, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(expansion.rule, (parent,))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == statement
    assert not find_inference_matches_for_rule(
        expansion.rule,
        (ProofStep(citation, (), ProofRule.INFERENCE,
                   inference_rule=expansion.rule),),
    )


def test_source_token_must_be_unique(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    chapter = tmp_path / "Toda_05_2.tex"
    chapter.write_text(source.LABEL + source.FORMULA + r"\end{equation}"
                       + r"\begin{proposition}\label{prop:5.8}"
                       + r"\begin{proposition}\label{prop:5.9}", encoding="utf-8")
    monkeypatch.setattr(source, "vetted_source", lambda path, pin: chapter.read_text(encoding="utf-8"))
    with pytest.raises(RuntimeError, match="SOURCE_ORDER_CHANGED"):
        source.verify_cited_511(tmp_path, tmp_path / "manifest.json")


def test_only_two_entire_functions_are_replaced() -> None:
    # BRIDGE_ANCHOR is indented eight spaces inside the actual if block.
    # A synthetic fixture must preserve that nesting before ast.parse().
    module = (
        "def build_shared_typed_bridge():\n"
        "    if True:\n"
        + installer.BRIDGE_ANCHOR
        + "    return None\n\n"
        + "def shared_expansion_provider():\n"
        + installer.PROVIDER_ANCHOR
        + "    return None\n"
    )
    ast.parse(module)
    after_provider, full_provider = installer.update_function(
        module, installer.PROVIDER_NAME,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_INSERT,
    )
    assert installer.PROVIDER_INSERT in full_provider
    assert after_provider.count(installer.PROVIDER_INSERT) == 1
    assert installer.BRIDGE_INSERT not in after_provider

    updated, full_bridge = installer.update_function(
        after_provider, installer.BRIDGE_NAME,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_INSERT,
    )
    assert installer.BRIDGE_INSERT in full_bridge
    assert updated.count(installer.BRIDGE_INSERT) == 1
    assert updated.count(installer.PROVIDER_INSERT) == 1
    ast.parse(updated)

    again, _ = installer.update_function(
        updated, installer.PROVIDER_NAME,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_INSERT,
    )
    again, _ = installer.update_function(
        again, installer.BRIDGE_NAME,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_INSERT,
    )
    assert again == updated


def test_readme_does_not_claim_group_completion() -> None:
    assert "pi_9^5" not in provider.RULE_NAME
    assert source.REFERENCE_ID == "toda:(5.11)"
