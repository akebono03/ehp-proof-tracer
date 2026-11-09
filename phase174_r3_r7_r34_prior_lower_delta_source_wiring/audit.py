"""R34 cited lower-Delta prior-source screen and provider audit.

Reports proven source leaves separately from later (unproved) kernel/root
claims. No inference step is fabricated by this audit.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r34_prior_lower_delta_source_wiring.install import preflight
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    ROOT,
    build_cited_lower_delta_sources,
)


def screen_report() -> dict[str, object]:
    from homotopy_groups import (
        FiniteCyclicGroup,
        FreeCyclicGroup,
        TodaDeltaMap,
        TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from proof import ProofRule, ProofStep, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    domain, codomain = TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5)
    delta = TodaDeltaMap(domain, codomain)
    isolated = build_cited_lower_delta_sources(ROOT)
    if len(isolated.proof_links) != 2:
        raise RuntimeError("R34 must register exactly two independent source leaves")
    registered = build_shared_typed_bridge()
    screen = screen_independent_sources_for_derived_goal(registered, goal=root)
    steps = tuple(
        link.step for link in screen.proof_links
        if type(link.step) is ProofStep and link.step.rule is ProofRule.GIVEN
    )
    group_steps = tuple(s for s in steps
                        if type(s.conclusion) is Relation
                        and s.conclusion.relation_type is RelationType.EQUALITY
                        and s.conclusion.lhs == codomain
                        and type(s.conclusion.rhs) is FiniteCyclicGroup
                        and s.conclusion.rhs.order == 2)
    delta_steps = tuple(s for s in steps
                        if type(s.conclusion) is TodaDeltaImageUpToSignStatement
                        and s.conclusion.map == delta)
    diagonal_steps = tuple(s for s in steps
                           if type(s.conclusion) is Relation
                           and s.conclusion.relation_type is RelationType.EQUALITY
                           and s.conclusion.lhs == domain
                           and type(s.conclusion.rhs) is FreeCyclicGroup)
    if len(group_steps) != 1 or len(delta_steps) != 1:
        raise RuntimeError("Two independently cited earlier leaves not publicly screened")
    expected_group = isolated.proof_links[0].step.conclusion
    expected_delta = isolated.proof_links[1].step.conclusion
    if group_steps[0].conclusion != expected_group or delta_steps[0].conclusion != expected_delta:
        raise RuntimeError("Source and public screened claims have different identities")
    if any(s.conclusion == root for s in steps) or any(
        type(s.conclusion) is KernelMultipleStatement and s.conclusion.map == delta
        for s in steps
    ):
        raise RuntimeError("An unproved kernel or root was registered as GIVEN")
    return {
        "screened_prior_codomain_leaves": len(group_steps),
        "screened_prior_delta_generator_leaves": len(delta_steps),
        "screened_concrete_diagonal_leaves": len(diagonal_steps),
        "signed_image_is_conservative_for_exact_equation": True,
        "prior_literature_citations": ["Proposition 5.8", "(5.10)"],
        "db_generator_is_independent_literature_source": False,
        "new_source_givens": 2,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_math_rules": 0,
        "lower_kernel_proved": False,
        "delta_surjectivity_proved": False,
        "root_complete": False,
        "full_pytest": False,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    state = preflight()
    screen = None if dry_run else screen_report()
    return {
        "phase": "174-R3-R7-R34",
        "git_state": state,
        "source": screen,
        "gate": (
            "PASS_R34_PRIOR_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R34_TWO_EARLIER_CITED_LEAVES_SCREENED_DOMAIN_AND_KERNEL_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r34"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "prior_cited_source.json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R34_"
    for key in ("local_head", "remote_head", "source_guard", "mode", "earlier_phases_preserved"):
        print(p + key.upper() + "=" + str(result["git_state"][key]))
    if result["source"] is not None:
        for key, value in result["source"].items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
