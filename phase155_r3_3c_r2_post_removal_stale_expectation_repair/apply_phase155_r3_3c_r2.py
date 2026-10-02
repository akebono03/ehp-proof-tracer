
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGETS = (
    (
        Path("tests/test_phase132_9_web_group_proof_modes.py"),
        "test_phase132_9_narrative_web_adapter_preserves_math",
        """def test_phase132_9_narrative_web_adapter_preserves_math():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=2,
      mode="narrative",
    )
  )

  latex_values = tuple(
    line.statement_latex
    for line in view.rendered_lines
    if line.statement_latex is not None
  )

  assert (
    r"\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}"
    in latex_values
  )

  assert (
    view.theorem
    == "Toda Proposition 5.15"
  )
""",
    ),
    (
        Path("tests/test_phase143_55b_conclusion_step_ordering.py"),
        "test_phase143_55b_pi6_3_auxiliary_order_precedes_main_order",
        """def test_phase143_55b_pi6_3_auxiliary_order_precedes_main_order():
  rendered = _render(
    3,
    3,
  )

  auxiliary = (
    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2$"
  )
  connector = "以上より, "
  conclusion = (
    r"$\\operatorname{ord}\\left(\\nu'\\right) = 4$"
  )

  assert auxiliary in rendered
  assert conclusion in rendered
  assert (
    rendered.index(
      auxiliary
    )
    < rendered.index(
      connector,
      rendered.index(
        auxiliary
      ),
    )
    < rendered.index(
      conclusion
    )
  )
""",
    ),
    (
        Path("tests/test_phase143_55b_conclusion_step_ordering.py"),
        "test_phase143_55b_pi8_5_auxiliary_order_precedes_main_order",
        """def test_phase143_55b_pi8_5_auxiliary_order_precedes_main_order():
  rendered = _render(
    5,
    3,
  )

  auxiliary = (
    r"$\\operatorname{ord}\\left(E^{2}\\nu'\\right) = 4$"
  )
  conclusion = (
    r"$\\operatorname{ord}\\left(\\nu_{5}\\right) = 8$"
  )

  assert auxiliary in rendered
  assert conclusion in rendered
  assert (
    rendered.index(
      auxiliary
    )
    < rendered.index(
      "以上より, ",
      rendered.index(
        auxiliary
      ),
    )
    < rendered.index(
      conclusion
    )
  )
""",
    ),
)


def _find_function(tree: ast.Module, function_name: str) -> ast.FunctionDef:
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == function_name
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one top-level function {function_name}, found {len(matches)}"
        )
    return matches[0]


def _replace_functions_in_file(
    path: Path,
    replacements: list[tuple[str, str]],
) -> None:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    spans = []

    for function_name, replacement in replacements:
        function = _find_function(tree, function_name)
        decorator_lines = [d.lineno for d in function.decorator_list]
        start = min([function.lineno, *decorator_lines]) - 1
        end = function.end_lineno or function.lineno
        spans.append((start, end, replacement))

    for start, end, replacement in sorted(
        spans,
        reverse=True,
        key=lambda item: item[0],
    ):
        lines[start:end] = [replacement]

    new_source = "".join(lines)
    ast.parse(new_source)
    path.write_text(new_source, encoding="utf-8")


def main() -> int:
    repo_root = Path.cwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = (
        repo_root.parent
        / f"{repo_root.name}_phase155_r3_3c_r2_backup_{timestamp}"
    )

    replacements_by_file: dict[Path, list[tuple[str, str]]] = {}
    for relative_path, function_name, replacement in TARGETS:
        replacements_by_file.setdefault(relative_path, []).append(
            (function_name, replacement)
        )

    for relative_path, replacements in replacements_by_file.items():
        source_path = repo_root / relative_path
        if not source_path.exists():
            raise RuntimeError(f"target test file not found: {source_path}")

        backup_path = backup_root / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, backup_path)

        _replace_functions_in_file(
            source_path,
            replacements,
        )

    print("Phase 155-R3-3C-r2 stale expectation repair applied.")
    print("backup:", backup_root)
    print("production changes: none")
    print("existing test files changed: 2")
    print("existing test functions changed: 3")
    print("import changes: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
