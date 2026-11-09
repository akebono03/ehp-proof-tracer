"""R30 shared public-provider wiring and cited-screened proof audit."""
from __future__ import annotations

import argparse
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, shared_expansion_provider,
)
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from phase174_r3_r7_r30_prop27_public_provider_wiring.install import preflight
from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
    has_certified_prop27_leaf,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parents[1]


def audit_public_wiring() -> dict[str, object]:
    """Measure the *real* default shared bridge and source-first screen."""
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    target = typed_specialization(6)
    original = build_shared_typed_bridge()
    if not has_certified_prop27_leaf(original):
        raise RuntimeError("default shared registry lacks cited Proposition 2.7 leaf")
    screened = screen_independent_sources_for_derived_goal(original, goal=goal)
    if not has_certified_prop27_leaf(screened):
        raise RuntimeError("source-first public screen removed Proposition 2.7")
    provider = shared_expansion_provider(screened, proof_target=goal)
    options = provider(target)
    matches = tuple(item for item in options if item.subgoals and
                    len(item.subgoals) == 1 and
                    item.rule.name == "Toda Proposition 2.7 even-dimensional typed Hopf-Delta specialization")
    if len(matches) != 1:
        raise RuntimeError("shared public provider did not expose unique typed R29 proposal")
    citation_id = next(iter(screened.registry._assertions))
    step = reconstruct_registered_goal(
        target, screened, citation_id, provider, lookup_mode="typed_reference",
    )
    if (step.rule is not ProofRule.INFERENCE or step.conclusion != target
            or len(step.premises) != 1 or step.premises[0].rule is not ProofRule.INFERENCE
            or len(step.premises[0].premises) != 1
            or step.premises[0].premises[0].rule is not ProofRule.GIVEN
            or type(step.premises[0].premises[0].conclusion)
            is not Prop27UniversalLiteratureStatement):
        raise RuntimeError("normal shared provider lost source-backed proof ancestry")
    return {
        "default_source_present": True,
        "public_source_screen_admits_prop27": True,
        "public_shared_provider_candidates": len(matches),
        "public_verified_n6_inference": True,
        "n6_direct_given_count": 0,
        "web_http_route_tested": False,
        "delta_surjectivity_proved": False,
        "root_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, _expected, installed = preflight()
    print("PHASE174_R3R7R30_HEAD=" + head)
    print("PHASE174_R3R7R30_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R30_INSTALLED=" + str(installed))
    if args.dry_run:
        print("PHASE174_R3R7R30_GATE=PASS_R30_SOURCE_PREFLIGHT_ONLY")
    else:
        if not installed:
            raise RuntimeError("R30 source wiring not yet installed")
        for key, value in audit_public_wiring().items():
            print("PHASE174_R3R7R30_" + key.upper() + "=" + str(value))
        print("PHASE174_R3R7R30_GATE=PASS_R30_SHARED_PUBLIC_PROVIDER_CITED_INFERENCE_ROOT_PENDING")
    print("PHASE174_R3R7R30_FULL_PYTEST=False")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
