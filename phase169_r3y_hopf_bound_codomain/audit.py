"""R3Y actual proof-tree and reference audit; no unstated mathematical facts."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from proof import ProofRule
from toda_rules import TodaHopfInvariantSurjectiveStatement


def examine():
    bridge = build_shared_typed_bridge()
    contexts = []
    proof = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if proof.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError("pi5^3 no longer complete")
    model = build_linked_proof_narrative_model(proof, contexts[0])
    goal = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    matched = tuple(x for x in model.steps if x.conclusion == goal)
    if len(matched) != 1:
        raise AssertionError("expected one Hopf surjectivity proof")
    hopf = matched[0]
    if len(hopf.premises) != 3:
        raise AssertionError("Hopf proof must contain its derived codomain")
    image, source, group = hopf.premises
    if (image.rule is not ProofRule.GIVEN or source.rule is not ProofRule.GIVEN
            or group.rule is not ProofRule.INFERENCE or len(group.premises) != 1
            or group.premises[0].rule is not ProofRule.GIVEN
            or group.premises[0].inference_rule.literature_reference.locator != "Proposition 5.1"
            or group.conclusion.lhs != goal.map.target_group):
        raise AssertionError("invalid Hopf codomain proof ancestry")
    refs = tuple(c.reference.locator for c in model.citations)
    if "Proposition 5.1" not in refs or "(5.1)" not in refs or "(5.3)" not in refs:
        raise AssertionError("missing cited source")
    return {
        "phase": "169-R3Y", "pi53_status": proof.status.value,
        "proof_step_count": len(model.steps),
        "hopf_premise_types": [type(p.conclusion).__name__ for p in hopf.premises],
        "hopf_premise_rules": [p.rule.value for p in hopf.premises],
        "codomain_inference_rule": group.inference_rule.name,
        "codomain_source_locator": group.premises[0].inference_rule.literature_reference.locator,
        "references": refs, "full_pytest_run": False,
    }


def main():
    report = examine()
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    for key, value in report.items():
        print("R3Y_" + key.upper() + "=" + repr(value))
    print("R3Y_REPORT=" + str(output))


if __name__ == "__main__":
    main()
