"""R13 cited source registration, screening and inference provenance tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    canonical_annihilator_instance, cited_annihilator_specialization_rule,
    expand_cited_annihilator_specialization,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, TODA_CLAUSE,
)
from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
    ASSERTION_ID, REF_ID, build_isolated_toda59_annihilator_bridge,
    join_isolated_source_bridge, reviewed_toda59_source_position,
)
from proof import ProofRule, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def manifest_fixture(tmp_path: Path, *, position: int = 9300, clause: str = TODA_CLAUSE) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "publication_order_scope": "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION",
        "assertions": [{
            "reference_id": "toda:(5.9)",
            "source_file": "Toda_05_2.tex",
            "chapter": 5,
            "review_needed": False,
            "publication_position": position,
            "source_text": "\\begin{equation} " + clause + " \\end{equation}",
        }],
    }), encoding="utf-8")
    return path


def test_manifest_source_order_is_grounded_not_an_original_edition_rank(tmp_path: Path) -> None:
    assert reviewed_toda59_source_position(manifest_fixture(tmp_path)) == 9300


@pytest.mark.parametrize("change", ("wrong_clause", "no_position", "unreviewed", "duplicate", "wrong_scope"))
def test_manifest_without_exact_reviewed_unique_clause_fails_closed(
    tmp_path: Path, change: str,
) -> None:
    path = manifest_fixture(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if change == "wrong_clause":
        data["assertions"][0]["source_text"] = "different theorem"
    elif change == "no_position":
        data["assertions"][0]["publication_position"] = None
    elif change == "unreviewed":
        data["assertions"][0]["review_needed"] = True
    elif change == "duplicate":
        data["assertions"].append(dict(data["assertions"][0]))
    elif change == "wrong_scope":
        data["publication_order_scope"] = "PRINTED_ORIGINAL_EDITION"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RuntimeError):
        reviewed_toda59_source_position(path)


def test_isolated_source_bridge_has_only_one_general_cited_given() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    assert isinstance(bridge, RegistryBridgeResult)
    assert len(bridge.proof_links) == 1
    link = bridge.proof_links[0]
    assert link.assertion_id == ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert isinstance(link.step.conclusion, CitedFamilyAnnihilator)
    entry = bridge.registry.assertion(ASSERTION_ID)
    reference = bridge.registry.reference(REF_ID)
    assert entry.content == link.step.conclusion
    assert entry.origin is AssertionOrigin.FIXED_STATEMENT
    assert reference.publication_position == reviewed_toda59_source_position()
    assert reference.locator == "(5.9)"
    assert link.step.inference_rule.literature_reference.locator == "(5.9)"


def test_source_screening_retains_cited_general_schema_but_not_instance_as_given() -> None:
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(
        build_isolated_toda59_annihilator_bridge(), goal=target,
    )
    assert len(screened.proof_links) == 1
    cited = screened.proof_links[0].step
    goal = canonical_annihilator_instance(cited.conclusion, 6)
    assert goal is not None
    assert goal != target
    assert goal != cited.conclusion
    assert all(link.step.conclusion != goal for link in screened.proof_links)
    expansions = expand_cited_annihilator_specialization(goal, (cited.conclusion,))
    assert len(expansions) == 1
    assert expansions[0].subgoals == (cited.conclusion,)


def test_proved_source_ancestor_creates_real_n6_inference_not_given() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    cited = bridge.proof_links[0].step
    goal = canonical_annihilator_instance(cited.conclusion, 6)
    assert goal is not None
    inference = cited_annihilator_specialization_rule(goal, cited.conclusion)
    matches = find_inference_matches_for_rule(inference, (cited,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (cited,)
    assert step.inference_rule is inference
    assert step.conclusion != TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))


def test_missing_cited_given_cannot_close_instance() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    given = bridge.proof_links[0].step
    goal = canonical_annihilator_instance(given.conclusion, 6)
    rule = cited_annihilator_specialization_rule(goal, given.conclusion)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert expand_cited_annihilator_specialization(goal, ()) == ()


def test_join_builds_fresh_registry_leaves_input_unchanged() -> None:
    existing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    cited = build_isolated_toda59_annihilator_bridge()
    joined = join_isolated_source_bridge(existing, cited)
    assert joined.registry is not existing.registry
    assert len(existing.registry._references) == 0
    assert len(existing.registry._assertions) == 0
    assert len(joined.proof_links) == 1
    assert joined.registry.assertion(ASSERTION_ID).content == cited.proof_links[0].step.conclusion


def test_join_rejects_duplicate_cited_source_registration() -> None:
    source = build_isolated_toda59_annihilator_bridge()
    with pytest.raises(ValueError, match="duplicate"):
        join_isolated_source_bridge(source, source)


def test_join_rejects_invalid_or_missing_source_links() -> None:
    existing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError):
        join_isolated_source_bridge(existing, existing)
    with pytest.raises(TypeError):
        join_isolated_source_bridge(object(), existing)
