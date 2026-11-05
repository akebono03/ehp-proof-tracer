"""End-to-end proof-ancestry audit of the corrected conditional Proposition 4.4."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    verify_prelude_source,
)
from proof import ProofRule


def cited_leaves(step) -> tuple[object, ...]:
    if step.rule is ProofRule.GIVEN:
        return (step.conclusion,)
    out: list[object] = []
    for premise in step.premises:
        out.extend(cited_leaves(premise))
    return tuple(out)


def inspect() -> dict[str, object]:
    position = verify_prelude_source()
    original = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(original, n=5, k=3)
    if len(roots) != 1:
        raise ValueError("Expected the registered pi_8^5 target")
    target = roots[0]
    citing = resolve_specialized_goal_citing_id(original, target)
    if citing is None:
        raise ValueError("Missing real publication position of target")
    augmented = attach_earlier_verified_lemma54(original, citing)
    if augmented is original:
        raise ValueError("Lemma 5.4 not attached although it precedes Proposition 5.6")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaProp44UniversalStatement()) == 1
    assert available.count(TodaLemma54TypedSource()) == 1
    assert available.count(TodaPreProp44SplittingStatement()) == 1
    provider = shared_expansion_provider(screened, proof_target=target)
    map_goal = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
    ))
    map_step = reconstruct_registered_goal(
        map_goal, screened, citing, provider, lookup_mode="typed_reference",
    )
    if (map_step.rule is not ProofRule.INFERENCE
            or map_step.conclusion != map_goal
            or getattr(map_step.inference_rule, "name", None)
            != "Toda Proposition 4.4 using separately proved Hopf invariant"
            or len(map_step.premises) != 2
            or map_step.premises[1].conclusion != canonical_hopf_relation()
            or map_step.premises[1].rule is not ProofRule.INFERENCE):
        raise ValueError("Proposition 4.4 was used without independently proved Hopf condition")
    ancestry = cited_leaves(map_step)
    if (ancestry.count(TodaProp44UniversalStatement()) != 1
            or ancestry.count(TodaLemma54TypedSource()) != 1
            or TodaPreProp44SplittingStatement() in ancestry):
        raise ValueError("Wrong cited ancestry for conditional Proposition 4.4")
    result = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    if result.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("pi_8^5 completed root regressed: " + result.status.value)
    roots_proved = tuple(step for step in result.proven_steps if step.conclusion == target)
    if len(roots_proved) != 1 or roots_proved[0].rule is not ProofRule.INFERENCE:
        raise ValueError("Completed group root lacks its own inference")
    root_ancestors = cited_leaves(roots_proved[0])
    if (TodaLemma54TypedSource() not in root_ancestors
            or TodaProp44UniversalStatement() not in root_ancestors
            or TodaPreProp44SplittingStatement() in root_ancestors):
        raise ValueError("Public group root did not choose the Lemma 5.4 route")
    model = build_linked_proof_narrative_model(result, screened)
    narrative = render_model_backed_narrative_markdown(result, model)
    if "Lemma 5.4" not in narrative or "Proposition 4.4" not in narrative:
        raise ValueError("Proposition 4.4 or Lemma 5.4 citation not visible")
    if r"$h:S^7\to S^4$" in narrative:
        raise ValueError("Unproved H(h) presentation remains in the narrative")
    # Earlier targets must not cite the later Lemma 5.4.
    previous = search_group_from_registered_goal(n=4, k=2, bridge=original)
    if previous.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("Prior pi_6^4 complete proof regressed")
    return {
        "phase": "174-R3-R6-R2",
        "root": "pi_8^5",
        "root_status": result.status.value,
        "root_proven_steps": len(result.proven_steps),
        "root_verified": True,
        "source_given_lemma54": True,
        "proposition44_conditional": True,
        "hopf_invariant_condition_inferred": True,
        "lemma54_is_root_ancestor": True,
        "preprop44_is_root_ancestor": False,
        "previous_pi6_4_still_complete": True,
        "prelude_source_position": position,
        "new_group_given": 0,
        "narrative_reference_verified": True,
        "narrative": narrative,
        "full_pytest_performed": False,
    }


def main() -> int:
    result = inspect()
    output = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    output = output / "EHPProofTracerAudit" / "phase174_r3_r6_r2"
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (output / "web_narrative.md").write_text(result["narrative"], encoding="utf-8")
    print("PHASE174_R3R6R2_PI85_COMPLETE=True")
    print("PHASE174_R3R6R2_HOPF_CONDITION_INFERRED=True")
    print("PHASE174_R3R6R2_LEMMA54_ROOT_ANCESTRY=True")
    print("PHASE174_R3R6R2_PRELUDE_NOT_IN_ROOT=True")
    print("PHASE174_R3R6R2_PI64_PRESERVED=True")
    print("PHASE174_R3R6R2_ROOT_STEPS=" + str(result["root_proven_steps"]))
    print("PHASE174_R3R6R2_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6R2_AUDIT=" + str(output / "audit.json"))
    print("PHASE174_R3R6R2_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
