"""Phase 169 R10E: read-only proof-source and group-shape boundary diagnosis.

No reconstructed source is promoted to a GIVEN step. Search statuses are
reported as observed, and DB rows remain candidate goal metadata only.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaPrimaryGroupZeroStatement,
)
from proof import ProofRule, Relation

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
TARGETS = ((8, 4), (8, 6), (15, 7), (15, 8), (15, 9))


def group_shape(goal: object) -> str:
    """Classify the actual typed goal; do not infer group structure from a label."""
    if isinstance(goal, TodaPrimaryGroupZeroStatement):
        return "zero_group"
    if isinstance(goal, Relation):
        structure = goal.rhs
        if isinstance(structure, FiniteCyclicGroup):
            return "finite_cyclic"
        if isinstance(structure, FreeCyclicGroup):
            return "free_cyclic"
        if isinstance(structure, DirectSumGroup):
            return "direct_sum"
    return "other"


def _goal_description(goal: object) -> dict:
    return {
        "type": type(goal).__name__,
        "shape": group_shape(goal),
        "repr": repr(goal),
    }


def _safe_citing_id(bridge, goal: object) -> str | None:
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    if not isinstance(goal, Relation):
        return None
    return resolve_specialized_goal_citing_id(bridge, goal)


def audit_case(bridge, *, n: int, k: int) -> dict:
    """Inspect a real DB goal, screened citations, and the unchanged R7 guard."""
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
    from phase169_r3m_prior_result_catalog.prior_results import (
        _database_result_candidates,
        resolve_prior_group_result,
    )
    from phase169_r7_general_stable_transport.rule import (
        _consecutive_generator_image_goals,
        expand_prior_general_stable_transport,
    )

    zero_goals = database_zero_group_goal_candidates(n=n, k=k)
    relations = registered_group_goal_candidates(bridge, n=n, k=k)
    goals = zero_goals if zero_goals else relations
    report = {
        "group": f"pi_{n+k}^{n}",
        "n": n,
        "stem": k,
        "stable_source_minimum_n": k + 2,
        "target_is_stable": n >= k + 2,
        "lower_stable_source_exists": n > k + 2,
        "zero_database_goal_count": len(zero_goals),
        "registered_group_goal_count": len(relations),
        "goals": [_goal_description(goal) for goal in goals],
        "goal_details": [],
    }
    for goal in goals:
        kind = group_shape(goal)
        citing = _safe_citing_id(bridge, goal)
        item = {
            "goal_type": type(goal).__name__,
            "group_shape": kind,
            "citing_assertion_id": citing,
            "r7_root_shape_accepted": kind == "finite_cyclic",
            "prior_sources": [],
            "r7_direct_candidate_count": None,
            "provider_root_option_count": None,
            "provider_root_rule_names": [],
            "visible_general_family_ids": [],
        }
        screened = None
        available = ()
        if citing is not None:
            screened = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing,
                explicit_publication_target=True,
            )
            links = tuple(link.step for link in screened.proof_links
                          if link.step is not None
                          and link.step.rule is ProofRule.GIVEN)
            available = tuple(step.conclusion for step in links)
            item["screened_given_count"] = len(links)
            item["visible_general_family_ids"] = sorted(set(
                statement.family_id for statement in available
                if type(statement).__name__ == "CitedStableFamilyDefinition"
                and type(getattr(statement, "family_id", None)) is int
            ))
            provider = shared_expansion_provider(screened, proof_target=goal)
            options = provider(goal)
            item["provider_root_option_count"] = len(options)
            item["provider_root_rule_names"] = sorted(set(
                getattr(option.rule, "name", type(option.rule).__name__)
                for option in options
            ))
            if kind == "finite_cyclic":
                item["r7_direct_candidate_count"] = len(
                    expand_prior_general_stable_transport(
                        goal, available, screened, proof_target=goal,
                    )
                )

        if n > k + 2:
            for source_n in range(k + 2, n):
                candidates = _database_result_candidates(
                    source_n=source_n, source_k=k,
                )
                prior = {
                    "source_group": f"pi_{source_n+k}^{source_n}",
                    "db_result_count": len(candidates),
                    "source_shapes": [group_shape(x) for x in candidates],
                    "publication_eligibility": "unknown_without_target_citation",
                }
                if citing is not None:
                    source = resolve_prior_group_result(
                        bridge, source_n=source_n, source_k=k,
                        citing_assertion_id=citing,
                    )
                    prior.update({
                        "publication_eligibility": source.eligible,
                        "reason": source.reason,
                        "source_assertion_id": source.source_assertion_id,
                    })
                    if (source.relation is not None
                            and isinstance(goal, Relation)
                            and kind == "finite_cyclic"):
                        images = _consecutive_generator_image_goals(
                            source.relation, goal,
                        )
                        prior["typed_generator_image_goal_count"] = (
                            len(images) if images is not None else None
                        )
                item["prior_sources"].append(prior)
        report["goal_details"].append(item)
    return report


def main() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    bridge = build_shared_typed_bridge()
    report = {
        "phase": "169 R10E0",
        "kind": "AUDIT_ONLY",
        "head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "proof_steps_created": 0,
        "production_files_modified": [],
        "full_pytest_run": False,
        "cases": [audit_case(bridge, n=n, k=k) for n, k in TARGETS],
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 169 R10E0: 型付き輸送の共通境界監査",
        "",
        "AUDIT_ONLY：本番コード・既存テストを変更しない。",
        "DB の目標候補は引用可能な数学的証明とは区別する。",
        "",
        "| 群 | Goal 型 | R7 直接適用 | 先行安定範囲 | 引用に適格な先行 DB 結果 |",
        "|---|---|---|---|---|",
    ]
    for item in report["cases"]:
        details = item["goal_details"]
        shapes = ", ".join(sorted({x["group_shape"] for x in details})) or "候補なし"
        root = ", ".join("yes" if x["r7_root_shape_accepted"] else "no"
                         for x in details) or "no"
        eligible = sum(1 for d in details for x in d["prior_sources"]
                       if x["publication_eligibility"] is True)
        lines.append(
            f"| `{item['group']}` | {shapes} | {root} | "
            f"{'yes' if item['lower_stable_source_exists'] else 'no'} | {eligible} |"
        )
    lines.extend([
        "",
        "## 監査の解釈",
        "",
        "- `finite_cyclic` 以外では、現行 R7 は根 Goal を直接展開しない。",
        "- 最初の安定次元 `n=k+2` には、それより低次元の安定な輸送元がない。",
        "- 先行 DB 結果は、掲載順が適格であっても自動的な証明済み GIVEN ではない。",
        "- `visible_general_family_ids` は引用審査で残った系列定義の ID。",
        "- 詳細は同じフォルダの audit.json を参照。",
        "",
        "全体 pytest は実行していない。",
        "",
    ])
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"R10E0_HEAD={report['head']}")
    for item in report["cases"]:
        shapes = ",".join(sorted({x["group_shape"] for x in item["goal_details"]}))
        prior = sum(1 for d in item["goal_details"] for x in d["prior_sources"]
                    if x["publication_eligibility"] is True)
        print(f"R10E0_{item['group']}_SHAPES={shapes or 'none'}")
        print(f"R10E0_{item['group']}_ELIGIBLE_PRIOR={prior}")
    print(f"R10E0_AUDIT_JSON={destination}")
    print(f"R10E0_AUDIT_MD={OUTPUT / 'audit.md'}")
    print("R10E0_PRODUCTION_FILES_CHANGED=none")
    print("R10E0_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
