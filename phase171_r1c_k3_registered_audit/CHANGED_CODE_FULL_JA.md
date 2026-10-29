# Phase 171 R1C-R2 — `k=3` 監査の区切り行修正

## 原因と確認結果

`data/sphere.csv` の CSV レコード139行目には `3,,,,,,,,,,,,,,` があり、`k=3` ブロックの末尾を示す区切り行である。元の `registered_three_stem()` は `k=3` と一致するすべての行に対して `n >= 2` を要求したため、群座標ではない区切り行を「invalid n」と誤判定した。

GitHub `akebono03/ehp-proof-tracer` の `develop` で、`data/sphere.csv`（blob `b7e98a4469e0dcf2c5ea16691a7225951fd36395`）、`phase165_r55_nk_only_goal.py`、`web_group_proof.py`、`test_phase165_r55_nk_only_goal.py`、`test_phase165_r54_explicit_web_goal.py` を照合済み。R1C の現行コードと既存限定テスト14件を確認した。

## 変更対象

- `phase171_r1c_k3_registered_audit/audit.py` の **`registered_three_stem()` 関数全体**。既存 import は変更しない。
- `phase171_r1c_k3_registered_audit/tests/test_audit.py` に新規テスト関数3件を `test_inventory_deduplicates_csv_rows_and_sorts_n` の直後へ追加。既存テスト14件と import は変更しない。
- `phase171_r1c_k3_registered_audit/README.md` に区切り行修正の説明を追加（全文ファイル同梱、英語）。
- 本ファイルを新しい実装内容に更新。
- `run.ps1` は変更なし。既存アプリ、数式、データベース、Renderer、Git 追跡済みファイル、正式文書5件も変更なし。

## 変更後の `registered_three_stem()` 関数全文

`audit.py` 内の `tracked_digest()` の直後、`preflight()` の直前。

```python
def registered_three_stem(csv_path: Path) -> tuple[dict, ...]:
    """Enumerate explicit CSV coordinates, deduplicating generator rows."""
    counts: dict[int, int] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv requires n, k, id columns")
        for line_number, row in enumerate(reader, start=2):
            k_text = (row.get("k") or "").strip()
            n_text = (row.get("n") or "").strip()
            if k_text != str(STEM):
                continue
            # Toda's CSV uses an empty row such as "3,,,,,,,,,,,,,," at each
            # stem boundary. It is not a registered group coordinate.
            if not n_text and all(
                not (row.get(column) or "").strip()
                for column in reader.fieldnames if column != "k"
            ):
                continue
            if not n_text.isdecimal() or int(n_text) < 2:
                raise ValueError(f"invalid n for k=3 at CSV row {line_number}")
            n = int(n_text)
            counts[n] = counts.get(n, 0) + 1
    if not counts:
        raise ValueError("no explicitly registered k=3 goals")
    return tuple({"n": n, "k": STEM, "csv_rows": counts[n]}
                 for n in sorted(counts))
```

## 新規テスト関数3件の全文

`tests/test_audit.py` 内、`test_inventory_deduplicates_csv_rows_and_sorts_n()` の直後。

```python
def test_inventory_skips_k3_stem_separator_without_counting_it(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "4", "0", "inf", "ν4"))
        writer.writerow(("3", "4", "1", "4", "E ν'"))
        writer.writerow(("3", "", "", "", ""))
        writer.writerow(("4", "2", "0", "4", "η2ν'"))
    assert target.registered_three_stem(path) == (
        {"n": 2, "k": 3, "csv_rows": 1},
        {"n": 4, "k": 3, "csv_rows": 2},
    )


def test_inventory_skips_actual_sphere_csv_stem_boundary_shape(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text(
        "k,n,id,orders,generator,P,P_coe,E,E_coe,H,H_coe,Element,gen_coe,hyouji,orders2\n"
        "3,3,0,4,nu_prime,,,,,,,,,,\n"
        "3,,,,,,,,,,,,,,\n"
        "4,2,0,4,other,,,,,,,,,,\n",
        encoding="utf-8-sig",
    )
    assert target.registered_three_stem(path) == (
        {"n": 3, "k": 3, "csv_rows": 1},
    )


def test_inventory_rejects_k3_row_with_empty_n_and_nonempty_data(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "", "1", "4", "ν"))
    with pytest.raises(ValueError, match="invalid n for k=3 at CSV row 3"):
        target.registered_three_stem(path)
```

## `audit.py`：変更後の import およびファイル全文

```python
"""Read-only registered 3-stem audit (k=3, variable n >= 2).

This module does not add mathematical premises, infer groups from missing CSV
entries, or change existing project sources. Each registered (n, 3) goal is
searched independently and checked against the public trust-gated Web route.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
EXPECTED_BRANCH = "develop"
EXPECTED_CSV_BLOB = "b7e98a4469e0dcf2c5ea16691a7225951fd36395"
STEM = 3
SENTINEL = "__PHASE171_R1C_WORKER__="


def run_git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return process.stdout.decode("utf-8", errors="replace").strip()


def tracked_digest(root: Path) -> str:
    process = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("cannot obtain tracked diff")
    return sha256(process.stdout).hexdigest()


def registered_three_stem(csv_path: Path) -> tuple[dict, ...]:
    """Enumerate explicit CSV coordinates, deduplicating generator rows."""
    counts: dict[int, int] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv requires n, k, id columns")
        for line_number, row in enumerate(reader, start=2):
            k_text = (row.get("k") or "").strip()
            n_text = (row.get("n") or "").strip()
            if k_text != str(STEM):
                continue
            # Toda's CSV uses an empty row such as "3,,,,,,,,,,,,,," at each
            # stem boundary. It is not a registered group coordinate.
            if not n_text and all(
                not (row.get(column) or "").strip()
                for column in reader.fieldnames if column != "k"
            ):
                continue
            if not n_text.isdecimal() or int(n_text) < 2:
                raise ValueError(f"invalid n for k=3 at CSV row {line_number}")
            n = int(n_text)
            counts[n] = counts.get(n, 0) + 1
    if not counts:
        raise ValueError("no explicitly registered k=3 goals")
    return tuple({"n": n, "k": STEM, "csv_rows": counts[n]}
                 for n in sorted(counts))


def preflight(root: Path) -> dict:
    """Pin the reviewed Git state without contacting or modifying origin."""
    branch = run_git(root, "branch", "--show-current")
    head = run_git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    origin = run_git(root, "rev-parse", "--verify", "refs/remotes/origin/develop")
    if origin != EXPECTED_HEAD:
        raise RuntimeError(f"origin/develop mismatch: {origin}")
    if run_git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked working tree is not clean")
    csv_blob = run_git(root, "rev-parse", "HEAD:data/sphere.csv")
    if csv_blob != EXPECTED_CSV_BLOB:
        raise RuntimeError("unreviewed sphere.csv blob")
    required = (
        "data/sphere.csv",
        "phase165_r55_nk_only_goal.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "web_group_proof.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
    )
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise RuntimeError(f"missing current sources: {missing}")
    return {"branch": branch, "head": head, "origin_develop": origin,
            "csv_blob": csv_blob, "tracked_digest": tracked_digest(root),
            "tracked_clean": True}


def worker(n: int) -> int:
    """Run standard typed-goal search and public Web verification, unmodified."""
    row = {"n": n, "k": STEM, "group_dimension": n + STEM,
           "result": "WORKER_FAILURE", "web_error": None}
    try:
        from phase169_r10e4_ordered_db_prior.db_prior import (
            exact_prior_database_result,
            group_coordinates,
        )
        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from web_group_proof import build_standard_web_group_proof_view

        target = exact_prior_database_result(n, STEM)
        row["target_typed"] = target is not None
        row["target_type"] = type(target).__name__ if target is not None else None
        row["target_coordinates"] = (
            list(group_coordinates(target))
            if target is not None and group_coordinates(target) is not None
            else None
        )
        result = search_group_from_registered_goal(n=n, k=STEM)
        row["search_status"] = getattr(result.status, "value", str(result.status))
        row["proven_steps"] = len(result.proven_steps)
        row["open_goals"] = len(result.open_goals)
        row["diagnostics"] = [str(item)[:1000] for item in result.diagnostics[:10]]
        row["open_goal_samples"] = [str(item)[:1000] for item in result.open_goals[:5]]
        row["root_conclusion_matches_target"] = bool(
            target is not None and type(result.conclusion) is type(target)
            and result.conclusion == target
        )
        row["search_complete"] = bool(
            result.status is ProofSearchStatus.COMPLETE
            and not result.open_goals and result.proven_steps
            and result.conclusion is not None
        )
        row.update(web_key=None, web_partial=None, web_steps=0, web_lines=0)
        try:
            view = build_standard_web_group_proof_view(
                n=n, k=STEM, max_depth=2,
                mode="narrative", citation_source="model",
            )
            row["web_key"] = view.key
            row["web_partial"] = view.partial_result
            row["web_steps"] = len(view.steps)
            row["web_lines"] = len(view.rendered_lines)
        except Exception as exc:
            row["web_error"] = f"{type(exc).__name__}: {exc}"[:1500]
        row["result"] = classify_worker(row, n)
        exit_code = 0
    except Exception as exc:
        row["exception"] = f"{type(exc).__name__}: {exc}"[:1500]
        row["traceback"] = traceback.format_exc()[-3000:]
        exit_code = 1
    print(SENTINEL + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
    return exit_code


def qualifies_complete(row: dict, n: int) -> bool:
    return (
        row.get("n") == n and row.get("k") == STEM
        and row.get("group_dimension") == n + STEM
        and row.get("target_typed") is True
        and row.get("target_coordinates") == [n, STEM]
        and row.get("root_conclusion_matches_target") is True
        and row.get("search_status") == "complete"
        and row.get("search_complete") is True
        and type(row.get("proven_steps")) is int and row["proven_steps"] > 0
        and type(row.get("open_goals")) is int and row["open_goals"] == 0
        and row.get("web_key") == "generic-complete-proof"
        and row.get("web_partial") is False
        and type(row.get("web_steps")) is int and row["web_steps"] > 0
        and type(row.get("web_lines")) is int and row["web_lines"] > 0
        and row.get("web_error") is None
    )


def classify_worker(row: dict, n: int) -> str:
    if qualifies_complete(row, n):
        return "COMPLETE_AND_WEB_VERIFIED"
    if row.get("target_typed") is not True:
        return "TYPED_TARGET_UNAVAILABLE"
    if row.get("search_status") != "complete" or row.get("open_goals") != 0:
        return "PROOF_UNFINISHED"
    if row.get("root_conclusion_matches_target") is not True:
        return "CONCLUSION_MISMATCH"
    return "WEB_UNVERIFIED"


def parse_worker_output(output: str, exit_code: int, n: int) -> dict:
    markers = [line[len(SENTINEL):] for line in output.splitlines()
               if line.startswith(SENTINEL)]
    if len(markers) != 1:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "marker_count": len(markers),
                "diagnostics": [output[-1500:]]}
    try:
        row = json.loads(markers[0])
    except json.JSONDecodeError as exc:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "diagnostics": [str(exc)]}
    if not isinstance(row, dict) or row.get("n") != n or row.get("k") != STEM:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "diagnostics": ["worker goal mismatch"]}
    if exit_code != 0 or row.get("result") == "WORKER_FAILURE":
        row["result"] = "WORKER_FAILURE"
        row["exit_code"] = exit_code
    elif row.get("result") != classify_worker(row, n):
        row["result"] = "WORKER_FAILURE"
        row["diagnostics"] = ["worker classification mismatch"]
    return row


def execute_worker(root: Path, n: int, timeout_seconds: int, output: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    path = output / f"n_{n:03d}.log"
    try:
        process = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).resolve()),
             "--worker", "--n", str(n)],
            cwd=root, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", timeout=timeout_seconds, check=False,
        )
        path.write_text(process.stdout, encoding="utf-8")
        return parse_worker_output(process.stdout, process.returncode, n)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        path.write_text(raw, encoding="utf-8")
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "diagnostics": ["timeout"], "timeout_seconds": timeout_seconds}


def summarize_rows(rows: list[dict], domain: tuple[dict, ...]) -> dict:
    expected = [item["n"] for item in domain]
    actual = [item.get("n") for item in rows]
    if actual != expected or any(row.get("k") != STEM for row in rows):
        raise ValueError("worker rows do not match registered k=3 domain")
    complete = sum(row.get("result") == "COMPLETE_AND_WEB_VERIFIED" for row in rows)
    failures = sum(row.get("result") == "WORKER_FAILURE" for row in rows)
    return {"domain_checked": len(rows), "domain_complete": complete,
            "domain_gaps": len(rows) - complete, "worker_failures": failures}


def write_json(path: Path, report: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def write_markdown(path: Path, report: dict) -> None:
    lines = ["# Phase 171 R1C — 3-stem 全登録座標監査", "",
             "対象は k=3、n は現行 data/sphere.csv の明示登録のみ。",
             "未完成群を証明済みと扱わず、正式文書・コードは変更しない。", "",
             f"- 対象群: {report.get('domain_checked', 0)}",
             f"- 完成・Web検証済み: {report.get('domain_complete', 0)}",
             f"- 未完成・未検証: {report.get('domain_gaps', 0)}",
             f"- Worker failures: {report.get('worker_failures', 0)}", "",
             "| n | 群 | CSV行 | Typed goal | Search | Steps | Open | Web | Result |",
             "|---:|---|---:|---|---|---:|---:|---|---|"]
    registered = {entry["n"]: entry["csv_rows"] for entry in report.get("domain", [])}
    for row in report.get("rows", []):
        n = row["n"]
        lines.append(
            f"| {n} | $\\pi_{{{n + STEM}}}^{{{n}}}$ | {registered.get(n, 0)} | "
            f"{row.get('target_typed', '?')} | {row.get('search_status', '?')} | "
            f"{row.get('proven_steps', '?')} | {row.get('open_goals', '?')} | "
            f"{row.get('web_key', '?')} | {row.get('result', '?')} |"
        )
    lines.extend(["", "詳細は audit.json および n_XXX.log を参照。", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def audit(root: Path, *, dry_run: bool, timeout_seconds: int) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    recovery.mkdir(parents=True, exist_ok=True)
    output = recovery / ("phase171_r1c_k3_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE171_R1C_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE171_R1C_OUTPUT={output}", flush=True)
    report: dict = {"phase": "171 R1C", "mode": "AUDIT_ONLY",
                    "stem": STEM, "dry_run": dry_run, "full_pytest": False,
                    "production_modified": False, "rows": []}
    before = None
    exit_code = 2
    try:
        before = preflight(root)
        report["preflight"] = before
        domain = registered_three_stem(root / "data" / "sphere.csv")
        report["domain"] = list(domain)
        print(f"PHASE171_R1C_DOMAIN_REGISTERED={len(domain)}", flush=True)
        print("PHASE171_R1C_N=" + ",".join(str(item["n"]) for item in domain), flush=True)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            exit_code = 0
            print("PHASE171_R1C_DRY_RUN=PASS", flush=True)
        else:
            for item in domain:
                n = item["n"]
                row = execute_worker(root, n, timeout_seconds, output)
                report["rows"].append(row)
                report.update(summarize_rows(report["rows"], tuple(domain[:len(report["rows"])])))
                write_json(output / "audit.json", report)
                print(f"PHASE171_R1C_n={n} RESULT={row['result']}", flush=True)
            report.update(summarize_rows(report["rows"], domain))
            report["result"] = (
                "AUDIT_COMPLETE_WITH_WORKER_FAILURES" if report["worker_failures"]
                else "AUDIT_COMPLETE_WITH_GAPS" if report["domain_gaps"]
                else "ALL_REGISTERED_COMPLETE"
            )
            for key in ("domain_checked", "domain_complete", "domain_gaps", "worker_failures"):
                print(f"PHASE171_R1C_{key.upper()}={report[key]}", flush=True)
            exit_code = 1 if report["worker_failures"] else 0
    except Exception as exc:
        report["result"] = "AUDIT_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print(f"PHASE171_R1C_ERROR={report['error']}", flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root)
                report["tracked_unchanged"] = after == before
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                exit_code = 2
        else:
            report["tracked_unchanged"] = None
        write_json(output / "audit.json", report)
        if not dry_run:
            write_markdown(output / "audit.md", report)
        print(f"PHASE171_R1C_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE171_R1C_REPORT={output / 'audit.json'}", flush=True)
        print(f"PHASE171_R1C_RESULT={report['result']}", flush=True)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=False, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int)
    args = parser.parse_args()
    if args.worker:
        if args.n is None or args.n < 2:
            parser.error("worker requires n >= 2")
        return worker(args.n)
    if args.root is None:
        parser.error("--root required for main audit")
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    return audit(args.root.resolve(), dry_run=args.dry_run,
                 timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_audit.py`：import およびテスト全文

```python
"""Only newly added R1C audit helpers are tested; no full-suite pytest."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from phase171_r1c_k3_registered_audit import audit as target


def make_csv(path: Path, records: list[tuple[str, str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "generator"))
        for k, n, record_id in records:
            writer.writerow((k, n, record_id, "g"))


def complete_row(n: int) -> dict:
    return {"n": n, "k": 3, "group_dimension": n + 3,
            "target_typed": True, "target_coordinates": [n, 3],
            "root_conclusion_matches_target": True, "search_status": "complete",
            "search_complete": True, "proven_steps": 2, "open_goals": 0,
            "web_key": "generic-complete-proof", "web_partial": False,
            "web_steps": 2, "web_lines": 3, "web_error": None}


def test_inventory_deduplicates_csv_rows_and_sorts_n(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("3", "59", "0"), ("3", "4", "0"),
                    ("3", "4", "1"), ("2", "8", "0"), ("3", "2", "0")])
    assert target.registered_three_stem(path) == (
        {"n": 2, "k": 3, "csv_rows": 1},
        {"n": 4, "k": 3, "csv_rows": 2},
        {"n": 59, "k": 3, "csv_rows": 1},
    )


def test_inventory_skips_k3_stem_separator_without_counting_it(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "4", "0", "inf", "ν4"))
        writer.writerow(("3", "4", "1", "4", "E ν'"))
        writer.writerow(("3", "", "", "", ""))
        writer.writerow(("4", "2", "0", "4", "η2ν'"))
    assert target.registered_three_stem(path) == (
        {"n": 2, "k": 3, "csv_rows": 1},
        {"n": 4, "k": 3, "csv_rows": 2},
    )


def test_inventory_skips_actual_sphere_csv_stem_boundary_shape(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text(
        "k,n,id,orders,generator,P,P_coe,E,E_coe,H,H_coe,Element,gen_coe,hyouji,orders2\n"
        "3,3,0,4,nu_prime,,,,,,,,,,\n"
        "3,,,,,,,,,,,,,,\n"
        "4,2,0,4,other,,,,,,,,,,\n",
        encoding="utf-8-sig",
    )
    assert target.registered_three_stem(path) == (
        {"n": 3, "k": 3, "csv_rows": 1},
    )


def test_inventory_rejects_k3_row_with_empty_n_and_nonempty_data(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("k", "n", "id", "orders", "generator"))
        writer.writerow(("3", "2", "0", "2", "η2^3"))
        writer.writerow(("3", "", "1", "4", "ν"))
    with pytest.raises(ValueError, match="invalid n for k=3 at CSV row 3"):
        target.registered_three_stem(path)


def test_inventory_rejects_unregistered_stem(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("2", "3", "0")])
    with pytest.raises(ValueError, match="no explicitly"):
        target.registered_three_stem(path)


def test_inventory_rejects_invalid_n(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    make_csv(path, [("3", "1", "0")])
    with pytest.raises(ValueError, match="invalid n"):
        target.registered_three_stem(path)


def test_inventory_requires_columns(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("n,k\n3,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="requires"):
        target.registered_three_stem(path)


def test_verified_row_must_match_fixed_k_and_variable_n() -> None:
    good = complete_row(11)
    assert target.qualifies_complete(good, 11)
    assert target.classify_worker(good, 11) == "COMPLETE_AND_WEB_VERIFIED"
    assert not target.qualifies_complete(good, 3)
    bad = {**good, "k": 2}
    assert not target.qualifies_complete(bad, 11)


def test_qualified_complete_requires_actual_web_and_root() -> None:
    row = complete_row(3)
    assert not target.qualifies_complete({**row, "web_partial": True}, 3)
    assert not target.qualifies_complete({**row, "web_error": "UnverifiedProofTree"}, 3)
    assert not target.qualifies_complete({**row, "root_conclusion_matches_target": False}, 3)
    assert not target.qualifies_complete({**row, "proven_steps": 0}, 3)


def test_classification_is_fail_closed() -> None:
    row = complete_row(4)
    assert target.classify_worker({**row, "target_typed": False}, 4) == "TYPED_TARGET_UNAVAILABLE"
    assert target.classify_worker({**row, "search_status": "partial"}, 4) == "PROOF_UNFINISHED"
    assert target.classify_worker({**row, "root_conclusion_matches_target": False}, 4) == "CONCLUSION_MISMATCH"
    assert target.classify_worker({**row, "web_key": "partial-proof"}, 4) == "WEB_UNVERIFIED"


def test_parse_worker_emitted_result() -> None:
    row = {**complete_row(3), "result": "COMPLETE_AND_WEB_VERIFIED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3) == row


def test_worker_rejects_mismatched_coordinates() -> None:
    row = {**complete_row(4), "result": "COMPLETE_AND_WEB_VERIFIED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3)["result"] == "WORKER_FAILURE"


def test_worker_rejects_wrong_classification_or_exit() -> None:
    row = {**complete_row(3), "result": "PROOF_UNFINISHED"}
    raw = target.SENTINEL + json.dumps(row) + "\n"
    assert target.parse_worker_output(raw, 0, 3)["result"] == "WORKER_FAILURE"
    assert target.parse_worker_output(raw, 1, 3)["result"] == "WORKER_FAILURE"


def test_worker_rejects_missing_or_invalid_json() -> None:
    assert target.parse_worker_output("no marker", 0, 3)["result"] == "WORKER_FAILURE"
    assert target.parse_worker_output(target.SENTINEL + "{invalid", 0, 3)["result"] == "WORKER_FAILURE"


def test_summary_uses_registered_coordinate_not_csv_row_count() -> None:
    domain = ({"n": 2, "k": 3, "csv_rows": 1},
              {"n": 4, "k": 3, "csv_rows": 2})
    rows = [{"n": 2, "k": 3, "result": "COMPLETE_AND_WEB_VERIFIED"},
            {"n": 4, "k": 3, "result": "PROOF_UNFINISHED"}]
    assert target.summarize_rows(rows, domain) == (
        {"domain_checked": 2, "domain_complete": 1,
         "domain_gaps": 1, "worker_failures": 0}
    )
    with pytest.raises(ValueError, match="do not match"):
        target.summarize_rows(list(reversed(rows)), domain)


def test_summary_counts_worker_failures() -> None:
    domain = ({"n": 3, "k": 3, "csv_rows": 1},)
    rows = [{"n": 3, "k": 3, "result": "WORKER_FAILURE"}]
    assert target.summarize_rows(rows, domain)["worker_failures"] == 1


def test_report_outputs_are_utf8_and_unabridged(tmp_path: Path) -> None:
    report = {"domain": [{"n": 4, "csv_rows": 2}],
              "rows": [{"n": 4, "k": 3, "result": "PROOF_UNFINISHED",
                        "diagnostics": ["生成元の型付き対応"]}],
              "domain_checked": 1, "domain_complete": 0,
              "domain_gaps": 1, "worker_failures": 0}
    json_path, md_path = tmp_path / "audit.json", tmp_path / "audit.md"
    target.write_json(json_path, report)
    target.write_markdown(md_path, report)
    assert json.loads(json_path.read_text(encoding="utf-8")) == report
    assert "\\pi_{7}^{4}" in md_path.read_text(encoding="utf-8")
    assert "CSV行" in md_path.read_text(encoding="utf-8")
```

## `run.ps1`：解凍後の実行器全文（変更なし）

```powershell
param(
    [switch]$DryRun,
    [ValidateRange(1, 3600)][int]$TimeoutSeconds = 180
)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider '.\phase171_r1c_k3_registered_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R1C_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R1C_FOCUSED_PYTEST=PASS'
    $AuditArgs = @('-B', '.\phase171_r1c_k3_registered_audit\audit.py', '--root', $RepoRoot, '--timeout-seconds', [string]$TimeoutSeconds)
    if ($DryRun) { $AuditArgs += '--dry-run' }
    & python @AuditArgs
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R1C_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R1C=PASS'
}
finally {
    Pop-Location
}
```

## Windows での実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase171_r1c_k3_registered_audit_r2.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1c_k3_registered_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1c_k3_registered_audit\run.ps1"
git status -sb
```

`Expand-Archive -Force` は既存の追跡対象外 `phase171_r1c_k3_registered_audit/` 内の同名ファイルを置き換える。正式な production ソースは変更しない。

## 実施した検証と完了条件

- 限定 pytest：**17 PASS**（従来14件と新規3件）。全体テストは実行しない。
- Python 構文：PASS。
- CSV 区切り行 `3,,,,,,,,,,,,,,` を除外し、型付き実データ行で `n` が不正な場合は引き続き例外にする。
- 複数 CSV 行を持つ同一 $(n,3)$ を1座標として数える。
- Windows 実監査の `PHASE171_R1C_DOMAIN_REGISTERED=32`、`PHASE171_R1C_TRACKED_UNCHANGED=True` を確認するまでは、監査完了件数を主張しない。

## 次段階との境界

R1C-R2 は **監査入力の CSV 区切り行修正のみ**。数学的な推論規則、文献引用、Proof Search、Trust Boundary には手を加えない。登録済み $k=3$ 群の監査結果が得られてから Phase 171 R2 の数学的実装対象を決定する。
