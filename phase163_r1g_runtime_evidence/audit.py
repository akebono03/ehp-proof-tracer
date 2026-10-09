from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from pathlib import Path


def describe_repository(name: str, repository: object) -> dict:
    raw = getattr(repository, "entries")
    entries = raw() if callable(raw) else raw
    rows = []
    for i, entry in enumerate(entries):
        step = getattr(entry, "step", None)
        statement = getattr(entry, "statement", None)
        conclusion = getattr(step, "conclusion", None) if step is not None else statement
        reference = getattr(entry, "reference", None)
        rows.append({
            "repository": name,
            "index": i,
            "entry_type": type(entry).__name__,
            "key": getattr(entry, "key", None),
            "theorem": getattr(entry, "theorem", None),
            "phase": getattr(entry, "phase", None),
            "statement_type": type(conclusion).__name__ if conclusion is not None else None,
            "reference_type": type(reference).__name__ if reference is not None else None,
            "premise_count": len(step.premises) if step is not None and hasattr(step, "premises") else None,
            "proof_step_present": step is not None,
        })
    return {"repository": name, "entry_count": len(rows), "entries": rows}


def gather(include_standard: bool = False) -> dict:
    results = []
    errors = []
    try:
        module = importlib.import_module("theorem_facts")
        results.append(describe_repository("THEOREM_FACT_REPOSITORY", module.THEOREM_FACT_REPOSITORY))
    except Exception as exc:
        errors.append({"repository": "THEOREM_FACT_REPOSITORY", "error": f"{type(exc).__name__}: {exc}"})

    if include_standard:
        try:
            # Reuse existing focused test fixture without changing its contracts.
            tests_path = str(Path.cwd() / "tests")
            if tests_path not in sys.path:
                sys.path.insert(0, tests_path)
            fixture = importlib.import_module("test_phase100_standard_repository")
            data = fixture.build_phase100_11_standard_data()
            results.append(describe_repository("build_standard_proof_repository", data["repository"]))
        except Exception as exc:
            errors.append({"repository": "build_standard_proof_repository", "error": f"{type(exc).__name__}: {exc}"})
    return {
        "scope": "selected real runtime repositories, NOT all registered mathematical statements",
        "standard_fixture_requested": include_standard,
        "repositories": results,
        "errors": errors,
        "unverified": [
            "other repositories and indirect factories",
            "distinct mathematical statement identity",
            "literature source, publication order, proof-completion position",
            "fixed-statement versus proof-internal classification",
            "general-variable application domains and dependencies",
        ],
    }


def write_report(output_dir: Path, result: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    fields = [
        "repository", "index", "entry_type", "key", "theorem", "phase",
        "statement_type", "reference_type", "premise_count", "proof_step_present",
    ]
    with (output_dir / "runtime_entries.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for group in result["repositories"]:
            writer.writerows(group["entries"])
    lines = [
        "# Phase 163 R1G 実行時 Repository 監査",
        "",
        "これは選択した Repository の実行時登録実体であり、全命題総数ではありません。",
        "",
    ]
    for group in result["repositories"]:
        lines.append(f"- {group['repository']}: {group['entry_count']} entries")
    for err in result["errors"]:
        lines.append(f"- ERROR {err['repository']}: {err['error']}")
    lines += [
        "",
        "## 未確認事項",
        *[f"- {s}" for s in result["unverified"]],
        "",
        "R1 完了判定: 未完了（追加 Repository と文献との照合が必要）",
        "",
    ]
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-standard", action="store_true")
    parser.add_argument("--output", default="phase163_r1g_output")
    args = parser.parse_args()
    result = gather(include_standard=args.include_standard)
    write_report(Path(args.output), result)
    print(json.dumps(
        {"repositories": {g["repository"]: g["entry_count"] for g in result["repositories"]},
         "errors": result["errors"], "status": "R1_NOT_COMPLETE"},
        ensure_ascii=False, indent=2
    ))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
