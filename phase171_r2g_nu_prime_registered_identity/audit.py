"""Verify only the registered nu-prime presentation identity, not a group proof."""
from __future__ import annotations

import json
import sys

from expression import Multiple
from homotopy_groups import FiniteCyclicGroup
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2e_toda53_double_reference import ASSERTION_ID
from proof import ProofRule


def audit() -> int:
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(targets) != 1:
        raise RuntimeError("expected exactly one typed pi_6^3 DB goal")
    target = targets[0]
    if not isinstance(target.rhs, FiniteCyclicGroup) or target.rhs.order != 4:
        raise RuntimeError("unexpected pi_6^3 target structure")
    source_id = "shared:12:" + ASSERTION_ID
    source = bridge.registry.assertion(source_id).content
    if not isinstance(source.lhs, Multiple) or source.lhs.coefficient != 2:
        raise RuntimeError("unexpected R2E double relation")
    cited = source.lhs.expression
    db = target.rhs.generator
    if db == cited:
        raise RuntimeError("this audit expects structurally distinct generator presentations")
    if not same_registered_group_presentation(target.rhs, FiniteCyclicGroup(4, cited)):
        raise RuntimeError("R2G HyoujiGen identity mismatch")
    citing_id = resolve_specialized_goal_citing_id(bridge, target)
    if not citing_id or not precedes_citing_assertion(bridge, source_id, citing_id):
        raise RuntimeError("R2E source is not strictly prior to pi_6^3 goal")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    matches = tuple(link for link in screened.proof_links
                    if link.assertion_id == source_id
                    and link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and not link.step.premises
                    and link.step.conclusion == source)
    if len(matches) != 1:
        raise RuntimeError("R2E source is not exactly one screened GIVEN")
    if any(link.step is not None and link.step.conclusion == target
           for link in screened.proof_links):
        raise RuntimeError("DB goal must never become a direct proof leaf")
    result = {
        "coordinate": "pi_6^3",
        "master_id": 3,
        "raw_generator_dataclass_equal": False,
        "registered_presentation_identity": True,
        "screened_r2e_given_count": len(matches),
        "root_proof_created": False,
    }
    print("PHASE171_R2G_IDENTITY=" + json.dumps(result, ensure_ascii=False), flush=True)
    print("PHASE171_R2G_RESULT=PASS_SOURCE_IDENTITY_ONLY", flush=True)
    return 0


def main() -> int:
    try:
        return audit()
    except Exception as exc:
        print("PHASE171_R2G_AUDIT_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
