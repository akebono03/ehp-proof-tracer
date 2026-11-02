"""Live public selector and Web-adapter audit for the typed pi_7^4 proof."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource, canonical_hopf_relation,
)
from proof import ProofRule, ProofStep
from web_group_proof import build_standard_web_group_proof_view


def ancestry(step: ProofStep) -> tuple[ProofStep, ...]:
    seen: set[int] = set()
    output: list[ProofStep] = []

    def visit(current: ProofStep) -> None:
        if id(current) in seen:
            return
        seen.add(id(current))
        output.append(current)
        for item in current.premises:
            visit(item)

    visit(step)
    return tuple(output)


def main() -> int:
    result = search_group_from_registered_goal(n=4, k=3)
    complete = result.status is ProofSearchStatus.COMPLETE
    roots = tuple(
        step for step in result.proven_steps
        if step.rule is ProofRule.INFERENCE and step.inference_rule is not None
        and step.inference_rule.name == "Toda (5.6) pi_7^4 source-bound direct-sum presentation"
        and step.conclusion == result.conclusion
    )
    checked = ancestry(roots[0]) if len(roots) == 1 else ()
    hopf = canonical_hopf_relation()
    certified = bool(
        complete and len(roots) == 1 and len(roots[0].premises) == 4
        and roots[0].premises[2].rule is ProofRule.INFERENCE
        and roots[0].premises[3].rule is ProofRule.INFERENCE
        and any(step.rule is ProofRule.GIVEN
                and type(step.conclusion) is TodaLemma54TypedSource
                for step in checked)
        and any(step.rule is ProofRule.INFERENCE and step.conclusion == hopf
                for step in checked)
    )
    view = build_standard_web_group_proof_view(
        n=4, k=3, max_depth=2, mode="narrative", citation_source="model",
    )
    web_complete = bool(
        view.key == "generic-complete-proof" and not view.partial_result
        and view.steps and view.rendered_lines
    )
    print("PHASE173_R4_R1_PUBLIC_STATUS=" + result.status.value)
    print("PHASE173_R4_R1_PUBLIC_COMPLETE=" + str(complete))
    print("PHASE173_R4_R1_PUBLIC_SOURCE_CERTIFIED=" + str(certified))
    print("PHASE173_R4_R1_PUBLIC_WEB_COMPLETE=" + str(web_complete))
    print("PHASE173_R4_R1_PUBLIC_WEB_KEY=" + str(view.key))
    print("PHASE173_R4_R1_PUBLIC_OPEN_GOALS=" + str(len(result.open_goals)))
    print("PHASE173_R4_R1_PUBLIC_PROVEN_STEPS=" + str(len(result.proven_steps)))
    print("PHASE173_R4_R1_PUBLIC_WEB_LINES=" + str(len(view.rendered_lines)))
    print("PHASE173_R4_R1_PUBLIC_DIAGNOSTICS=" + repr(result.diagnostics))
    if not (complete and certified and web_complete and not result.open_goals):
        raise RuntimeError("R4-R1 public complete proof is not yet certified")
    print("PHASE173_R4_R1_PUBLIC_VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
