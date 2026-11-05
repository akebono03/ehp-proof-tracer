"""Phase 174 R3-R6: source ancestry and generic backward specialization tests."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
    Toda48IndexTwoDoubleSuspensionStatement,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    build_cited_extension_sources,
    cited_toda55_double_inference_rule,
    expand_cited_toda55_double,
    verify_extension_texts,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _public_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    assert len(goals) == 1
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing is not None
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=goal)
    return goal, citing, screened, provider


def test_toda48_toda55_text_and_manifest_order() -> None:
    positions = dict(verify_extension_texts())
    assert positions == {"(4.8)": 7500, "(5.5)": 8600}


def test_toda48_injectivity_clause_preserves_printed_tex_spacing() -> None:
    """The adopted source has a space before the closing TeX brace."""
    source = Path(__file__).resolve().parents[2] / "sources/toda/Toda_04_2.tex"
    text = source.read_text(encoding="utf-8-sig")
    start = r"\begin{equation}\label{4.8}"
    assert text.count(start) == 1
    block = text.split(start, 1)[1].split(r"\end{equation}", 1)[0]
    assert r"E^{2}:\pit{2n-2}{\,n-1}\to\pit{2n}{\,n+1}" in block
    assert r"\ \text{は単射で, }" in block
    assert r"\pit{2n}{\,n+1}/E^{2}\pit{2n-2}{\,n-1}\cong\mathbb{Z}_2" in block
    assert dict(verify_extension_texts()) == {"(4.8)": 7500, "(5.5)": 8600}


def test_unverified_modified_toda_transcription_rejected(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    for ch in ("04", "05"):
        source = root / "sources" / "toda" / f"Toda_{ch}_2.tex"
        target = tmp_path / "sources" / "toda" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_bytes()
        if ch == "04":
            content = content.replace(b"\\Delta(\\iota_{2n-1})=0", b"\\Delta(\\iota_{2n-1})=1")
        target.write_bytes(content)
    with pytest.raises(ValueError, match="Unreviewed Toda source blob"):
        verify_extension_texts(tmp_path)


def test_source_bridge_registers_universal_only() -> None:
    bridge = build_cited_extension_sources()
    assert len(bridge.proof_links) == 2
    claims = {link.step.conclusion for link in bridge.proof_links}
    assert claims == {
        Toda48UniversalConditionalStatement(), Toda55UniversalDoubleStatement(),
    }
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)
    assert all(not isinstance(link.step.conclusion, Relation) for link in bridge.proof_links)
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry.reference(assertion.reference_id)
        assert ref.publication_position in (7500, 8600)
        assert assertion.content in claims


def test_cited_toda55_inference_rejects_given_family_member_and_wrong_formula() -> None:
    n = 5
    nu = HomotopyElement("ν₅", n, n + 3, n, GeneratorSymbol("ν", index=n))
    prior = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    goal = Relation(Multiple(2, nu), IteratedSuspension(prior, n - 3), RelationType.EQUALITY)
    sources = (Toda55UniversalDoubleStatement(),)
    assert not expand_cited_toda55_double(goal, sources)
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition,
        canonical_member,
    )
    definition = CitedStableFamilyDefinition(4, 4, 3)
    proposals = expand_cited_toda55_double(goal, sources + (definition,))
    assert len(proposals) == 1
    member, theorem = proposals[0].subgoals
    assert member == canonical_member(definition, n)
    assert theorem == Toda55UniversalDoubleStatement()
    rule = cited_toda55_double_inference_rule(goal)
    inferred = ProofStep(member, (), ProofRule.INFERENCE)
    cited = ProofStep(theorem, (), ProofRule.GIVEN)
    assert len(find_inference_matches_for_rule(rule, (inferred, cited))) == 1
    assert not find_inference_matches_for_rule(
        rule, (ProofStep(member, (), ProofRule.GIVEN), cited),
    )
    assert not find_inference_matches_for_rule(
        rule, (inferred, ProofStep(theorem, (), ProofRule.INFERENCE)),
    )
    assert not expand_cited_toda55_double(
        Relation(Multiple(2, nu), IteratedSuspension(prior, 3), RelationType.EQUALITY),
        sources + (definition,),
    )
    wrong = replace(nu, generator=GeneratorSymbol("μ", index=n))
    assert not expand_cited_toda55_double(
        Relation(Multiple(2, wrong), IteratedSuspension(prior, 2), RelationType.EQUALITY),
        sources + (definition,),
    )


def test_public_screen_exposes_two_source_only_leaves_before_target() -> None:
    goal, citing, screened, provider = _public_context()
    refs = {type(link.step.conclusion): link.step for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN}
    assert Toda48UniversalConditionalStatement in refs
    assert Toda55UniversalDoubleStatement in refs
    assert refs[Toda48UniversalConditionalStatement].conclusion == Toda48UniversalConditionalStatement()
    assert refs[Toda55UniversalDoubleStatement].conclusion == Toda55UniversalDoubleStatement()
    assert goal not in tuple(step.conclusion for step in refs.values())
    options = provider(CyclicStructureStatement(goal.lhs, goal.rhs.generator, 8))
    candidates = tuple(x for x in options if x.rule.name ==
                       "finite cyclic extension by an index-two injective image")
    assert len(candidates) == 1
    index, prior, doubled = candidates[0].subgoals
    assert isinstance(index, Toda48IndexTwoDoubleSuspensionStatement)
    assert prior.lhs == TodaPrimaryGroup(6, 3)
    double_proposals = tuple(p for p in provider(doubled) if p.rule.name ==
                             "specialize cited Toda (5.5) doubled nu-family identity")
    assert len(double_proposals) == 1
    index_step = reconstruct_registered_goal(
        index, screened, citing, provider, lookup_mode="typed_reference",
    )
    double_step = reconstruct_registered_goal(
        doubled, screened, citing, provider, lookup_mode="typed_reference",
    )
    assert index_step.rule is ProofRule.INFERENCE
    assert double_step.rule is ProofRule.INFERENCE
    assert any(s.rule is ProofRule.GIVEN and
               s.conclusion == Toda55UniversalDoubleStatement()
               for s in double_step.premises)
