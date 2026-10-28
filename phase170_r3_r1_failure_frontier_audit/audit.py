"""Reconcile R1/R2 evidence and inspect source eligibility for failed targets.

This does not execute backward search, alter a proof, create a theorem or
promote any unproved target to COMPLETE. Source screens are diagnostic only.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

REVIEWED_R1_HEAD = "790db364a8531693572fc510f969da831f1f9ffb"
REVIEWED_R2_HEAD = "f9e9a9d59970943d967e2cbcb0a98f13b2471407"
EXPECTED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r57_r16_web_proof_order.py": "b8760e932e90c9d71f398e37d8f405aec276d640",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
}
DATA_FILES = ("data/sphere.csv", "data/sphere_relation2.csv", "data/HyoujiGen.csv", "data/TBtable.csv")
TARGETS = ((3, 3), (4, 3), (5, 3), (4, 4), (5, 4))
ALL_CASES = ((2, 2), (3, 2), (4, 2), (2, 1), (3, 1), (4, 1),
             (3, 3), (4, 3), (5, 3), (4, 4), (5, 4), (8, 2))
ALLOWED_LATER_PREFIXES = ("phase170_r2_head_sync_r1/", "phase170_r2_database_utilization_audit/")


def git(root: Path, *arguments: str) -> bytes:
    process = subprocess.run(
        ("git", "-C", str(root), *arguments),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + " failed: "
            + process.stderr.decode("utf-8", errors="replace")
        )
    return process.stdout


def git_text(root: Path, *arguments: str) -> str:
    return git(root, *arguments).decode("utf-8", errors="strict").strip()


def tracked_snapshot(root: Path) -> dict[str, str]:
    return {
        "unstaged": git(root, "diff", "--raw", "-z").hex(),
        "staged": git(root, "diff", "--cached", "--raw", "-z").hex(),
        "index": git(root, "ls-files", "-s", "-z").hex(),
    }


def parse_name_status_z(raw: bytes) -> tuple[tuple[str, str], ...]:
    """Accept only the simple added-file NUL status format; reject renames."""
    parts = raw.decode("utf-8", errors="strict").split("\0")
    if parts and parts[-1] == "":
        parts.pop()
    if len(parts) % 2:
        raise ValueError("malformed git --name-status -z payload")
    return tuple((parts[i], parts[i + 1]) for i in range(0, len(parts), 2))


def allowed_later_files(changes: tuple[tuple[str, str], ...]) -> bool:
    """New R2 audit artifacts are allowed; changed production files are not."""
    return all(
        status == "A" and any(path.startswith(prefix) for prefix in ALLOWED_LATER_PREFIXES)
        and "/../" not in path and not path.endswith("/..")
        for status, path in changes
    )


def preflight(root: Path) -> dict[str, Any]:
    branch = git_text(root, "branch", "--show-current")
    head = git_text(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R3 requires develop branch")
    git(root, "merge-base", "--is-ancestor", REVIEWED_R2_HEAD, head)
    changes = parse_name_status_z(git(root, "diff", "--name-status", "-z", REVIEWED_R2_HEAD, head))
    if not allowed_later_files(changes):
        raise RuntimeError(f"unreviewed code change since R2: {changes!r}")
    observed = {}
    for relative, expected in EXPECTED_BLOBS.items():
        if not (root / relative).is_file():
            raise RuntimeError(f"missing reviewed production file {relative}")
        actual = git_text(root, "hash-object", "--", relative)
        if actual != expected:
            raise RuntimeError(f"reviewed production differs {relative}: {actual}")
        observed[relative] = actual
    for relative in DATA_FILES:
        # Do not interpret uncommitted CSV changes as the reviewed DB.
        if not (root / relative).is_file():
            raise RuntimeError(f"missing database {relative}")
        if git_text(root, "hash-object", "--", relative) != git_text(root, "rev-parse", f"HEAD:{relative}"):
            raise RuntimeError(f"uncommitted database edit: {relative}")
    return {"branch": branch, "head": head, "reviewed_blobs": observed,
            "allowed_added_committed_audit_files": list(changes)}


def load_reports(root: Path, r2_path: Path) -> tuple[dict, dict, dict[str, dict], dict[str, dict], Path]:
    if r2_path.name != "audit.json" or not r2_path.is_file():
        raise RuntimeError("R2 input must be a saved audit.json")
    r2 = json.loads(r2_path.read_text(encoding="utf-8"))
    if (r2.get("phase") != "170 R2" or r2.get("mode") != "AUDIT_ONLY"
            or r2.get("tracked_unchanged") is not True
            or r2.get("full_pytest_run") is not False or r2.get("audit_error")):
        raise RuntimeError("R2 report is not a completed read-only audit")
    if r2.get("git", {}).get("head") != REVIEWED_R2_HEAD:
        raise RuntimeError("R2 report is not based on reviewed production")
    r1_path = Path(r2.get("r1_report", "")).resolve()
    if not r1_path.is_file() or r1_path.name != "audit.json":
        raise RuntimeError("R2 points to a missing R1 audit.json")
    r1 = json.loads(r1_path.read_text(encoding="utf-8"))
    if (r1.get("phase") != "170 R1" or r1.get("mode") != "AUDIT_ONLY"
            or r1.get("git", {}).get("head") != REVIEWED_R1_HEAD
            or r1.get("tracked_unchanged") is not True
            or r1.get("full_pytest_run") is not False or r1.get("audit_error")):
        raise RuntimeError("R1 report is not a completed reviewed audit")
    git(root, "merge-base", "--is-ancestor", REVIEWED_R1_HEAD, REVIEWED_R2_HEAD)
    if r2.get("r1_source_transition", {}).get("kind") != "REVIEWED_R1_ONLY_COMMIT":
        raise RuntimeError("R2 did not certify R1-only HEAD transition")
    a = tuple(r1.get("cases", ()))
    b = tuple(r2.get("cases", ()))
    names = {f"pi_{n+k}^{n}" for n, k in ALL_CASES}
    if (len(a) != len(names) or len(b) != len(names)
            or {x.get("group") for x in a} != names
            or {x.get("group") for x in b} != names):
        raise RuntimeError("R1/R2 case samples are incomplete")
    r1_map = {x["group"]: x for x in a}
    r2_map = {x["group"]: x for x in b}
    for label in names:
        if r2_map[label].get("r1_status") != r1_map[label].get("status"):
            raise RuntimeError(f"R1/R2 status disagrees for {label}")
        if r1_map[label].get("classification") == "COMPLETE_TRUSTED":
            if r1_map[label].get("status") != "complete" or r1_map[label].get("trust") != "PASS":
                raise RuntimeError(f"complete/trust mismatch {label}")
    for n, k in TARGETS:
        label = f"pi_{n+k}^{n}"
        if r1_map[label].get("status") != "search_failed":
            raise RuntimeError(f"expected R1 search-failed sample: {label}")
        if r2_map[label].get("blocker_classification") != "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC":
            raise RuntimeError(f"expected R2 follow-up target missing: {label}")
    return r1, r2, r1_map, r2_map, r1_path


def load_trace(r1_path: Path, n: int, k: int, expected_steps: int) -> dict[str, Any]:
    """Use R1's serialized observed graph; never recreate unseen steps."""
    path = (r1_path.parent / f"pi{n+k}_{n}_trace.json").resolve()
    if path.parent != r1_path.parent.resolve() or not path.is_file():
        raise RuntimeError(f"missing per-group R1 trace: {path}")
    trace = json.loads(path.read_text(encoding="utf-8"))
    steps = trace.get("step_graph")
    if not isinstance(steps, list) or len(steps) != expected_steps:
        raise RuntimeError(f"R1 step count disagreement for pi_{n+k}^{n}")
    for i, step in enumerate(steps):
        if step.get("index") != i:
            raise RuntimeError(f"R1 trace has invalid step numbering at {i}")
        if not isinstance(step.get("premises"), list):
            raise RuntimeError(f"R1 trace has invalid premises at {i}")
        if any(type(x) is not int or x < 0 or x >= len(steps) for x in step["premises"]):
            raise RuntimeError(f"R1 trace has invalid dependency at {i}")
    return {"step_count": len(steps), "steps": steps,
            "root_index": trace.get("root_index"), "open_goals": trace.get("open_goals", []),
            "diagnostics": trace.get("diagnostics", []), "references": trace.get("references", [])}


def compact(value: object, max_length: int = 1800) -> str:
    rendered = repr(value)
    return rendered if len(rendered) <= max_length else rendered[:max_length] + " [TRUNCATED]"


def infer_frontier(r1: dict, r2: dict, citing_id: str | None) -> dict[str, Any]:
    """Classify what is *observed*, not what Toda mathematics lacks."""
    count = r2.get("selected_goal_count")
    if r2.get("selector_errors"):
        category = "GOAL_SELECTOR_EXCEPTION"
    elif count == 0:
        category = "GOAL_NOT_SELECTED"
    elif type(count) is int and count > 1:
        category = "GOAL_NOT_UNIQUE"
    elif count != 1:
        category = "GOAL_COUNT_UNVERIFIED"
    elif r1.get("status") == "search_failed":
        category = ("DERIVED_TARGET_SCREENING_AND_INFERENCE_UNRESOLVED"
                    if citing_id is None else "POSITIONED_TARGET_INFERENCE_UNRESOLVED")
    else:
        category = "SEARCH_STATUS_REVIEW_REQUIRED"
    return {
        "observed_category": category,
        "positioned_citing_assertion": citing_id is not None,
        "has_open_goals": bool(r1.get("open_goals")),
        "observed_proof_steps": r1.get("proof_step_count"),
        "mathematical_theorem_missing_certified": False,
        "renderer_only_defect_certified": False,
        "interpretation": (
            "A missing target citation ID does not invalidate an independently derived goal; "
            "source screening and typed inference remain separate questions."
        ),
    }


def inspect_source_screen(bridge: object, n: int, k: int) -> dict[str, Any]:
    """Inspect the real source-screen policy without running the prover."""
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from proof import ProofRule

    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    data: dict[str, Any] = {"typed_goal_count": len(candidates),
                            "typed_goals": [compact(x, 1800) for x in candidates],
                            "citation_ids": [], "source_screen_mode": "NOT_APPLICABLE",
                            "screened_link_count": None, "eligible_screened_fixed_count": None}
    for goal in candidates:
        data["citation_ids"].append(resolve_specialized_goal_citing_id(bridge, goal))
    if len(candidates) != 1:
        return data
    goal = candidates[0]
    citing_id = data["citation_ids"][0]
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        data["source_screen_mode"] = "INDEPENDENTLY_POSITIONED_DERIVED_TARGET"
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        data["source_screen_mode"] = "POSITIONED_CITING_ASSERTION"
    data["screened_link_count"] = len(screened.proof_links)
    fixed = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        entry = screened.registry.reference(assertion.reference_id)
        fixed.append({"assertion_id": assertion.assertion_id,
                      "locator": entry.locator,
                      "publication_position": entry.publication_position,
                      "content_type": type(assertion.content).__name__})
    data["eligible_screened_fixed_count"] = len(fixed)
    data["sample_screened_fixed_sources"] = fixed[:35]
    # These source candidates were screened, not used by a successful proof.
    data["screened_sources_are_proof_uses"] = False
    return data


def report_case(r1: dict, r2: dict, trace: dict, screen: dict) -> dict[str, Any]:
    if screen.get("typed_goal_count") != r2.get("selected_goal_count"):
        raise RuntimeError("live Goal selection differs from R2 recorded selection")
    citing_ids = screen.get("citation_ids", [])
    recorded_ids = [x.get("citing_assertion_id") for x in r2.get("selected_goal_citations", [])]
    if citing_ids != recorded_ids:
        raise RuntimeError("live citation resolution differs from R2 record")
    citing = citing_ids[0] if len(citing_ids) == 1 else None
    return {
        "group": r1["group"], "n": r1["n"], "k": r1["k"],
        "search_status": r1["status"], "r1_classification": r1["classification"],
        "r2_blocker_classification": r2["blocker_classification"],
        "r1_diagnostics_exact": r1.get("diagnostics", []),
        "r1_open_goals_exact": r1.get("open_goals", []),
        "r2_goal_source_classification": r2.get("goal_source_classification"),
        "r2_sphere_row_count": r2.get("direct_sphere_row_count"),
        "r2_relation_row_count": r2.get("relation_row_count"),
        "r2_bracket_row_count": r2.get("toda_bracket_row_count"),
        "r2_generator_id_gaps": r2.get("generator_reconstruction", {}).get("element_unknown_ids"),
        "r2_concrete_registry_assertions": r2.get("concrete_registry_assertions", []),
        "observed_graph": trace,
        "source_screen": screen,
        "frontier": infer_frontier(r1, r2, citing),
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 170 R3-R1 — 未完成証明の原因切り分け（読み取り専用）", "",
        "本監査は R1・R2 の保存済み観測と、現行の出典審査を突き合わせる。", 
        "探索は再実行せず、出典候補を証明済みの事実とみなさない。", "",
        f"- Git HEAD: `{report['git']['head']}`",
        f"- R1 report: `{report['r1_report']}`",
        f"- R2 report: `{report['r2_report']}`",
        f"- Git tracked/index unchanged: `{report['tracked_unchanged']}`",
        "- 全体 pytest: 未実行", "",
        "## 未完成5群", "",
        "| 群 | 分類 | typed Goal | Citation ID | 出典審査 | 審査済み候補数 | 証明Step |",
        "|---|---|---:|---|---|---:|---:|",
    ]
    for row in report.get("cases", []):
        s = row["source_screen"]
        ids = s["citation_ids"]
        lines.append(
            f"| `{row['group']}` | `{row['frontier']['observed_category']}` | "
            f"{s['typed_goal_count']} | `{ids}` | `{s['source_screen_mode']}` | "
            f"{s['eligible_screened_fixed_count']} | {row['observed_graph']['step_count']} |"
        )
    lines.extend(["", "## 未完成群の実測根拠", ""])
    for row in report.get("cases", []):
        lines.extend([
            f"### `{row['group']}`", "",
            f"- R1 診断（原文）: `{compact(row['r1_diagnostics_exact'], 2500)}`",
            f"- 未解決 Goal: `{compact(row['r1_open_goals_exact'], 2300)}`",
            f"- R2 Goal 選択源: `{row['r2_goal_source_classification']}`",
            f"- CSV 行数 sphere/relation/TodaBracket: `{row['r2_sphere_row_count']}`/`{row['r2_relation_row_count']}`/`{row['r2_bracket_row_count']}`",
            f"- HyoujiGen 未解決 ID: `{row['r2_generator_id_gaps']}`",
            f"- 現行出典スクリーン: `{row['source_screen']['source_screen_mode']}`",
            f"- 現行審査済み出典候補（実際の使用とは異なる）: `{row['source_screen']['eligible_screened_fixed_count']}`",
            f"- ProofStep（R1 実測）: `{row['observed_graph']['step_count']}`", "",
        ])
    lines.extend([
        "## 判定と次の工程", "",
        "- `SOURCE_ORDER_OR_CITATION_DIAGNOSTIC` は R1 の文字列診断から作られた分類で、掲載順違反の独立した証明ではない。",
        "- Goal に位置付き引用 ID が無くても、独立出典を使う合法的導出経路が存在し得る。",
        "- 審査済み出典候補数は文献命題の採用可能性であり、Proof Tree の証明成功を意味しない。",
        "- 残る未解決 Goal の推論規則不足を判断するには、出典・型・展開候補を別途検査する必要がある。",
        "- 本監査によって不足定理、新規実装の必要性、Renderer の欠陥を確定しない。",
        "- 新規規則追加・証明の complete 化・Git 操作・全体 pytest は行わない。", "",
    ])
    return "\n".join(lines)


def run(root: Path, r2_path: Path, output: Path) -> int:
    if not root.is_dir() or output.exists() or output == root or root in output.parents:
        raise RuntimeError("invalid root or output; audit outputs must be new and external")
    checked = preflight(root)
    r1, r2, r1_map, r2_map, r1_path = load_reports(root, r2_path)
    original = tracked_snapshot(root)
    output.mkdir(parents=True)
    sys.path.insert(0, str(root))
    report: dict[str, Any] = {
        "phase": "170 R3-R1", "mode": "AUDIT_ONLY",
        "git": checked, "r1_report": str(r1_path), "r2_report": str(r2_path),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "full_pytest_run": False, "production_modified": False, "cases": [],
        "verified_r1_complete_trusted": sum(
            x.get("status") == "complete" and x.get("trust") == "PASS"
            for x in r1_map.values()
        ),
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        bridge = build_shared_typed_bridge()
        for n, k in TARGETS:
            label = f"pi_{n+k}^{n}"
            try:
                trace = load_trace(r1_path, n, k, r1_map[label]["proof_step_count"])
                screened = inspect_source_screen(bridge, n, k)
                row = report_case(r1_map[label], r2_map[label], trace, screened)
            except Exception as exc:
                row = {"group": label, "error": f"{type(exc).__name__}: {exc}",
                       "traceback": traceback.format_exc()}
            report["cases"].append(row)
            tag = row.get("frontier", {}).get("observed_category", "AUDIT_ERROR")
            print(f"PHASE170_R3_{label}={tag}", flush=True)
    finally:
        report["tracked_unchanged"] = tracked_snapshot(root) == original
        report["review_required"] = any("error" in row for row in report["cases"])
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        try:
            content = (markdown(report) if not report["review_required"] else
                       "# Phase 170 R3-R1 監査エラー\n\n" + compact(report, 16000))
        except Exception as exc:
            content = f"# Report rendering error\n\n{type(exc).__name__}: {exc}\n"
        (output / "audit.md").write_text(content, encoding="utf-8")
        print(f"PHASE170_R3_REPORT={output / 'audit.md'}", flush=True)
        print(f"PHASE170_R3_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print("PHASE170_R3_FULL_PYTEST=False", flush=True)
    good = (report["tracked_unchanged"] and not report["review_required"]
            and len(report["cases"]) == len(TARGETS))
    print(f"PHASE170_R3_AUDIT_EXECUTION={'PASS' if good else 'REVIEW_REQUIRED'}", flush=True)
    return 0 if good else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--r2-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return run(args.root.resolve(), args.r2_report.resolve(), args.output.resolve())
    except Exception:
        print("PHASE170_R3_REFUSED=" + traceback.format_exc(), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
