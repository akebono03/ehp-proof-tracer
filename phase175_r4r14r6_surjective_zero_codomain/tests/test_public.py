"""Real shared provider proposal, not a claimed completed group proof."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r14r6_surjective_zero_codomain.rule import (
    RULE_NAME, surjective_zero_codomain_inputs,
)


def test_live_root_has_exactly_one_generic_zero_codomain_option() -> None:
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=goal)
    options = tuple(shared_expansion_provider(bridge, proof_target=goal)(goal))
    matches = tuple(option for option in options if option.rule.name == RULE_NAME)
    assert len(matches) == 1
    assert matches[0].subgoals == surjective_zero_codomain_inputs(goal)
