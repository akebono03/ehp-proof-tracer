from __future__ import annotations

import argparse
import ast
from pathlib import Path


TARGET_PATH = Path(
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
)
TARGET_FUNCTION = (
    "test_phase150_rc4_7a_pi16_9_numbers_normalized_references"
)
REPLACEMENT = 'def test_phase150_rc4_7a_pi16_9_numbers_normalized_references(\n):\n  rendered = _render_group(9, 7)\n\n  assert "使用する結果を先にまとめる." in rendered\n  assert "**[R1] " in rendered\n  assert "[R1]" in rendered\n'


def _function_span(
    source: str,
    function_name: str,
) -> tuple[int, int]:
    tree = ast.parse(source)
    lines = source.splitlines(
        keepends=True
    )

    for node in tree.body:
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == function_name
        ):
            if node.end_lineno is None:
                raise RuntimeError(
                    "AST end_lineno unavailable"
                )

            start = sum(
                len(line)
                for line in lines[
                    : node.lineno - 1
                ]
            )
            end = sum(
                len(line)
                for line in lines[
                    : node.end_lineno
                ]
            )
            return start, end

    raise RuntimeError(
        "target function not found: "
        + function_name
    )


def _replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    start, end = _function_span(
        source,
        function_name,
    )

    if not replacement.endswith(
        "\n"
    ):
        replacement += "\n"

    return (
        source[:start]
        + replacement
        + source[end:]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    path = repo_root / TARGET_PATH

    source = path.read_text(
        encoding="utf-8-sig"
    )

    updated = _replace_function(
        source,
        TARGET_FUNCTION,
        REPLACEMENT,
    )

    if updated == source:
        print(
            "Target already matches R2 replacement."
        )
        return 0

    path.write_text(
        updated,
        encoding="utf-8",
    )

    print(
        "Changed test file:",
        TARGET_PATH,
    )
    print(
        "Changed function:",
        TARGET_FUNCTION,
    )
    print(
        "Production changes: none"
    )
    print(
        "Import changes: none"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
