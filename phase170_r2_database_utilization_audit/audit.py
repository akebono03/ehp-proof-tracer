"""Phase 170 R2: inspect database-to-Goal and used-proof paths without mutations.

R1 already executed the real searches. R2 reuses their recorded proof traces, and
queries only the current read-only typed Goal conversion and registry interfaces.
Never treat a CSV row, an unmatched claim, or a search failure as a proof.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

EXPECTED_HEADS = frozenset({
    "790db364a8531693572fc510f969da831f1f9ffb",
    "83b1400d55890cea7b8ab44579c11e11f8dd8e69",
})
REVIEWED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
}
DATASETS = ("sphere.csv", "sphere_relation2.csv", "HyoujiGen.csv", "TBtable.csv")
R1_GROUPS = (
    (2, 2), (3, 2), (4, 2), (2, 1), (3, 1), (4, 1),
    (3, 3), (4, 3), (5, 3), (4, 4), (5, 4), (8, 2),
)


def git(root: Path, *args: str) -> bytes:
    process = subprocess.run(
        ("git", "-C", str(root), *args),
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(f"git {args} failed: {process.stderr.decode('utf-8', 'replace')}")
    return process.stdout


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).decode("utf-8", "replace").strip()


def snapshot(root: Path) -> dict[str, str]:
    return {
        "tracked_unstaged_raw": git(root, "diff", "--raw", "-z").hex(),
        "tracked_staged_raw": git(root, "diff", "--cached", "--raw", "-z").hex(),
        "index_records": git(root, "ls-files", "-s", "-z").hex(),
    }


def preflight(root: Path) -> dict[str, Any]:
    branch = git_text(root, "branch", "--show-current")
    head = git_text(root, "rev-parse", "HEAD")
    if branch != "develop" or head not in EXPECTED_HEADS:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch!r} {head}")
    observed = {}
    for name, expected in REVIEWED_BLOBS.items():
        if not (root / name).is_file():
            raise RuntimeError(f"missing reviewed production file: {name}")
        actual = git_text(root, "hash-object", "--", name)
        if actual != expected:
            raise RuntimeError(f"unreviewed source: {name} {actual} expected {expected}")
        observed[name] = actual
    return {"branch": branch, "head": head, "source_blobs": observed}


def number_is(cell: object, expected: int) -> bool:
    """Allow 3 and 3.0, but not malformed or nonfinite dimensions."""
    try:
        value = Decimal(str(cell).strip())
        return value.is_finite() and value == expected
    except (InvalidOperation, ValueError, TypeError):
        return False


def read_rows(root: Path, name: str) -> tuple[list[str], list[dict[str, str]]]:
    path = root / "data" / name
    if not path.is_file():
        return [], []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [
            {str(key): "" if value is None else str(value) for key, value in row.items()
             if key is not None}
            for row in reader
        ]
        return list(reader.fieldnames or []), rows


def exact_rows(rows: list[dict[str, str]], n: int, k: int) -> list[dict[str, str]]:
    return [x for x in rows if number_is(x.get("n"), n) and number_is(x.get("k"), k)]


def parse_element_ids(raw: object) -> tuple[int, ...] | None:
    """Read simple whitespace/comma-separated Element IDs; never parse expressions."""
    value = str(raw or "").strip()
    if not value:
        return ()
    parts = value.replace(",", " ").split()
    if any(re.fullmatch(r"[0-9]+", part) is None for part in parts):
        return None
    return tuple(int(part) for part in parts)


def generator_diagnostics(sphere_rows: list[dict[str, str]], gen_rows: list[dict[str, str]]) -> dict[str, Any]:
    ids = {int(x["id"]) for x in gen_rows if re.fullmatch(r"[0-9]+", x.get("id", ""))}
    used: set[int] = set()
    malformed = []
    missing: set[int] = set()
    for i, row in enumerate(sphere_rows):
        tokens = parse_element_ids(row.get("Element"))
        if tokens is None:
            malformed.append({"row_index": i, "raw": row.get("Element", "")[:200]})
            continue
        used.update(tokens)
        missing.update(item for item in tokens if item not in ids)
    return {
        "element_referenced_ids": sorted(used),
        "element_unknown_ids": sorted(missing),
        "element_non_integer_rows": malformed,
        "hyoujigen_registered_ids": len(ids),
    }


def compact(value: Any, limit: int = 1300) -> str:
    string = repr(value)
    return string if len(string) <= limit else string[:limit] + " [TRUNCATED]"


def reason_category(case: dict[str, Any]) -> str:
    """Classify observed blockers only; never diagnose a missing theorem from a guess."""
    if case.get("r1_status") == "complete":
        return "COMPLETE_RECORDED"
    if case.get("selector_errors"):
        return "SELECTOR_EXCEPTION_UNDETERMINED"
    if case.get("r1_status") in ("ERROR", None):
        return "AUDIT_OR_SOURCE_UNAVAILABLE"
    diag = " ".join(str(x) for x in case.get("r1_diagnostics", ()))
    if case.get("selected_goal_count", 0) == 0:
        return "NO_TYPED_GOAL_CANDIDATE"
    if case.get("selected_goal_count", 0) > 1:
        return "AMBIGUOUS_TYPED_GOAL"
    if case.get("r1_status") == "search_failed" and any(
        keyword in diag for keyword in ("掲載順", "publication", "引用", "citation", "order", "位置")
    ):
        return "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC"
    if case.get("r1_status") in ("search_failed", "partial"):
        return "GOAL_EXISTS_SEARCH_OR_PREMISE_UNRESOLVED"
    return "OTHER_UNFINISHED"


def load_r1(root: Path, report_path: Path, current_head: str) -> tuple[dict, dict]:
    # R1 report is an input record, never a source of executable instructions.
    if report_path.name != "audit.json" or not report_path.is_file():
        raise RuntimeError("R1 report must be an existing audit.json")
    data = json.loads(report_path.read_text(encoding="utf-8"))
    if data.get("phase") != "170 R1" or data.get("mode") != "AUDIT_ONLY":
        raise RuntimeError("R1 report identity is invalid")
    if data.get("git", {}).get("head") != current_head:
        raise RuntimeError("R1 HEAD differs from audited current source")
    if data.get("tracked_unchanged") is not True or data.get("full_pytest_run") is not False:
        raise RuntimeError("R1 protection flags are not verified")
    if data.get("audit_error") or data.get("scope") != "sample":
        raise RuntimeError("R1 full sample did not finish")
    index = {x.get("group"): x for x in data.get("cases", ())}
    required = {f"pi_{n+k}^{n}" for n, k in R1_GROUPS}
    if set(index) != required or len(data.get("cases", ())) != len(required):
        raise RuntimeError("R1 group sample is incomplete or duplicated")
    return data, index


def case_evidence(bridge: object, n: int, k: int, r1: dict, datasets: dict) -> dict:
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3af_goal_adapter import database_group_goal_candidates, database_zero_group_goal_candidates
    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import Relation
    from unified_statement_registry import AssertionOrigin

    selector_errors: list[dict[str, str]] = []

    def guarded(name: str, selector: Any) -> tuple[Any, ...]:
        try:
            result = selector()
            if not isinstance(result, tuple):
                raise TypeError("typed selector must return a tuple")
            return result
        except Exception as exc:
            selector_errors.append({"selector": name, "error": f"{type(exc).__name__}: {exc}"})
            return ()

    selected = guarded("production_goal_selector", lambda: registered_group_goal_candidates(bridge, n=n, k=k))
    zeros = guarded("zero_group_DB", lambda: database_zero_group_goal_candidates(n=n, k=k))
    standard = guarded("simple_group_DB", lambda: database_group_goal_candidates(n=n, k=k))
    structured = guarded("structured_group_DB", lambda: database_structured_group_goal_candidates(n=n, k=k))
    direct = exact_rows(datasets["sphere.csv"]["rows"], n, k)
    base_n = k + 2 if n >= k + 2 else None
    stable_base = (exact_rows(datasets["sphere.csv"]["rows"], base_n, k)
                   if base_n is not None and base_n != n else [])
    relation_rows = exact_rows(datasets["sphere_relation2.csv"]["rows"], n, k)
    tb_rows = exact_rows(datasets["TBtable.csv"]["rows"], n, k)
    gen_source = direct or stable_base
    gen_evidence = generator_diagnostics(gen_source, datasets["HyoujiGen.csv"]["rows"])

    target_assertions = []
    for entry in bridge.registry._assertions.values():
        statement = entry.content
        if not isinstance(statement, Relation):
            continue
        lhs = statement.lhs
        if (getattr(lhs, "sphere_dimension", None) != n
                or getattr(lhs, "group_dimension", None) != n + k):
            continue
        ref = bridge.registry.reference(entry.reference_id)
        target_assertions.append({
            "assertion_id": entry.assertion_id,
            "origin": getattr(entry.origin, "value", str(entry.origin)),
            "locator": ref.locator,
            "publication_position": ref.publication_position,
            "component_position": entry.component_position,
            "typed_content": compact(statement, 1000),
        })

    citations = list(r1.get("references", []))
    selected_goal_cites = []
    for goal in selected:
        try:
            cite = resolve_specialized_goal_citing_id(bridge, goal)
        except Exception as exc:
            selector_errors.append({
                "selector": "resolve_specialized_goal_citing_id",
                "error": f"{type(exc).__name__}: {exc}",
            })
            cite = None
        selected_goal_cites.append({
            "goal": compact(goal, 1700),
            "citing_assertion_id": cite,
        })
    if len(zeros) == 1:
        selected_kind = "explicit_or_stable_db_zero"
    elif len(selected) == 1:
        selected_kind = (
            "structured_generator_DB" if len(structured) == 1 else
            "simple_DB" if len(standard) == 1 else
            "registered_or_specialized_claim"
        )
    elif len(selected) > 1:
        selected_kind = "ambiguous_candidates"
    else:
        selected_kind = "no_candidate"
    actual_used = {
        "reference_locators": [x.get("locator") for x in citations],
        "reference_count": len(citations),
        "db_prior_reference_used": any("DB prior: sphere.csv" in str(x.get("locator")) for x in citations),
        "toda_45_reference_used": any(x.get("locator") == "(4.5)" for x in citations),
        "related_relation_database_citation": any("sphere_relation2.csv" in str(x.get("locator")) for x in citations),
        "recorded_proof_steps": r1.get("proof_step_count", 0),
        "recorded_trust": r1.get("trust"),
    }
    result = {
        "group": f"pi_{n+k}^{n}", "n": n, "k": k,
        "r1_status": r1.get("status"), "r1_classification": r1.get("classification"),
        "r1_open_goals": r1.get("open_goals", []),
        "r1_diagnostics": r1.get("diagnostics", []),
        "r1_errors": r1.get("errors", []),
        "selected_goal_count": len(selected), "zero_goal_count": len(zeros),
        "simple_db_goal_count": len(standard),
        "structured_db_goal_count": len(structured),
        "goal_source_classification": selected_kind,
        "selected_goal_citations": selected_goal_cites,
        "selector_errors": selector_errors,
        "direct_sphere_row_count": len(direct),
        "stable_base": None if base_n is None else {"n": base_n, "k": k, "row_count": len(stable_base)},
        "relation_row_count": len(relation_rows),
        "toda_bracket_row_count": len(tb_rows),
        "sphere_rows": direct[:20],
        "relation_rows": relation_rows[:20],
        "generator_reconstruction": gen_evidence,
        "concrete_registry_assertions": target_assertions[:30],
        "concrete_registry_assertion_count": len(target_assertions),
        "fixed_concrete_assertion_count": sum(
            entry["origin"] == AssertionOrigin.FIXED_STATEMENT.value
            for entry in target_assertions
        ),
        "observed_proof_use": actual_used,
    }
    result["blocker_classification"] = reason_category(result)
    return result


def markdown(report: dict) -> str:
    lines = [
        "# Phase 170 R2 — DB 活用状況の読み取り専用監査", "",
        f"- HEAD: `{report['git']['head']}`",
        f"- R1 報告: `{report['r1_report']}`",
        f"- 既存 tracked/index 保全: `{report['tracked_unchanged']}`",
        "- 既存テスト・本体修正なし、全体 pytest 未実行", "",
        "## データセット実数", "",
        "| データセット | CSV 行数 | n,k列 |",
        "|---|---:|---|",
    ]
    for name, data in report["datasets"].items():
        cols = ", ".join(x for x in ("n", "k") if x in data["headers"])
        lines.append(f"| `{name}` | {data['rows']} | {cols or 'なし'} |")
    lines += ["", "## 12群における DB → Goal → 証明利用", "",
              "| 群 | R1 状態 | sphere行 | 関係式行 | typed Goal（構造/簡易/zero/採用） | DB prior実引用 | R2 分類 |",
              "|---|---|---:|---:|---|---|---|"]
    for x in report["cases"]:
        counts = "{}/{}/{}/{}".format(
            x["structured_db_goal_count"], x["simple_db_goal_count"],
            x["zero_goal_count"], x["selected_goal_count"],
        )
        lines.append(
            f"| `{x['group']}` | `{x['r1_status']}` | {x['direct_sphere_row_count']} | "
            f"{x['relation_row_count']} | {counts} | "
            f"{x['observed_proof_use']['db_prior_reference_used']} | `{x['blocker_classification']}` |"
        )
    lines += ["", "## 失敗群の診断根拠", ""]
    for x in report["cases"]:
        if x["r1_status"] == "complete":
            continue
        lines += [f"### `{x['group']}`", "",
                  f"- R1: `{x['r1_classification']}` / R2: `{x['blocker_classification']}`",
                  f"- Goal 選択: `{x['goal_source_classification']}`, 件数 `{x['selected_goal_count']}`",
                  f"- sphere 行/安定基底: `{x['direct_sphere_row_count']}` / `{x['stable_base']}`",
                  f"- relation 行: `{x['relation_row_count']}`",
                  f"- HyoujiGen 参照未登録 ID: `{x['generator_reconstruction']['element_unknown_ids']}`",
                  f"- R1 診断: `{compact(x['r1_diagnostics'], 1300)}`",
                  f"- R1 未解決 Goal: `{compact(x['r1_open_goals'], 1500)}`",
                  f"- R1 errors: `{compact(x['r1_errors'], 900)}`",
                  f"- Goal/DB 変換器の例外: `{compact(x['selector_errors'], 900)}`", ""]
    lines += ["## 限界・次の段階", "",
              "`selected_goal_count` は正式な本番 Goal 選択器の返値であり、数学的証明ではありません。",
              "`sphere.csv` の存在や `HyoujiGen.csv` の ID 解決可能性は、証明根拠としての引用資格を与えません。",
              "DB prior の実引用は R1 に記録された Reference から判定し、未参照データを使用済みと扱いません。",
              "Toda 命題の一般形・特殊化の全自動適用可能性を個別 CSV 行数から推測しません。",
              "`GOAL_EXISTS_SEARCH_OR_PREMISE_UNRESOLVED` の内部原因は R3 で Proof Tree と未解決 Goal を詳査します。",
              "今回の監査標本だけから任意の stem・任意の群に一般化しません。", ""]
    return "\n".join(lines)


def run(root: Path, r1_report: Path, output: Path) -> int:
    if not root.is_dir() or output.exists():
        raise RuntimeError("repository missing or report output already exists")
    if output == root or root in output.parents:
        raise RuntimeError("output must be outside repository")
    evidence = preflight(root)
    r1_data, r1_index = load_r1(root, r1_report, evidence["head"])
    previous = snapshot(root)
    output.mkdir(parents=True)
    sys.path.insert(0, str(root))
    report: dict[str, Any] = {
        "phase": "170 R2", "mode": "AUDIT_ONLY", "git": evidence,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "r1_report": str(r1_report), "r1_case_count": len(r1_index),
        "full_pytest_run": False, "production_changed": False,
        "datasets": {}, "registry": {}, "cases": [],
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        datasets = {}
        for name in DATASETS:
            headers, rows = read_rows(root, name)
            datasets[name] = {"headers": headers, "rows": rows}
            report["datasets"][name] = {"headers": headers, "rows": len(rows)}
        bridge = build_shared_typed_bridge()
        registry = bridge.registry
        report["registry"] = {
            "assertions": len(registry._assertions),
            "references": len(registry._references),
            "proof_links": len(bridge.proof_links),
            "origin_counts": dict(Counter(
                getattr(x.origin, "value", str(x.origin))
                for x in registry._assertions.values()
            )),
            "positioned_fixed_assertions": sum(
                getattr(x.origin, "value", str(x.origin)) == "fixed_statement"
                and registry.reference(x.reference_id).publication_position is not None
                for x in registry._assertions.values()
            ),
        }
        for n, k in R1_GROUPS:
            label = f"pi_{n+k}^{n}"
            try:
                item = case_evidence(bridge, n, k, r1_index[label], datasets)
            except Exception as exc:
                item = {"group": label, "error": f"{type(exc).__name__}: {exc}",
                        "traceback": traceback.format_exc(), "blocker_classification": "AUDIT_ERROR"}
            report["cases"].append(item)
            print(f"PHASE170_R2_{label}={item['blocker_classification']}", flush=True)
        report["blocker_distribution"] = dict(Counter(
            x["blocker_classification"] for x in report["cases"]
        ))
        report["review_required"] = any(
            bool(x.get("selector_errors")) for x in report["cases"]
        )
    except Exception as exc:
        report["audit_error"] = f"{type(exc).__name__}: {exc}"
        report["audit_traceback"] = traceback.format_exc()
    finally:
        report["tracked_unchanged"] = snapshot(root) == previous
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        try:
            display = markdown(report) if not report.get("audit_error") and all(
                "error" not in x for x in report["cases"]
            ) else "# Phase 170 R2 — 監査エラー\n\n" + compact(report, 12000)
        except Exception as exc:
            display = f"# Phase 170 R2 — Markdown 出力エラー\n\n{type(exc).__name__}: {exc}\n"
        (output / "audit.md").write_text(display, encoding="utf-8")
        print(f"PHASE170_R2_REPORT={output / 'audit.md'}", flush=True)
        print(f"PHASE170_R2_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print("PHASE170_R2_FULL_PYTEST=False", flush=True)
    success = (
        report["tracked_unchanged"] and not report.get("audit_error")
        and len(report["cases"]) == len(R1_GROUPS)
        and all("error" not in x for x in report["cases"])
    )
    print(f"PHASE170_R2_REVIEW_REQUIRED={report.get('review_required', True)}", flush=True)
    print(f"PHASE170_R2_EXECUTION={'PASS' if success else 'REVIEW_REQUIRED'}", flush=True)
    return 0 if success else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--r1-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        return run(args.root.resolve(), args.r1_report.resolve(), args.output.resolve())
    except Exception:
        print("PHASE170_R2_REFUSED=" + traceback.format_exc(), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
