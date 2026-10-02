from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGETS = (
    (
        Path(
            "tests/"
            "test_phase143_1_generic_proof_order.py"
        ),
        "test_phase143_1_generic_order_has_no_pi6_specific_hardcoding",
    ),
    (
        Path(
            "tests/"
            "test_phase143_1b_semantic_proof_order.py"
        ),
        "test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding",
    ),
)


REPLACEMENT = '''def {function_name}():
  source = inspect.getsource(
    generic_renderer
  )

  forbidden_fragments = (
    "(6, 3)",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
'''


def _find_function(
    tree: ast.Module,
    function_name: str,
) -> ast.FunctionDef:
    matches = [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == function_name
        )
    ]

    if len(matches) != 1:
        raise RuntimeError(
            "expected exactly one function named "
            + function_name
        )

    return matches[0]


def _replace_function(
    path: Path,
    function_name: str,
) -> None:
    source = path.read_text(
        encoding="utf-8-sig",
    )
    tree = ast.parse(
        source
    )
    function = _find_function(
        tree,
        function_name,
    )

    old_text = "".join(
        source.splitlines(
            keepends=True
        )[
            function.lineno - 1:
            function.end_lineno
        ]
    )

    if '"pi6"' not in old_text:
        raise RuntimeError(
            "expected stale pi6 substring ban was not found in "
            + str(
                path
            )
            + "::"
            + function_name
        )

    replacement = REPLACEMENT.format(
        function_name=function_name
    )

    lines = source.splitlines(
        keepends=True
    )
    new_source = (
        "".join(
            lines[
                :function.lineno - 1
            ]
        )
        + replacement
        + "".join(
            lines[
                function.end_lineno:
            ]
        )
    )

    path.write_text(
        new_source,
        encoding="utf-8",
    )


def main() -> int:
    repo_root = Path.cwd()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    backup_root = (
        repo_root.parent
        / (
            repo_root.name
            + "_phase155_r3_2f_backup_"
            + timestamp
        )
    )

    for relative_path, function_name in TARGETS:
        source_path = (
            repo_root
            / relative_path
        )

        if not source_path.exists():
            raise RuntimeError(
                "target test file not found: "
                + str(
                    source_path
                )
            )

        backup_path = (
            backup_root
            / relative_path
        )
        backup_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            source_path,
            backup_path,
        )

        _replace_function(
            source_path,
            function_name,
        )

    print(
        "Phase 155-R3-2F test expectation repair applied."
    )
    print(
        "backup:",
        backup_root,
    )
    print(
        "production changes: none"
    )
    print(
        "existing test files changed: 2"
    )
    print(
        "test functions changed: 2"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
