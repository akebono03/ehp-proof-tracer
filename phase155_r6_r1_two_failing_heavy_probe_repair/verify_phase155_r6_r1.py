from __future__ import annotations

import argparse
import ast
from pathlib import Path


EXPECTED = {
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py":
        "test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py":
        "test_phase150_rc4_7a_pi16_9_numbers_normalized_references",
}


def _function_source(source: str, function_name: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            if node.end_lineno is None:
                raise RuntimeError("missing end_lineno")
            return "".join(lines[node.lineno - 1:node.end_lineno])
    raise RuntimeError("function not found: " + function_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    sources = {}
    for relative_path, function_name in EXPECTED.items():
        source = (repo_root / relative_path).read_text(encoding="utf-8-sig")
        sources[relative_path] = _function_source(source, function_name)

    phase144 = sources[
        "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py"
    ]
    phase150 = sources[
        "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
    ]

    checks = {
        "phase144_no_longer_requires_zero_missing": (
            "missing_rendered_count" in phase144
            and "== 0" not in phase144
        ),
        "phase144_preserves_count_relationship": (
            "<= row.insertable_count" in phase144
            and "<= row.contribution_count" in phase144
        ),
        "phase150_requires_current_reference_set": (
            'assert "Lemma 5.14" in rendered' in phase150
            and 'assert "Theorem 3.6" in rendered' in phase150
            and 'assert "Lemma 5.13" in rendered' in phase150
        ),
        "phase150_excludes_stale_prop515": (
            'assert "Proposition 5.15" not in rendered' in phase150
        ),
    }

    for name, value in checks.items():
        print(name + ":", "PASS" if value else "FAIL")

    validated = all(checks.values())
    print("R6-R1 source repair validated:", validated)
    return 0 if validated else 2


if __name__ == "__main__":
    raise SystemExit(main())
