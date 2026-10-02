from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


REPLACEMENTS = {
    "tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads": r"""def test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads():
  data = (
    build_phase132_6_sigma9_narrative(
      max_depth=1,
    )
  )

  rendered = data[
    "rendered"
  ]

  assert "まず, " in rendered
  assert "このことから, " in rendered
  assert "したがって, " in rendered

  assert "まず、" not in rendered
  assert "このことから、" not in rendered
  assert "したがって、" not in rendered

  assert "まず, 既出の" not in rendered
  assert "まず, すでに得た" not in rendered
""",
    "tests/test_phase153_r12_root_reference_exclusion.py::test_phase153_r12_pi11_4_body_uses_renumbered_external_references": r"""def test_phase153_r12_pi11_4_body_uses_renumbered_external_references():
  rendered = _render_group(
    4,
    7,
  )
  marker = "## 証明\n\n"
  body = rendered.split(
    marker,
    1,
  )[1]

  assert "[R1]を用いる." in body
  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in body
  )
  assert "[R3]" not in body
  assert "Proposition 5.15" not in body
""",
}


def _replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    tree = ast.parse(source)
    target = next(
        (
            node
            for node in tree.body
            if (
                isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                )
                and node.name == function_name
            )
        ),
        None,
    )

    if target is None:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    lines = source.splitlines(
        keepends=True,
    )
    changed = (
        "".join(
            lines[: target.lineno - 1]
        )
        + replacement.rstrip()
        + "\n\n"
        + "".join(
            lines[target.end_lineno :]
        )
    )
    ast.parse(
        changed
    )
    return changed


def apply_repairs(
    repo_root: Path,
) -> dict[str, list[str]]:
    by_file: dict[
        str,
        list[
            tuple[
                str,
                str,
            ]
        ],
    ] = {}

    for nodeid, replacement in (
        REPLACEMENTS.items()
    ):
        file_name, function_name = (
            nodeid.split(
                "::",
                1,
            )
        )
        by_file.setdefault(
            file_name,
            [],
        ).append(
            (
                function_name,
                replacement,
            )
        )

    changed_files: dict[
        str,
        list[str],
    ] = {}

    for file_name in sorted(
        by_file
    ):
        path = (
            repo_root
            / file_name
        )
        if not path.exists():
            raise RuntimeError(
                "target file not found: "
                + file_name
            )

        source = path.read_text(
            encoding="utf-8-sig",
        )
        original = source

        changed_functions = []

        for (
            function_name,
            replacement,
        ) in by_file[file_name]:
            source = (
                _replace_function(
                    source,
                    function_name,
                    replacement,
                )
            )
            changed_functions.append(
                function_name
            )

        if source == original:
            raise RuntimeError(
                "no change produced for: "
                + file_name
            )

        path.write_text(
            source,
            encoding="utf-8",
        )
        changed_files[
            file_name
        ] = changed_functions

    return changed_files


def main() -> int:
    parser = (
        argparse.ArgumentParser()
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = (
        args.repo_root.resolve()
    )
    changed = apply_repairs(
        repo_root
    )

    manifest = {
        "phase": "155-R2C-r2",
        "production_code_modified": False,
        "existing_tests_modified": True,
        "changed_files": changed,
        "changed_test_functions": sum(
            len(functions)
            for functions
            in changed.values()
        ),
        "repository_wide_pytest_executed": False,
    }

    manifest_path = (
        repo_root
        / "phase155_r2c_r2_repair_manifest.json"
    )
    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R2C-r2 repairs applied."
    )
    print(
        "changed files:",
        len(changed),
    )
    print(
        "changed test functions:",
        sum(
            len(functions)
            for functions
            in changed.values()
        ),
    )
    print(
        "manifest:",
        manifest_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
