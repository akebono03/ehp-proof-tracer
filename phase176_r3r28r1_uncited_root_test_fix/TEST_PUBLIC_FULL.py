"""Phase 176 R3R28 focused contracts for source-first public wiring."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase176_r3r28_toda55_quadruple_public import install
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    canonical_quadruple_goal,
)
from proof import ProofRule


def test_patch_both_functions_and_idempotent() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig")
    result = install.proposed(current.replace("\r\n", "\n"))
    functions = install.functions_in(result)
    assert "build_cited_toda55_quadruple_source" in functions["build_shared_typed_bridge"]
    assert "expand_public_toda55_quadruple" in functions["shared_expansion_provider"]
    assert install.proposed(result) == result


def test_partial_patch_fails_closed() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    without = current.replace(install.PROVIDER_PATCH, "")
    if install.SOURCE_PATCH in without:
        with pytest.raises(RuntimeError, match="PARTIAL_PATCH_DETECTED"):
            install.proposed(without)


def test_full_source_contains_complete_functions() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    text = install.full_code_md(install.proposed(current))
    assert "def build_shared_typed_bridge" in text
    assert "def shared_expansion_provider" in text


def test_default_shared_bridge_has_one_screened_quadruple_source() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    statements = tuple(link.step.conclusion for link in screened.proof_links
                       if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert statements.count(Toda55UniversalQuadrupleStatement()) == 1
    assert roots[0] not in statements


def test_shared_provider_proposes_and_proves_nu5_quadruple() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    root = roots[0]
    # An unpositioned DB group goal has no invented source citation.
    assert resolve_specialized_goal_citing_id(bridge, root) is None
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    goal = canonical_quadruple_goal(5)
    assert goal is not None
    choices = tuple(item for item in provider(goal)
                    if item.rule.name == "specialize cited Toda (5.5) quadruple nu-family identity")
    assert len(choices) == 1
    assert len(choices[0].subgoals) == 3

    # The reconstruction API requires an existing assertion ID as a context
    # anchor.  Use the uniquely screened (5.5) source, NOT an invented
    # citation for the unrelated, still-unproved pi_8^3 group goal.
    source_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == Toda55UniversalQuadrupleStatement()
    )
    assert len(source_links) == 1
    context_id = source_links[0].assertion_id
    assert bridge.registry.assertion(context_id).content == Toda55UniversalQuadrupleStatement()
    result = reconstruct_registered_goal(
        goal, screened, context_id, provider, lookup_mode="typed_reference",
    )
    assert result is not None and result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert len(result.premises) == 3
    assert not any(step.conclusion == root for step in result.premises)
