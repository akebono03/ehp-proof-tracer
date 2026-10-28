"""Phase 169 R10ET-R2: shadow-only common Definition preference audit.

This audit never edits application or test source. The sole change is a temporary
in-process replacement of a function reference; the original is restored.
A failure to retain a trusted complete proof is recorded, not concealed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Callable

sys.dont_write_bytecode = True

BASE_HEAD = "36e4dc41427ec4437009c96b01cacb07dc165bf6"
AUDIT_HEAD = "a5892721436effaf7be759ff17afd3bd427814ed"
EXPECTED_SHARED_MATH_BLOB = "61cbadb06f770c51a9c1f5a3c8026acf9e3e14aa"
ALLOWED_HEADS = frozenset((BASE_HEAD, AUDIT_HEAD))
BASELINE = (
    "phase169_r10et_r1_definition_reference_dependency_audit/"
    "output/20261028_150930_366/audit.json"
)
CORE_CASES = ((43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9))
LOW_CASES = ((2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2))
PROJECTION_CASES = ((22, 6), (22, 10), (15, 8), (24, 9))


def git_output(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def tracked_status(root: Path) -> tuple[str, str]:
    return (git_output(root, "diff", "--name-status"),
            git_output(root, "diff", "--cached", "--name-status"))


def prioritize_common_definition(legacy_provider: Callable) -> Callable:
    """Return canonical, replay-checked zero-premise proposals when defined.

    No source is fabricated. Noneligible goals use the unmodified provider.
    This wrapper only exists in the auditing interpreter, not production.
    """
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        expand_defined_stable_element_image,
    )

    def expand(goal: object):
        defined = expand_defined_stable_element_image(goal)
        return defined if defined else legacy_provider(goal)

    return expand


def shadow_provider_factory(original_factory: Callable) -> Callable:
    """Build the usual screened provider, then prioritize proven Definition goals."""
    def factory(*args, **kwargs):
        return prioritize_common_definition(original_factory(*args, **kwargs))
    return factory


def read_baseline(root: Path) -> dict[str, dict]:
    path = root / BASELINE
    if not path.is_file():
        raise FileNotFoundError(f"reviewed R10ET-R1 baseline not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (data.get("head") != BASE_HEAD or data.get("mode") != "AUDIT_ONLY"
            or not data.get("tracked_unchanged")
            or any(case.get("trust") != "PASS" for case in data.get("cases", ()))):
        raise RuntimeError("R10ET-R1 baseline is incomplete or not the reviewed HEAD")
    return {item["group"]: item for item in data["cases"]}


def compare_case(case: dict, previous: dict | None) -> dict:
    """Compare actual tracked proof evidence; no display-based inference."""
    if previous is None or case.get("trust") != "PASS":
        return {"previous_available": previous is not None}
    old_refs = [row["locator"] for row in previous.get("references", ())]
    new_refs = [row["locator"] for row in case.get("references", ())]
    old_proj = previous.get("direct_sum_projection")
    new_proj = case.get("direct_sum_projection")
    return {
        "previous_available": True,
        "previous_references": old_refs,
        "new_references": new_refs,
        "removed_references": [x for x in old_refs if x not in new_refs],
        "added_references": [x for x in new_refs if x not in old_refs],
        "baseline_common_images": previous.get("image_actual_common"),
        "shadow_common_images": case.get("image_actual_common"),
        "baseline_cited_common_eligible": previous.get("image_cited_but_common_eligible"),
        "shadow_cited_common_eligible": case.get("image_cited_but_common_eligible"),
        "before_root_support": previous.get("root_first_two_premise_support"),
        "after_root_support": case.get("root_first_two_premise_support"),
        "baseline_projection_present": old_proj is not None,
        "shadow_projection_present": new_proj is not None,
        "baseline_equations": None if old_proj is None else old_proj.get("statement"),
        "shadow_equations": None if new_proj is None else new_proj.get("statement"),
    }


def inspect_cyclic_projection(bridge: object, n: int, k: int) -> dict:
    """Check the existing cyclic display gate under the same shadow preference."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase169_r10a_verified_stable_chain_projection.projection import (
        project_verified_stable_image_chain,
    )

    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        return {"status": result.status.value, "trust": "NOT_COMPLETE"}
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(x.step_index for x in project_narrative_order(model))
    display = project_verified_stable_image_chain(model, order)
    return {
        "status": "complete", "trust": "PASS",
        "cyclic_projection_present": display is not None,
        "cyclic_citation_numbers": ([] if display is None
                                    else list(display.citation_numbers)),
        "reference_locators": [x.reference.locator or x.reference.label
                               for x in model.citations],
    }


def markdown_report(report: dict) -> str:
    lines = [
        "# Phase 169 R10ET-R2 — 共通 Definition 優先の影響比較",
        "", "**AUDIT_ONLY。アプリケーション実装・既存テスト・文書は変更しない。**",
        "", f"- HEAD: `{report['head']}`",
        f"- 基準 HEAD: `{BASE_HEAD}`",
        f"- 基準ソース Blob: `{EXPECTED_SHARED_MATH_BLOB}`",
        f"- 追跡対象差分は不変: `{report['tracked_unchanged']}`",
        "- 全体 pytest: 未実行", "",
        "| 群 | 完成 | Trust | 共通 Definition 実採用 | 引用付き適用可能 | 引用数 | 圧縮表示 |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for case in report["cases"]:
        lines.append(
            f"| `{case['group']}` | {case.get('status', 'ERROR')} | "
            f"{case.get('trust', 'ERROR')} | "
            f"{case.get('image_actual_common', '-')} | "
            f"{case.get('image_cited_but_common_eligible', '-')} | "
            f"{len(case.get('references', []))} | "
            f"{case.get('direct_sum_projection') is not None} |"
        )
    lines.extend(("", "## 個別 Reference の比較", ""))
    for case in report["cases"]:
        diff = case.get("comparison", {})
        if not diff.get("previous_available"):
            continue
        lines.append(f"### `{case['group']}`")
        lines.append(f"- 消えた Reference: {diff['removed_references']}")
        lines.append(f"- 新たな Reference: {diff['added_references']}")
        lines.append(f"- 元の直和圧縮表示: {diff['baseline_projection_present']}")
        lines.append(f"- 試験経路の直和圧縮表示: {diff['shadow_projection_present']}")
        lines.append("")
    lines.extend(("## 巡回群の圧縮表示", ""))
    for case in report.get("cyclic", []):
        lines.append(
            f"- `{case['group']}`: {case.get('trust')}, "
            f"projection={case.get('cyclic_projection_present', 'ERROR')}"
        )
    lines.extend((
        "", "## 実装判定", "",
        "共通 Definition で Proof Tree を再構築して Trust が通っても、"
        "古い引用前提に依存する Projection が不成立になれば、単純な探索優先順変更は採用しない。",
        "Proof Tree の不要な個別引用を表示側だけで消さない。",
        "DB prior と Toda (4.5) は別の前提として維持する。",
        "監査段階での PASS は、実装変更の完了を意味しない。",
        "",
    ))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", choices=("core", "all"), default="all")
    args = parser.parse_args(argv)

    root, output = args.root.resolve(), args.output.resolve()
    if git_output(root, "branch", "--show-current") != "develop":
        raise SystemExit("R10ET-R2 REFUSED: not on develop")
    head = git_output(root, "rev-parse", "HEAD")
    if head not in ALLOWED_HEADS:
        raise SystemExit(f"R10ET-R2 REFUSED: unreviewed HEAD {head}")
    blob = git_output(root, "hash-object", "phase165_r52_r9_shared_math.py")
    if blob != EXPECTED_SHARED_MATH_BLOB:
        raise SystemExit("R10ET-R2 REFUSED: current production provider differs")
    initial = tracked_status(root)
    if any(initial):
        raise SystemExit("R10ET-R2 REFUSED: preexisting tracked changes")
    baseline = read_baseline(root)
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(root))
    from phase169_r10et_r1_definition_reference_dependency_audit.audit import (
        inspect_case,
    )
    import phase165_r52_r9_shared_math as shared

    original_factory = shared.shared_expansion_provider
    report = {
        "phase": "169 R10ET-R2", "mode": "AUDIT_ONLY_SHADOW",
        "head": head, "base_head": BASE_HEAD, "source_blob": blob,
        "cases": [], "cyclic": [], "full_pytest_run": False,
        "production_changed": [], "in_process_provider_override_only": True,
    }
    scenario = CORE_CASES if args.cases == "core" else (
        CORE_CASES + LOW_CASES + PROJECTION_CASES
    )
    try:
        bridge = shared.build_shared_typed_bridge()
        shared.shared_expansion_provider = shadow_provider_factory(original_factory)
        for n, k in scenario:
            group = f"pi_{n+k}^{n}"
            print(f"R10ET_R2_START={group}", flush=True)
            try:
                case = inspect_case(bridge, n, k, output)
                case["comparison"] = compare_case(case, baseline.get(group))
            except Exception as exc:
                case = {
                    "group": group, "status": "ERROR", "trust": "ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            report["cases"].append(case)
            print(f"R10ET_R2_{group}_STATUS={case.get('status')}", flush=True)
            print(f"R10ET_R2_{group}_TRUST={case.get('trust')}", flush=True)
            if "image_actual_common" in case:
                print(f"R10ET_R2_{group}_COMMON_IMAGES={case['image_actual_common']}", flush=True)
                print(f"R10ET_R2_{group}_CITED_COMMON_ELIGIBLE={case['image_cited_but_common_eligible']}", flush=True)
        if args.cases == "all":
            for n, k in ((22, 6), (22, 10)):
                group = f"pi_{n+k}^{n}"
                try:
                    projection = inspect_cyclic_projection(bridge, n, k)
                    projection["group"] = group
                except Exception as exc:
                    projection = {"group": group, "trust": "ERROR",
                                  "error": f"{type(exc).__name__}: {exc}",
                                  "traceback": traceback.format_exc()}
                report["cyclic"].append(projection)
                print(f"R10ET_R2_{group}_CYCLIC_PROJECTION={projection.get('cyclic_projection_present')}", flush=True)
    finally:
        shared.shared_expansion_provider = original_factory
        report["provider_restored"] = shared.shared_expansion_provider is original_factory
        report["tracked_unchanged"] = initial == tracked_status(root)
        report["all_complete_trusted"] = all(
            x.get("status") == "complete" and x.get("trust") == "PASS"
            for x in report["cases"]
        ) and all(x.get("trust") == "PASS" for x in report["cyclic"])
        report["lost_direct_sum_projection"] = [x["group"] for x in report["cases"]
            if x.get("comparison", {}).get("baseline_projection_present")
            and not x.get("comparison", {}).get("shadow_projection_present")]
        report["lost_cyclic_projection"] = [x["group"] for x in report["cyclic"]
            if not x.get("cyclic_projection_present")]
        report["core_provenance_preserved"] = all(
            case.get("comparison", {}).get("previous_available")
            and case["comparison"]["before_root_support"]
                == case["comparison"]["after_root_support"]
            and case.get("image_cited_but_common_eligible") == 0
            and len(case.get("references", ())) == 2
            and "DB prior" in case["references"][0]["locator"]
            and case["references"][1]["locator"] == "(4.5)"
            for case in report["cases"]
            if (case.get("n"), case.get("k")) in CORE_CASES
        )
        report["ready_for_implementation"] = bool(
            report["all_complete_trusted"] and report["tracked_unchanged"]
            and report["provider_restored"] and report["core_provenance_preserved"]
            and not report["lost_direct_sum_projection"]
            and not report["lost_cyclic_projection"]
        )
        (output / "audit.json").write_text(json.dumps(
            report, ensure_ascii=False, indent=2,
        ) + "\n", encoding="utf-8")
        (output / "audit.md").write_text(markdown_report(report), encoding="utf-8")
        print(f"R10ET_R2_REPORT={output / 'audit.md'}", flush=True)
        print(f"R10ET_R2_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"R10ET_R2_PROVIDER_RESTORED={report['provider_restored']}", flush=True)
        print(f"R10ET_R2_ALL_COMPLETE_TRUSTED={report['all_complete_trusted']}", flush=True)
        print(f"R10ET_R2_READY_FOR_IMPLEMENTATION={report['ready_for_implementation']}", flush=True)
    return 0 if report["tracked_unchanged"] and report["provider_restored"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
