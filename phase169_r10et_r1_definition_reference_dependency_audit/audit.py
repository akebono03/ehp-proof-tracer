"""Phase 169 R10ET-R1: read-only real Proof Tree / Definition / Reference audit.

This script does not modify proofs, registry, renderers, or tracked files.
Only run against an already installed EHP Proof Tracer working tree.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

EXPECTED_HEAD = "36e4dc41427ec4437009c96b01cacb07dc165bf6"
CORE_CASES = (
    (43, 26),
    (30, 26),
    (30, 11),
    (30, 14),
    (30, 16),
    (30, 9),
)
LOW_STEM_CASES = (
    (2, 1),
    (3, 1),
    (4, 1),
    (2, 2),
    (3, 2),
    (4, 2),
)
ALL_CASES = CORE_CASES + LOW_STEM_CASES


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def tracked_status(root: Path) -> dict[str, str]:
    return {
        "tracked_unstaged": git_output(root, "diff", "--name-status"),
        "tracked_staged": git_output(root, "diff", "--cached", "--name-status"),
    }


def clipped(value: object, limit: int = 1200) -> str:
    data = repr(value)
    return data if len(data) <= limit else data[:limit] + " [repr truncated]"


def linked_index(step: object, by_id: dict[int, int], steps: tuple) -> int:
    index = by_id.get(id(step))
    if index is not None:
        return index
    found = [i for i, candidate in enumerate(steps) if candidate == step]
    if len(found) == 1:
        return found[0]
    raise ValueError(f"ambiguous or missing ProofStep identity: {clipped(step, 200)}")


def ancestor_indices(index: int, dependencies: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    pending = [index]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(dependencies[current])
    return tuple(sorted(seen))


def canonical_definition_inference(step: object) -> bool:
    """Check actual zero-premise inference identity, never merely its name."""
    from proof import InferenceRule, ProofRule, find_inference_matches_for_rule
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        expand_defined_stable_element_image,
    )

    if (getattr(step, "rule", None) is not ProofRule.INFERENCE
            or getattr(step, "premises", None) != ()
            or not isinstance(getattr(step, "inference_rule", None), InferenceRule)):
        return False
    proposals = expand_defined_stable_element_image(step.conclusion)
    if len(proposals) != 1 or proposals[0].subgoals:
        return False
    actual, canonical = step.inference_rule, proposals[0].rule
    return (
        actual.name == canonical.name
        and actual.description == canonical.description
        and actual.premise_patterns == canonical.premise_patterns
        and actual.conclusion_pattern == canonical.conclusion_pattern
        and actual.conclusion_builder is None
        and actual.literature_reference is None
        and len(find_inference_matches_for_rule(actual, ())) == 1
    )


def step_linked_citations(model: object) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cite in model.citations:
        rows.append({
            "number": cite.number,
            "locator": cite.reference.locator or cite.reference.label,
            "step_indices": list(cite.step_indices),
            "assertion_ids": list(cite.assertion_ids),
            "reference_ids": list(cite.reference_ids),
            "statement_bodies": list(cite.statement_bodies),
        })
    return rows


def body_text(markdown: str) -> str:
    parts = re.split(r"(?m)^(?:##\s*)?証明\s*$", markdown, maxsplit=1)
    return parts[-1] if len(parts) == 2 else ""


def inspect_case(bridge: object, n: int, k: int, output: Path) -> dict[str, Any]:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase169_r10ec_direct_sum_narrative_projection.projection import (
        project_verified_direct_sum_transport,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        is_defined_stable_image,
    )
    from phase165_r14_r6_generic_iso import GeneratorImage
    from proof import ProofRule

    name = f"pi_{n+k}^{n}"
    folder = output / f"pi{n+k}_{n}"
    folder.mkdir(parents=True, exist_ok=False)
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    base: dict[str, Any] = {
        "group": name,
        "n": n,
        "k": k,
        "status": result.status.value,
        "open_goal_types": [type(goal).__name__ for goal in result.open_goals],
        "open_goals": [clipped(goal, 1500) for goal in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "context_count": len(contexts),
    }
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
        base["trust"] = "NOT_APPLICABLE_INCOMPLETE"
        return base
    if len(contexts) != 1:
        raise RuntimeError(f"{name}: complete search has {len(contexts)} contexts")

    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferences, givens = verify_proof_tree_for_narrative(
        result,
        contexts[0],
        citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    before = (tuple(id(step) for step in model.steps), model.step_citation_numbers)
    markdown = render_model_backed_narrative_markdown(result, model)
    after = (tuple(id(step) for step in model.steps), model.step_citation_numbers)
    if before != after:
        raise RuntimeError(f"{name}: renderer modified Proof Tree/citation association")
    if not markdown.rstrip().endswith("□"):
        raise RuntimeError(f"{name}: completion narrative does not end with □")

    steps = model.steps
    if len({id(step) for step in steps}) != len(steps):
        raise RuntimeError(f"{name}: duplicate ProofStep identities")
    by_id = {id(step): index for index, step in enumerate(steps)}
    dependencies = tuple(
        tuple(linked_index(parent, by_id, steps) for parent in step.premises)
        for step in steps
    )
    if model.root_index is None:
        raise RuntimeError(f"{name}: model root is absent")
    reachable = set(ancestor_indices(model.root_index, dependencies))
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    projection = project_verified_direct_sum_transport(model, order)
    citations = step_linked_citations(model)
    citation_by_number = {row["number"]: row for row in citations}

    records: list[dict[str, Any]] = []
    image_rows: list[dict[str, Any]] = []
    for index, step in enumerate(steps):
        rule = getattr(step.inference_rule, "name", None)
        source_reference = getattr(step.inference_rule, "literature_reference", None)
        row: dict[str, Any] = {
            "index": index,
            "root_ancestor": index in reachable,
            "proof_rule": getattr(step.rule, "value", str(step.rule)),
            "inference_rule": rule,
            "rule_source_locator": (
                source_reference.locator or source_reference.label
                if source_reference is not None else None
            ),
            "conclusion_type": type(step.conclusion).__name__,
            "conclusion_repr": clipped(step.conclusion, 1200),
            "premise_indices": list(dependencies[index]),
            "direct_citation_numbers": list(model.step_citation_numbers[index]),
        }
        if isinstance(step.conclusion, GeneratorImage):
            ancestors = ancestor_indices(index, dependencies)
            given_ancestors = tuple(
                j for j in ancestors if steps[j].rule is ProofRule.GIVEN
            )
            numbers = sorted({
                number
                for j in given_ancestors
                for number in model.step_citation_numbers[j]
            })
            compatible = is_defined_stable_image(step.conclusion)
            actual_common = canonical_definition_inference(step)
            row.update({
                "eligible_for_common_definition": compatible,
                "actual_canonical_common_definition": actual_common,
                "given_ancestor_indices": list(given_ancestors),
                "given_ancestor_citation_numbers": numbers,
                "given_ancestor_locators": [
                    citation_by_number[x]["locator"] for x in numbers
                    if x in citation_by_number
                ],
            })
            image_rows.append(row.copy())
        records.append(row)

    body = body_text(markdown)
    for citation in citations:
        number = citation["number"]
        related = citation["step_indices"]
        citation["reachable_from_root"] = any(j in reachable for j in related)
        citation["directly_attributed_to_given"] = any(
            steps[j].rule is ProofRule.GIVEN for j in related
        )
        citation["reference_heading_displayed"] = (
            f"**[R{number}]" in markdown
        )
        citation["body_marker_displayed"] = bool(
            re.search(rf"\[R{number}\](?!\d)", body)
        )
        citation["referenced_by_image_ancestry"] = [
            row["index"] for row in image_rows
            if number in row["given_ancestor_citation_numbers"]
        ]

    root = steps[model.root_index]
    root_premises = [linked_index(step, by_id, steps) for step in root.premises]
    root_support = []
    for idx in root_premises[:2]:
        ancestors = ancestor_indices(idx, dependencies)
        supporting = sorted({number
            for j in ancestors
            for number in model.step_citation_numbers[j]
        })
        root_support.append({
            "index": idx,
            "type": type(steps[idx].conclusion).__name__,
            "conclusion_repr": clipped(steps[idx].conclusion, 750),
            "citation_numbers": supporting,
        })

    summary = {
        **base,
        "trust": "PASS",
        "inferences": inferences,
        "givens": givens,
        "proof_steps": len(steps),
        "root_index": model.root_index,
        "root_ancestry_steps": len(reachable),
        "unreachable_steps": sorted(set(range(len(steps))) - reachable),
        "images": len(image_rows),
        "image_actual_common": sum(bool(x["actual_canonical_common_definition"]) for x in image_rows),
        "image_common_eligible": sum(bool(x["eligible_for_common_definition"]) for x in image_rows),
        "image_cited_but_common_eligible": sum(
            bool(x["eligible_for_common_definition"])
            and not bool(x["actual_canonical_common_definition"])
            and bool(x["given_ancestor_citation_numbers"])
            for x in image_rows
        ),
        "image_rules": dict(Counter(x["inference_rule"] or "(none)" for x in image_rows)),
        "references": citations,
        "root_first_two_premise_support": root_support,
        "direct_sum_projection": (
            None if projection is None else {
                "statement": projection.statement,
                "hidden_indices": list(projection.hidden_indices),
                "citation_numbers": list(projection.citation_numbers),
            }
        ),
        "narrative": str(folder / "narrative.md"),
        "trace": str(folder / "proof_steps.json"),
    }
    (folder / "narrative.md").write_text(markdown, encoding="utf-8")
    (folder / "proof_steps.json").write_text(
        json.dumps({
            "root_index": model.root_index,
            "root_premises": root_premises,
            "steps": records,
            "images": image_rows,
            "references": citations,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return summary


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 169 R10ET-R1 — Definition / Reference 依存関係監査",
        "",
        "監査方式：AUDIT_ONLY。記録は実行時の検証済み Proof Tree から取得。",
        "",
        f"- Branch: `{report['branch']}`",
        f"- HEAD: `{report['head']}`",
        f"- 期待 HEAD: `{EXPECTED_HEAD}`",
        f"- HEAD 一致: `{report['head_matches_expected']}`",
        f"- 既存 tracked 差分は不変: `{report['tracked_unchanged']}`",
        "- 全体 pytest: 実行しない",
        "",
        "## 実行結果",
        "",
        "| 群 | 探索 | Trust | 共通 Definition 実使用 / 適用可能 / 引用付き適用可能 | Reference |",
        "|---|---|---|---|---|",
    ]
    for case in report["cases"]:
        counts = "{}/{}/{}".format(
            case.get("image_actual_common", "-"),
            case.get("image_common_eligible", "-"),
            case.get("image_cited_but_common_eligible", "-"),
        )
        lines.append(
            f"| `{case['group']}` | {case.get('status', 'ERROR')} | "
            f"{case.get('trust', 'ERROR')} | {counts} | {len(case.get('references', []))} |"
        )
    lines.extend(("", "## Citation / image ancestor evidence", ""))
    for case in report["cases"]:
        lines.append(f"### `{case['group']}`")
        lines.append("")
        if "error" in case:
            lines.append(f"- ERROR: `{case['error']}`")
        else:
            lines.append(f"- status={case['status']}, trust={case.get('trust')}")
            for citation in case.get("references", []):
                lines.append(
                    f"- [R{citation['number']}] {citation['locator']} | "
                    f"root祖先={citation['reachable_from_root']} | "
                    f"GIVEN={citation['directly_attributed_to_given']} | "
                    f"image祖先={citation['referenced_by_image_ancestry']} | "
                    f"本文マーカー={citation['body_marker_displayed']}"
                )
            lines.append("- root 直前2前提の支持引用: " + clipped(
                case.get("root_first_two_premise_support", []), 1500))
            lines.append("- 直和圧縮: " + clipped(
                case.get("direct_sum_projection"), 1000))
        lines.append("")
    lines.extend((
        "## 判定上の注意", "",
        "- `image_cited_but_common_eligible` は **差し替え候補** であり、"
        "既存の証明から引用を削除してよいことの証明ではない。",
        "- [R] が root の祖先なら、現行 Proof Tree で使用中。"
        "表示だけで消さない。",
        "- (4.5) と DB prior は別の支持事実なので、Definition だけで代用しない。",
        "- 依存置換の採否は、次段階の最小修正と限定テストで確認する。",
        "",
    ))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", choices=("core", "all"), default="all")
    parser.add_argument("--allow-head-change", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    output = args.output.resolve()
    branch = git_output(root, "branch", "--show-current")
    head = git_output(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise SystemExit(f"AUDIT REFUSED: expected develop, got {branch}")
    if head != EXPECTED_HEAD and not args.allow_head_change:
        raise SystemExit(
            f"AUDIT REFUSED: develop HEAD moved ({head}); "
            "review current code first, then use --allow-head-change if appropriate"
        )
    initial = tracked_status(root)
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(root))
    cases = CORE_CASES if args.cases == "core" else ALL_CASES
    report: dict[str, Any] = {
        "phase": "169 R10ET-R1",
        "mode": "AUDIT_ONLY",
        "root": str(root),
        "branch": branch,
        "head": head,
        "expected_head": EXPECTED_HEAD,
        "head_matches_expected": head == EXPECTED_HEAD,
        "preexisting_tracked_status": initial,
        "cases": [],
        "full_pytest_run": False,
        "production_changed": [],
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        bridge = build_shared_typed_bridge()
        for n, k in cases:
            name = f"pi_{n+k}^{n}"
            print(f"R10ET_CASE_START={name}", flush=True)
            try:
                case = inspect_case(bridge, n, k, output)
            except Exception as exc:
                case = {
                    "group": name,
                    "n": n,
                    "k": k,
                    "status": "ERROR",
                    "trust": "ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            report["cases"].append(case)
            print(f"R10ET_{name}_STATUS={case.get('status')}", flush=True)
            print(f"R10ET_{name}_TRUST={case.get('trust')}", flush=True)
            if "image_cited_but_common_eligible" in case:
                print(
                    f"R10ET_{name}_CITED_COMMON_ELIGIBLE="
                    f"{case['image_cited_but_common_eligible']}", flush=True,
                )
    finally:
        final = tracked_status(root)
        report["post_tracked_status"] = final
        report["tracked_unchanged"] = initial == final
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output / "audit.md").write_text(markdown_report(report), encoding="utf-8")
        print(f"R10ET_REPORT={output / 'audit.md'}", flush=True)
        print(f"R10ET_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)

    successful = (
        report["tracked_unchanged"]
        and all(case.get("status") == "complete" and case.get("trust") == "PASS"
                for case in report["cases"])
    )
    print(f"R10ET_AUDIT={'PASS' if successful else 'REVIEW_REQUIRED'}", flush=True)
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
