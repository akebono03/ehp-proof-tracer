"""Phase 170 R1: read-only, current typed-search capability and evidence audit.

Only new report files outside the repository are written. No proof result is
silently promoted to COMPLETE. This script is diagnostic, not a proof checker.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

GITHUB_CURRENT_HEAD = "790db364a8531693572fc510f969da831f1f9ffb"
HANDOFF_HEAD = "83b1400d55890cea7b8ab44579c11e11f8dd8e69"
REVIEWED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
}
CORE_CASES = ((2, 2), (3, 2), (4, 2))
OTHER_STEM_CASES = ((2, 1), (3, 1), (4, 1), (3, 3), (4, 3), (5, 3), (4, 4), (5, 4), (8, 2))


def git(root: Path, *args: str, check: bool = True) -> bytes:
    p = subprocess.run(("git", "-C", str(root), *args), capture_output=True, check=False)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.decode('utf-8', errors='replace')}")
    return p.stdout


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).decode("utf-8", errors="replace").strip()


def tracked_snapshot(root: Path) -> dict[str, str]:
    return {
        "worktree_diff_raw": git(root, "diff", "--raw", "-z").hex(),
        "index_diff_raw": git(root, "diff", "--cached", "--raw", "-z").hex(),
        "index_entries": git(root, "ls-files", "-s", "-z").hex(),
    }


def preflight(root: Path) -> dict[str, Any]:
    if git_text(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R1 refuses any branch except develop")
    head = git_text(root, "rev-parse", "HEAD")
    # New unrelated commits are acceptable only after reviewing their code in
    # another R1 package. Fail closed rather than trust a moving implementation.
    if head not in (GITHUB_CURRENT_HEAD, HANDOFF_HEAD):
        raise RuntimeError(f"unreviewed HEAD {head}; audited heads are {GITHUB_CURRENT_HEAD} and {HANDOFF_HEAD}")
    observed = {}
    for relative, expected in REVIEWED_BLOBS.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"missing reviewed production source: {relative}")
        actual = git_text(root, "hash-object", "--", relative)
        if actual != expected:
            raise RuntimeError(f"reviewed production differs at {relative}: {actual} != {expected}")
        observed[relative] = actual
    return {"branch": "develop", "head": head,
            "matches_current_github_head": head == GITHUB_CURRENT_HEAD,
            "handoff_head_has_same_reviewed_production": head == HANDOFF_HEAD,
            "reviewed_production_blobs": observed}


def clipped(value: object, length: int = 1500) -> str:
    result = repr(value)
    return result if len(result) <= length else result[:length] + " [TRUNCATED]"


def same_integer_cell(cell: object, expected: int) -> bool:
    """Compare integer dimensions in both integer and spreadsheet '3.0' CSV forms."""
    try:
        from decimal import Decimal, InvalidOperation
        value = Decimal(str(cell).strip())
        return value.is_finite() and value == expected
    except (ValueError, TypeError, InvalidOperation):
        return False


def csv_info(root: Path, relative: str, n: int, k: int) -> dict[str, Any]:
    path = root / relative
    info: dict[str, Any] = {"path": relative, "exists": path.is_file(), "matches": [], "header": []}
    if not path.is_file():
        return info
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        info["header"] = reader.fieldnames or []
        if "n" in info["header"] and "k" in info["header"]:
            for row in reader:
                if same_integer_cell(row.get("n"), n) and same_integer_cell(row.get("k"), k):
                    info["matches"].append({name: str(value)[:300]
                                            for name, value in row.items() if name is not None})
    return info


def dataset_inventory(root: Path) -> dict[str, Any]:
    result = {}
    for name in ("sphere.csv", "sphere_relation2.csv", "HyoujiGen.csv", "TBtable.csv"):
        path = root / "data" / name
        row: dict[str, Any] = {"exists": path.is_file(), "rows": None, "headers": []}
        if path.is_file():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                row["headers"] = list(reader.fieldnames or ())
                row["rows"] = sum(1 for _ in reader)
        result[name] = row
    return result


def step_index(premise: object, steps: tuple[object, ...], ids: dict[int, int]) -> int | None:
    direct = ids.get(id(premise))
    if direct is not None:
        return direct
    matches = [j for j, step in enumerate(steps) if step == premise]
    return matches[0] if len(matches) == 1 else None


def step_graph(steps: tuple[object, ...], citation_numbers: tuple[tuple[int, ...], ...]) -> tuple[list[dict], list[str]]:
    ids = {id(item): i for i, item in enumerate(steps)}
    problems: list[str] = []
    if len(ids) != len(steps):
        problems.append("duplicate ProofStep identities")
    output = []
    for i, step in enumerate(steps):
        indices = [step_index(parent, steps, ids) for parent in step.premises]
        if any(index is None for index in indices):
            problems.append(f"step {i}: missing/ambiguous premise")
        source = getattr(step.inference_rule, "literature_reference", None)
        output.append({
            "index": i,
            "rule": getattr(step.rule, "name", str(step.rule)),
            "inference_rule": getattr(step.inference_rule, "name", None),
            "conclusion_type": type(step.conclusion).__name__,
            "conclusion": clipped(step.conclusion),
            "premises": indices,
            "source_locator": (getattr(source, "locator", None) or getattr(source, "label", None)),
            "citation_numbers": list(citation_numbers[i]) if i < len(citation_numbers) else [],
        })
    return output, problems


def classify(status: str, trust: str) -> str:
    if status == "complete" and trust == "PASS":
        return "COMPLETE_TRUSTED"
    if status == "complete":
        return "COMPLETE_NOT_CERTIFIED"
    if status in ("partial", "search_failed", "not_searched"):
        return status.upper()
    return "ERROR_OR_UNKNOWN"


def audit_case(bridge: object, root: Path, output: Path, n: int, k: int) -> dict[str, Any]:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model, root_ancestor_step_indices
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from proof import ProofRule

    label = f"pi_{n+k}^{n}"
    case = {"group": label, "n": n, "k": k,
            "sphere_db": csv_info(root, "data/sphere.csv", n, k),
            "relation_db": csv_info(root, "data/sphere_relation2.csv", n, k),
            "status": "NOT_RUN", "trust": "NOT_APPLICABLE", "errors": []}
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    zero = database_zero_group_goal_candidates(n=n, k=k)
    case["typed_goal_candidates"] = [clipped(x, 2400) for x in candidates]
    case["zero_goal_candidates"] = [clipped(x, 1400) for x in zero]
    contexts: list[object] = []
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge, context_sink=contexts.append)
    case.update({
        "status": result.status.value, "structure_status": result.structure_status.value,
        "conclusion": clipped(result.conclusion), "proof_step_count": len(result.proven_steps),
        "open_goals": [{"type": type(x).__name__, "value": clipped(x, 2000)} for x in result.open_goals],
        "diagnostics": list(result.diagnostics), "contexts": len(contexts),
        "search_references": list(result.references),
    })
    screened = contexts[-1] if contexts else None
    model = None
    try:
        model = (build_linked_proof_narrative_model(result, screened)
                 if screened is not None else build_proof_narrative_model(result))
    except Exception as exc:
        case["errors"].append(f"NARRATIVE_MODEL: {type(exc).__name__}: {exc}")
    if model is not None:
        steps, graph_problems = step_graph(tuple(model.steps), model.step_citation_numbers)
        case["step_graph"] = steps
        case["errors"].extend(graph_problems)
        case["root_index"] = model.root_index
        if result.status is ProofSearchStatus.COMPLETE and model.root_index is not None:
            try:
                scope = root_ancestor_step_indices(model.steps, model.root_index)
                case["root_reachable"] = sorted(scope)
                case["unreachable"] = sorted(set(range(len(model.steps))) - set(scope))
            except Exception as exc:
                case["errors"].append(f"ROOT_ANCESTRY: {type(exc).__name__}: {exc}")
        case["references"] = [{
            "number": cite.number,
            "locator": cite.reference.locator or cite.reference.label,
            "step_indices": list(cite.step_indices),
            "assertion_ids": list(cite.assertion_ids),
            "statement_bodies": list(cite.statement_bodies),
        } for cite in model.citations]
        for ref in case["references"]:
            reachable = case.get("root_reachable")
            ref["root_reachable"] = (None if reachable is None else
                                      all(i in reachable for i in ref["step_indices"]))
            ref["direct_given"] = any(
                model.steps[i].rule is ProofRule.GIVEN for i in ref["step_indices"]
            )
    else:
        case["step_graph"], problems = step_graph(tuple(result.proven_steps), ())
        case["errors"].extend(problems)
        case["references"] = []
    cited = [ref["locator"] for ref in case["references"]]
    case["db_rows_present"] = bool(case["sphere_db"]["matches"])
    case["db_prior_cited"] = any("sphere.csv" in str(locator) for locator in cited)
    case["toda_locators_cited"] = [locator for locator in cited if "sphere.csv" not in str(locator)]
    case["step_rules"] = dict(Counter(step["rule"] for step in case["step_graph"]))
    case["step_conclusion_types"] = dict(Counter(step["conclusion_type"] for step in case["step_graph"]))
    case["generator_image_steps"] = [step["index"] for step in case["step_graph"]
                                      if step["conclusion_type"] == "GeneratorImage"]
    case["stable_transport_steps"] = [step["index"] for step in case["step_graph"]
                                       if "suspension" in str(step["inference_rule"]).lower()
                                       or "toda45" in str(step["inference_rule"]).lower()]
    if result.status is ProofSearchStatus.COMPLETE:
        if screened is None or len(contexts) != 1:
            case["trust"] = "UNVERIFIABLE_NO_UNIQUE_SCREENED_CONTEXT"
        else:
            try:
                citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
                case["citing_assertion_id"] = citing
                inf, given = verify_proof_tree_for_narrative(
                    result, screened, citing_assertion_id=citing,
                    derived_target_without_citing_id=citing is None,
                )
                case["trust"] = "PASS"
                case["trust_inferences"] = inf
                case["trust_givens"] = given
            except Exception as exc:
                case["trust"] = "FAIL"
                case["errors"].append(f"TRUST: {type(exc).__name__}: {exc}")
    if model is not None:
        try:
            before = (tuple(id(x) for x in model.steps), model.step_citation_numbers)
            text = render_model_backed_narrative_markdown(result, model)
            after = (tuple(id(x) for x in model.steps), model.step_citation_numbers)
            if before != after:
                case["errors"].append("RENDERER_MUTATED_MODEL")
            if result.status is ProofSearchStatus.COMPLETE and case["trust"] == "PASS":
                case["public_narrative_complete_mark"] = text.rstrip().endswith("□")
            narrative = output / (f"pi{n+k}_{n}_narrative.md")
            narrative.write_text(text, encoding="utf-8")
            case["narrative_path"] = str(narrative)
            case["reference_headings_displayed"] = [f"**[R{ref['number']}]" in text
                                                    for ref in case["references"]]
        except Exception as exc:
            case["errors"].append(f"RENDER: {type(exc).__name__}: {exc}")
    case["classification"] = classify(case["status"], case["trust"])
    (output / (f"pi{n+k}_{n}_trace.json")).write_text(
        json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {key: value for key, value in case.items() if key != "step_graph"}


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 170 R1 — 現行証明能力・DB 活用状況 AUDIT_ONLY", "",
        f"- 実行 HEAD: `{report['git']['head']}`",
        f"- GitHub 確認 HEAD: `{GITHUB_CURRENT_HEAD}`",
        f"- 同一レビュー済み本体コード: `{report['git']['reviewed_production_blobs'] is not None}`",
        f"- 既存 tracked/index 維持: `{report.get('tracked_unchanged')}`",
        "- 全体 pytest: 実行していない", "",
        "## 探索・Trust の実測", "",
        "| 群 | stem | 探索 | Trust | Step | 未解決 | Reference | DB行 / 引用 |",
        "|---|---:|---|---|---:|---:|---:|---|",
    ]
    for x in report["cases"]:
        lines.append(f"| `{x['group']}` | {x['k']} | {x['status']} | {x['trust']} | "
                     f"{x.get('proof_step_count', 0)} | {len(x.get('open_goals', []))} | "
                     f"{len(x.get('references', []))} | "
                     f"{x.get('db_rows_present', False)} / {x.get('db_prior_cited', False)} |")
    lines.extend(["", "## 完成・未完成分布（調査対象だけ）", ""])
    for stem, counts in sorted(report["distribution"].items(), key=lambda item: int(item[0])):
        lines.append(f"- {stem}-stem: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    lines.extend(["", "## 個別の根拠と課題", ""])
    for x in report["cases"]:
        lines.extend([f"### `{x['group']}`", "",
                      f"- 分類: `{x['classification']}`",
                      f"- 結論: `{x.get('conclusion', '-')}`",
                      f"- Reference: " + "; ".join(ref["locator"] for ref in x.get("references", [])),
                      f"- 未解決 Goal: " + "; ".join(g["value"] for g in x.get("open_goals", [])),
                      f"- 診断: " + "; ".join(x.get("diagnostics", [])),
                      f"- 監査エラー: " + "; ".join(x.get("errors", [])), ""])
    lines.extend([
        "## 調査の限界", "",
        "stem 分布は列挙した標本だけ。未実行の DB 行・Goal を COMPLETE と評価しない。",
        "DB に行があることと、それが実際の証明で引用されたことを区別する。",
        "Trust の PASS は検査関数の実行結果であり、数学文献の無条件の真理保証ではない。",
        "R2 では未使用行・関係式・生成元の型付き接続を詳細に追跡する。", "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", choices=("core", "sample"), default="sample")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"Refuse overwriting an existing output folder: {output}")
    # Only allow output outside the version-controlled worktree.
    if output == root or root in output.parents:
        raise SystemExit("Audit output must be outside the repository")
    try:
        checked = preflight(root)
    except Exception as exc:
        print("PHASE170_R1_PREFLIGHT_REFUSED=" + str(exc), flush=True)
        return 2
    original = tracked_snapshot(root)
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(root))
    cases = CORE_CASES + (OTHER_STEM_CASES if args.scope == "sample" else ())
    report: dict[str, Any] = {
        "phase": "170 R1", "mode": "AUDIT_ONLY", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git": checked, "scope": args.scope, "cases": [], "dataset_inventory": {},
        "distribution": {}, "full_pytest_run": False, "production_changed": False,
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        report["dataset_inventory"] = dataset_inventory(root)
        bridge = build_shared_typed_bridge()
        registry = bridge.registry
        report["registry_counts"] = {
            "assertions": len(registry._assertions),
            "references": len(registry._references),
            "proof_links": len(bridge.proof_links),
        }
        for n, k in cases:
            label = f"pi_{n+k}^{n}"
            print(f"PHASE170_R1_CASE_START={label}", flush=True)
            try:
                case = audit_case(bridge, root, output, n, k)
            except Exception as exc:
                case = {"group": label, "n": n, "k": k, "status": "ERROR", "trust": "ERROR",
                        "classification": "ERROR_OR_UNKNOWN", "errors": [
                            f"{type(exc).__name__}: {exc}", traceback.format_exc()]}
            report["cases"].append(case)
            print(f"PHASE170_R1_{label}={case['classification']}", flush=True)
        distribution: dict[str, Counter] = {}
        for row in report["cases"]:
            distribution.setdefault(str(row["k"]), Counter())[row["classification"]] += 1
        report["distribution"] = {key: dict(counts) for key, counts in distribution.items()}
    except Exception as exc:
        report["audit_error"] = f"{type(exc).__name__}: {exc}"
        report["audit_traceback"] = traceback.format_exc()
    finally:
        report["tracked_unchanged"] = original == tracked_snapshot(root)
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "audit.md").write_text(markdown_report(report), encoding="utf-8")
        print(f"PHASE170_R1_REPORT={output / 'audit.md'}", flush=True)
        print(f"PHASE170_R1_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print("PHASE170_R1_FULL_PYTEST=False", flush=True)
    review_required = any(
        x.get("status") == "ERROR" or x.get("trust") == "FAIL"
        or x.get("errors") for x in report["cases"]
    )
    print(f"PHASE170_R1_REVIEW_REQUIRED={review_required}", flush=True)
    return 0 if (report["tracked_unchanged"] and not report.get("audit_error")
                 and not review_required) else 1


if __name__ == "__main__":
    raise SystemExit(main())
