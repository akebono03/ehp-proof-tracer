"""Verify genuine π5^5 (5.1) ancestry in the complete public π5^3 proof."""
from __future__ import annotations

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, Relation
from toda_rules import TodaDeltaInjectiveStatement


def main() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    if result.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError("R3U pi5^3 proof not complete")
    model = build_linked_proof_narrative_model(result, contexts[0])
    goal = TodaDeltaInjectiveStatement(TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)))
    delta = [step for step in model.steps if step.conclusion == goal]
    if len(delta) != 1 or len(delta[0].premises) != 2:
        raise AssertionError("Delta injectivity lacks its two certified premises")
    group = delta[0].premises[1]
    if (group.rule is not ProofRule.INFERENCE or not isinstance(group.conclusion, Relation)
            or group.conclusion.lhs != goal.map.source_group
            or len(group.premises) != 1
            or group.premises[0].rule is not ProofRule.GIVEN
            or group.premises[0].inference_rule.literature_reference.locator != "(5.1)"):
        raise AssertionError("Diagonally derived (5.1) group statement missing")
    markdown = render_model_backed_narrative_markdown(result, model)
    reference = tuple((c.reference.locator or c.reference.label) for c in model.citations)
    if "(5.1)" not in reference or "Proposition 5.1" not in reference:
        raise AssertionError("Cited (5.1) or Proposition 5.1 reference lost")
    if r"\pi_{5}^{5}" not in markdown or r"\iota_{5}" not in markdown:
        raise AssertionError("Derived diagonal group not visible")
    print("R3U_PI53_STATUS=complete")
    print("R3U_PI53_STEPS=" + str(len(model.steps)))
    print("R3U_DELTA_PREMISE_TYPES=" + repr([type(p.conclusion).__name__ for p in delta[0].premises]))
    print("R3U_DIAGONAL_INFERENCE=True")
    print("R3U_DIAGONAL_SOURCE=(5.1)")
    print("R3U_REFERENCES=" + repr(reference))
    print("R3U_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
