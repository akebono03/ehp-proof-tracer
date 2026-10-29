"""Phase 170 R3-R4: read-only n=2 vertical-slice proof and Web audit.

No derived answer is promoted to a proof.  All production imports are isolated
inside child processes; the parent verifies reviewed sources and Git integrity.
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
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

REVIEWED_BASE_HEAD = "5a49800274157fa6b8e58aa7c372cee7d17e0195"
REVIEWED_BLOBS = {
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r3_recursive_search.py": "9c424f61a2b4a2d7789777017ad4f91292b0ad30",
    "phase165_r52_r3_web_adapter.py": "aefdc5527aeec7bcb7ffe77f69b754a39f3a242b",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
}
# Only additions to isolated Phase 170 audit folders are acceptable past base.
ADDED_AUDIT_PATH = re.compile(r"^phase170_[a-z0-9_]+/(?:[a-zA-Z0-9_.\-/]+)$")
GROUP_SPHERE = 2
DEFAULT_MIN_K = 3
DEFAULT_MAX_K = 10


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(("git", "-C", str(root), *args), capture_output=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} exited {result.returncode}: "
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).stdout.decode("utf-8", errors="replace").strip()


def snapshot(root: Path) -> dict[str, str]:
    return {
        "head": git_text(root, "rev-parse", "HEAD"),
        "unstaged": git(root, "diff", "--raw", "-z").stdout.hex(),
        "staged": git(root, "diff", "--cached", "--raw", "-z").stdout.hex(),
        "index": git(root, "ls-files", "-s", "-z").stdout.hex(),
    }


def parse_changes_z(raw: bytes) -> tuple[tuple[str, str], ...]:
    """Require ordinary A/M/D status records; reject rename/copy ambiguity."""
    parts = raw.decode("utf-8", errors="strict").split("\x00")
    if not parts or parts[-1] != "":
        raise RuntimeError("malformed NUL-terminated Git diff")
    values = parts[:-1]
    if len(values) % 2:
        raise RuntimeError("malformed Git --name-status pair count")
    result = []
    for i in range(0, len(values), 2):
        status, path = values[i], values[i + 1]
        if not status or not path:
            raise RuntimeError("empty Git diff record")
        result.append((status, path))
    return tuple(result)


def acceptable_added_audit_changes(changes: tuple[tuple[str, str], ...]) -> bool:
    return all(status == "A" and ADDED_AUDIT_PATH.fullmatch(path) is not None
               and ".." not in Path(path).parts
               for status, path in changes)


def preflight(root: Path) -> dict[str, Any]:
    if not root.is_dir():
        raise RuntimeError("repository directory not found")
    branch = git_text(root, "branch", "--show-current")
    head = git_text(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"reviewed branch is develop, not {branch!r}")
    # Accept subsequent audit-only commits after the reviewed base, but never
    # production changes, DB changes, modified audits or unrelated additions.
    git(root, "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head)
    changes = parse_changes_z(git(
        root, "diff", "--name-status", "-z", REVIEWED_BASE_HEAD, head
    ).stdout) if head != REVIEWED_BASE_HEAD else ()
    if not acceptable_added_audit_changes(changes):
        raise RuntimeError(f"unreviewed committed changes: {changes!r}")
    if git(root, "diff", "--quiet", check=False).returncode != 0:
        raise RuntimeError("tracked working tree is dirty")
    if git(root, "diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("Git index is dirty")
    for relative, expected in REVIEWED_BLOBS.items():
        if not expected:
            raise RuntimeError(f"unreviewed blob fixture missing: {relative}")
        if not (root / relative).is_file():
            raise RuntimeError(f"reviewed file missing: {relative}")
        actual = git_text(root, "hash-object", "--", relative)
        if actual != expected:
            raise RuntimeError(f"reviewed file changed: {relative} {actual}")
    return {
        "branch": branch, "head": head, "base_head": REVIEWED_BASE_HEAD,
        "reviewed_audit_file_additions": len(changes),
        "reviewed_blobs": REVIEWED_BLOBS,
    }


def cell_is_int(cell: object, number: int) -> bool:
    try:
        value = Decimal(str(cell).strip())
        return value.is_finite() and value == number
    except (InvalidOperation, ValueError, TypeError):
        return False


def inventory_n2_rows(root: Path, k: int) -> list[dict[str, str]]:
    """Read explicit rows; do not derive group structure from their metadata."""
    path = root / "data" / "sphere.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"k", "n", "orders", "generator"}.issubset(reader.fieldnames):
            raise RuntimeError("sphere.csv required column missing")
        result = []
        for row in reader:
            if cell_is_int(row.get("n"), GROUP_SPHERE) and cell_is_int(row.get("k"), k):
                result.append({name: str(row.get(name, ""))
                               for name in ("k", "n", "id", "orders", "generator", "Element", "gen_coe", "hyouji")})
    return result


def clipped(value: object, limit: int = 2200) -> str:
    raw = repr(value)
    if len(raw) > limit:
        return raw[:limit] + " [TRUNCATED]"
    return raw


def web_line_text(view: object) -> str:
    """Store safe text representations, not an invented reformatted proof."""
    lines = []
    for item in getattr(view, "rendered_lines", ()):  # exact public view data
        lines.append(clipped(item, 900))
    return "\n".join(lines[:80])


def outcome_class(case: dict[str, Any]) -> str:
    if "error" in case:
        return "CASE_ERROR"
    if case.get("search_status") == "complete":
        if (case.get("web", {}).get("route") == "standard_web_public_trust_gated"
                and case.get("web", {}).get("partial_result") is False
                and case.get("web", {}).get("key") == "generic-complete-proof"):
            return "COMPLETE_AND_WEB_VERIFIED"
        return "SEARCH_COMPLETE_WEB_NOT_VERIFIED"
    if case.get("web", {}).get("error"):
        return "SEARCH_INCOMPLETE_AND_RENDER_ERROR"
    if not case.get("db_rows"):
        return "NO_EXPLICIT_DB_ROW"
    if case.get("typed_goal_count", 0) != 1:
        return "TYPED_GOAL_SELECTION_UNRESOLVED"
    if case.get("search_status") in ("search_failed", "partial", "not_searched"):
        return "GOAL_AVAILABLE_PROOF_UNFINISHED"
    return "INSPECTION_INCONCLUSIVE"


def run_one_child(root: Path, n: int, k: int) -> dict[str, Any]:
    """Observe search and its existing Web model adapter; never create proof."""
    sys.path.insert(0, str(root))
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates, database_group_goal_candidates
    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    structured = database_structured_group_goal_candidates(n=n, k=k)
    simple = database_group_goal_candidates(n=n, k=k)
    zero = database_zero_group_goal_candidates(n=n, k=k)
    case: dict[str, Any] = {
        "group": f"pi_{n+k}^{n}", "n": n, "k": k,
        "db_rows": inventory_n2_rows(root, k),
        "typed_goal_count": len(zero) if zero else len(candidates),
        "typed_goal_repr": [clipped(x, 2500) for x in (zero if zero else candidates)],
        "structured_goal_count": len(structured),
        "simple_goal_count": len(simple),
        "zero_goal_count": len(zero),
        "source_assertion_id": (resolve_specialized_goal_citing_id(bridge, candidates[0])
                                if len(candidates) == 1 else None),
    }
    contexts: list[Any] = []
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge, context_sink=contexts.append)
    case["search_status"] = result.status.value
    case["proven_step_count"] = len(result.proven_steps)
    case["open_goals"] = [{"kind": type(x).__name__, "repr": clipped(x, 2100)} for x in result.open_goals[:40]]
    case["open_goals_total"] = len(result.open_goals)
    case["diagnostics"] = [str(x) for x in result.diagnostics]
    case["conclusion"] = clipped(result.conclusion, 3000) if result.conclusion is not None else None
    case["screened_context_count"] = len(contexts)
    if result.status is ProofSearchStatus.COMPLETE:
        # The public entry repeats the search but additionally gates COMPLETE
        # against the unchanged Trust Boundary. Do not bypass this for success.
        from web_group_proof import build_standard_web_group_proof_view
        try:
            view = build_standard_web_group_proof_view(
                n=n, k=k, max_depth=2, mode="narrative", citation_source="model"
            )
            case["web"] = {"route": "standard_web_public_trust_gated",
                           "key": view.key, "partial_result": view.partial_result,
                           "statement": view.conclusion_latex,
                           "rendered_lines": len(view.rendered_lines),
                           "narrative_excerpt": web_line_text(view)}
        except Exception as exc:
            case["web"] = {"route": "standard_web_public_trust_gated",
                           "error": f"{type(exc).__name__}: {exc}"}
    else:
        # Exactly the same model and adapter that the standard Web entry uses
        # for incomplete results; no second search, no proof gate claim.
        try:
            model_bridge = contexts[-1] if contexts else bridge
            model = build_linked_proof_narrative_model(result, model_bridge)
            view = build_partial_web_group_proof_view(
                result, max_depth=2, mode="narrative", narrative_model=model
            )
            case["web"] = {"route": "public_partial_model_adapter",
                           "key": view.key, "partial_result": view.partial_result,
                           "statement": view.conclusion_latex,
                           "rendered_lines": len(view.rendered_lines),
                           "narrative_excerpt": web_line_text(view)}
        except Exception as exc:
            case["web"] = {"route": "public_partial_model_adapter",
                           "error": f"{type(exc).__name__}: {exc}"}
    case["outcome"] = outcome_class(case)
    return case


def execute_child(root: Path, k: int, seconds: int) -> dict[str, Any]:
    command = (sys.executable, "-B", str(Path(__file__).resolve()),
               "--child-root", str(root), "--child-k", str(k))
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        finished = subprocess.run(command, cwd=root, capture_output=True, encoding="utf-8",
                                  errors="replace", timeout=seconds, env=env, check=False)
    except subprocess.TimeoutExpired:
        return {"group": f"pi_{GROUP_SPHERE+k}^{GROUP_SPHERE}", "n": GROUP_SPHERE,
                "k": k, "error": f"case exceeded bounded audit limit ({seconds}s)",
                "outcome": "CASE_ERROR"}
    marker = "PHASE170_R3R4_CASE_JSON="
    payloads = [line[len(marker):] for line in finished.stdout.splitlines()
                if line.startswith(marker)]
    if finished.returncode != 0 or len(payloads) != 1:
        return {"group": f"pi_{GROUP_SPHERE+k}^{GROUP_SPHERE}", "n": GROUP_SPHERE,
                "k": k, "error": "child failed or did not return exactly one result",
                "return_code": finished.returncode,
                "stderr_tail": finished.stderr[-5000:], "stdout_tail": finished.stdout[-3000:],
                "outcome": "CASE_ERROR"}
    try:
        result = json.loads(payloads[0])
        if result.get("n") != GROUP_SPHERE or result.get("k") != k:
            raise ValueError("wrong group in child result")
        return result
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return {"group": f"pi_{GROUP_SPHERE+k}^{GROUP_SPHERE}", "n": GROUP_SPHERE,
                "k": k, "error": f"invalid child result: {exc}", "outcome": "CASE_ERROR"}


def to_markdown(report: dict[str, Any]) -> str:
    out = ["# Phase 170 R3-R4 — n=2 連続群 証明・表示監査", "",
           "現行 DB・型付き Goal・Proof Tree・Web model の経路を同じ条件で監査した。",
           "DB に登録された群構造は証明ではない。未完成も数学的証明不能を意味しない。", "",
           f"Git HEAD: `{report['git']['head']}`", "全体 pytest: 未実行", "",
           "## 群ごとの結果", ""]
    for case in report.get("cases", []):
        out.append(f"### `{case['group']}`")
        out.append("")
        out.append(f"- 評価: `{case.get('outcome', 'UNKNOWN')}`")
        if "error" in case:
            out.append(f"- 監査エラー: `{case['error']}`")
            out.append("")
            continue
        out.append("- DB に記録された構造: " + "; ".join(
            f"order={row['orders']}, generator={row['generator']}" for row in case.get("db_rows", [])))
        out.append(f"- 型付き Goal 候補: {case['typed_goal_count']} 件（structured: {case['structured_goal_count']}、simple: {case['simple_goal_count']}、zero: {case['zero_goal_count']}）")
        out.append(f"- Citation ID: `{case['source_assertion_id']}`")
        out.append(f"- Search: `{case['search_status']}`、確定 ProofStep: {case['proven_step_count']} 件")
        out.append(f"- Web: `{case.get('web', {}).get('key')}`、partial={case.get('web', {}).get('partial_result')}")
        if case.get("web", {}).get("error"):
            out.append(f"- Web 変換エラー: `{case['web']['error']}`")
        for g in case.get("open_goals", [])[:12]:
            out.append(f"- 未解決 `{g['kind']}`: `{g['repr']}`")
        for diagnostic in case.get("diagnostics", []):
            out.append(f"- 診断: `{diagnostic}`")
        out.append("")
    out.extend(["## 判定の境界", "",
                "- `COMPLETE_AND_WEB_VERIFIED` のみ完成表示が本番公開経路で検証されたことを表す。",
                "- `GOAL_AVAILABLE_PROOF_UNFINISHED` は既知の群構造と完成した証明を混同しない。",
                "- 前提・引用・推論不足の根本原因は必要に応じて次回の監査で特定する。",
                "- この監査は production / test / DB / Git の追跡対象を変更しない。", ""])
    return "\n".join(out)


def run(root: Path, output: Path, minimum: int, maximum: int, seconds: int) -> int:
    if not (3 <= minimum <= maximum <= 20):
        raise RuntimeError("expected 3 <= min-k <= max-k <= 20")
    if not (30 <= seconds <= 600):
        raise RuntimeError("expected case-seconds between 30 and 600")
    if output.exists() or root == output or root in output.parents:
        raise RuntimeError("refusing existing output or repository-internal output")
    pre = preflight(root)
    before = snapshot(root)
    output.mkdir(parents=True, exist_ok=False)
    report: dict[str, Any] = {
        "phase": "170 R3-R4", "mode": "AUDIT_ONLY", "git": pre,
        "utc": datetime.now(timezone.utc).isoformat(),
        "n": GROUP_SPHERE, "min_k": minimum, "max_k": maximum,
        "full_pytest_run": False, "production_changed": False,
        "cases": [], "tracked_unchanged": False, "review_required": True,
    }
    for k in range(minimum, maximum + 1):
        label = f"pi_{GROUP_SPHERE+k}^{GROUP_SPHERE}"
        print(f"PHASE170_R3R4_CASE_START={label}", flush=True)
        case = execute_child(root, k, seconds)
        report["cases"].append(case)
        print(f"PHASE170_R3R4_{label}={case.get('outcome', 'CASE_ERROR')}", flush=True)
    report["tracked_unchanged"] = snapshot(root) == before
    report["review_required"] = (not report["tracked_unchanged"]
                                 or any(x.get("outcome") == "CASE_ERROR" for x in report["cases"]))
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "audit.md").write_text(to_markdown(report), encoding="utf-8")
    print(f"PHASE170_R3R4_REPORT={output / 'audit.md'}", flush=True)
    print(f"PHASE170_R3R4_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
    print("PHASE170_R3R4_FULL_PYTEST=False", flush=True)
    print(f"PHASE170_R3R4_REVIEW_REQUIRED={report['review_required']}", flush=True)
    print(f"PHASE170_R3R4_AUDIT_EXECUTION={'REVIEW' if report['review_required'] else 'PASS'}", flush=True)
    return 1 if report["review_required"] else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-k", type=int, default=DEFAULT_MIN_K)
    parser.add_argument("--max-k", type=int, default=DEFAULT_MAX_K)
    parser.add_argument("--case-seconds", type=int, default=180)
    parser.add_argument("--child-root", type=Path)
    parser.add_argument("--child-k", type=int)
    args = parser.parse_args(argv)
    if args.child_root is not None:
        if args.child_k is None:
            parser.error("child-k is required with child-root")
        try:
            result = run_one_child(args.child_root.resolve(), GROUP_SPHERE, args.child_k)
            print("PHASE170_R3R4_CASE_JSON=" + json.dumps(result, ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 2
    if args.root is None or args.output is None:
        parser.error("root and output are required")
    try:
        return run(args.root.resolve(), args.output.resolve(), args.min_k, args.max_k, args.case_seconds)
    except Exception:
        print("PHASE170_R3R4_REFUSED=" + traceback.format_exc(), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
