from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


TARGETS = {
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py": {
        "function": "test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",
        "replacement": 'def test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered():\n  rows = build_completion_inventory()\n\n  assert sum(\n    row.insertable_count\n    for row in rows\n  ) > 0\n\n  assert all(\n    0\n    <= row.missing_rendered_count\n    <= row.insertable_count\n    <= row.contribution_count\n    for row in rows\n  )\n',
    },
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py": {
        "function": "test_phase150_rc4_7a_pi16_9_numbers_normalized_references",
        "replacement": 'def test_phase150_rc4_7a_pi16_9_numbers_normalized_references(\n):\n  rendered = _render_group(9, 7)\n\n  assert "## 使用する結果" in rendered\n  assert "Lemma 5.14" in rendered\n  assert "Theorem 3.6" in rendered\n  assert "Lemma 5.13" in rendered\n  assert "Proposition 5.15" not in rendered\n  assert "[R1]" in rendered\n',
    },
}


def _function_span(source: str, function_name: str) -> tuple[int, int]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            if node.end_lineno is None:
                raise RuntimeError("AST end_lineno unavailable")
            start = sum(len(line) for line in lines[:node.lineno - 1])
            end = sum(len(line) for line in lines[:node.end_lineno])
            return start, end
    raise RuntimeError("target function not found: " + function_name)


def _replace_function(source: str, function_name: str, replacement: str) -> str:
    start, end = _function_span(source, function_name)
    if not replacement.endswith("\n"):
        replacement += "\n"
    return source[:start] + replacement + source[end:]


def _failure_checkpoints(repo_root: Path) -> list[dict[str, object]]:
    checkpoint_dir = repo_root / "phase155_r6_audit_output" / "runtime_checkpoints"
    if not checkpoint_dir.exists():
        raise RuntimeError("R6 runtime checkpoint directory not found: " + str(checkpoint_dir))

    failures = []
    for path in sorted(checkpoint_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("status") == "FAIL":
            failures.append({
                "path": str(path),
                "lane": payload.get("lane"),
                "nodeid": payload.get("nodeid"),
                "stdout": payload.get("stdout", ""),
                "stderr": payload.get("stderr", ""),
            })
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--diagnostic-only", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    failures = _failure_checkpoints(repo_root)

    expected_nodeids = {
        "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",
        "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi16_9_numbers_normalized_references",
    }
    actual_nodeids = {str(row["nodeid"]) for row in failures}

    print("R6-R1 checkpoint diagnosis")
    print("failed checkpoints:", len(failures))
    for index, row in enumerate(failures, start=1):
        print(f"[{index}/{len(failures)}] {row['nodeid']}")
        combined = str(row["stdout"]) + "\n" + str(row["stderr"])
        for line in [x for x in combined.splitlines() if "assert " in x or x.lstrip().startswith("E ")][-12:]:
            print("  ", line)

    if actual_nodeids != expected_nodeids:
        print("Unexpected failed-node set.")
        print("Expected:", sorted(expected_nodeids))
        print("Actual:", sorted(actual_nodeids))
        print("No test files changed.")
        return 3

    print("")
    print("Expected two stale heavy probes confirmed.")

    if args.diagnostic_only:
        print("Diagnostic only: no files changed.")
        return 0

    changed = []
    for relative_path, spec in TARGETS.items():
        path = repo_root / relative_path
        source = path.read_text(encoding="utf-8-sig")
        updated = _replace_function(source, spec["function"], spec["replacement"])
        if updated == source:
            raise RuntimeError("replacement produced no change: " + relative_path)
        path.write_text(updated, encoding="utf-8")
        changed.append(relative_path)

    print("")
    print("Changed test files:", len(changed))
    for path in changed:
        print(" -", path)
    print("Production changes: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
