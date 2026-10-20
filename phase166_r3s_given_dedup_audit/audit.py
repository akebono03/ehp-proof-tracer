"""Phase 166 R3-S: read-only audit of Hopf GIVEN de-duplication and regressions."""
from __future__ import annotations

import json
from pathlib import Path

from proof import ProofRule, Relation
from phase165_r14_r6_generic_iso import GeneratorImage

HOPF_RELATION_IDS = (
    "shared:2:toda:adopted:prop5.1:eta2_hopf_relation",
    "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation",
)


def inspect_bridge(bridge: object) -> dict:
    """Keep assertions in registry; forbid the two duplicate relation GIVEN links."""
    links = tuple(bridge.proof_links)
    ids = [link.assertion_id for link in links]
    relation_given = [
        link.assertion_id for link in links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, Relation)
    ]
    image_given = [
        link.assertion_id for link in links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, GeneratorImage)
    ]
    registered = [
        assertion_id for assertion_id in HOPF_RELATION_IDS
        if assertion_id in bridge.registry._assertions
    ]
    duplicate = [identifier for identifier in HOPF_RELATION_IDS if identifier in ids]
    return {
        "registered_hopf_relation_assertions": registered,
        "duplicate_hopf_relation_given_links": duplicate,
        "generator_image_given_links": image_given,
        "other_relation_given_link_count": len(relation_given),
        "other_relation_given_link_ids": relation_given,
        "no_duplicate_hopf_given": not duplicate,
        "registered_assertions_preserved": bool(registered),
    }


def run_audit() -> dict:
    from homotopy_groups import FreeCyclicGroup
    from hopf_facts import ETA_2
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
    from web_group_proof import build_standard_web_group_proof_view

    bridge = build_shared_typed_bridge()
    before = tuple(bridge.proof_links)
    link_report = inspect_bridge(bridge)
    result = search_shared_group_goal(
        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge
    )
    from phase166_r3r_proof_tree_audit.audit import audit_relation_steps
    ancestry = audit_relation_steps(tuple(result.proven_steps), bridge)
    views = {}
    for n, k in ((2, 1), (3, 1)):
        view = build_standard_web_group_proof_view(n, k, 2, "narrative")
        content = "\n".join(
            line.prefix + " " + " ".join(segment.value for segment in line.segments)
            for line in view.rendered_lines
        )
        views[f"pi_{n+k}^{n}"] = {
            "has_goal": "証明対象" in content,
            "has_references": "使用する結果" in content,
            "has_proof": "証明" in content,
            "line_count": len(view.rendered_lines),
        }
    passed = (
        link_report["no_duplicate_hopf_given"]
        and link_report["registered_assertions_preserved"]
        and bool(link_report["generator_image_given_links"])
        and result.status is ProofSearchStatus.COMPLETE
        and ancestry["derived_image_relation_chain_verified"]
        and all(all(v[key] for key in ("has_goal", "has_references", "has_proof")) for v in views.values())
        and tuple(bridge.proof_links) == before
    )
    return {
        "phase": "166 R3-S", "mode": "read_only", "production_code_modified": False,
        "bridge": link_report,
        "pi32_search_status": result.status.name,
        "pi32_proven_steps": len(result.proven_steps),
        "pi32_image_relation_chain_verified": ancestry["derived_image_relation_chain_verified"],
        "web_views": views,
        "pass": passed,
        "full_pytest_run": False,
    }


def main() -> int:
    report = run_audit()
    target = Path(__file__).resolve().with_name("r3s_audit.json")
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("REPORT:", target)
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
