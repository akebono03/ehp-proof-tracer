from __future__ import annotations

import ast
import shutil
from pathlib import Path


NORMALIZE_FUNCTION = 'def _normalize_generic_narrative_step_latex(\n  proof_step: ProofStep,\n  latex: str,\n) -> str:\n  statement = proof_step.conclusion\n\n  if not hasattr(\n    statement,\n    "lhs",\n  ):\n    return latex\n\n  if not hasattr(\n    statement,\n    "rhs",\n  ):\n    return latex\n\n  lhs_rendered = (\n    _try_render_generic_narrative_expression_latex(\n      statement.lhs\n    )\n  )\n  rhs_rendered = (\n    _try_render_generic_narrative_expression_latex(\n      statement.rhs\n    )\n  )\n\n  if (\n    lhs_rendered is None\n    or rhs_rendered is None\n  ):\n    return latex\n\n  lhs_normalized = (\n    _render_generic_narrative_expression_latex(\n      statement.lhs\n    )\n  )\n  rhs_normalized = (\n    _render_generic_narrative_expression_latex(\n      statement.rhs\n    )\n  )\n\n  lhs_start = latex.find(\n    lhs_rendered\n  )\n\n  if lhs_start < 0:\n    return latex\n\n  lhs_end = (\n    lhs_start\n    + len(\n      lhs_rendered\n    )\n  )\n  rhs_start = latex.find(\n    rhs_rendered,\n    lhs_end,\n  )\n\n  if rhs_start < 0:\n    return latex\n\n  rhs_end = (\n    rhs_start\n    + len(\n      rhs_rendered\n    )\n  )\n\n  return (\n    latex[\n      :lhs_start\n    ]\n    + lhs_normalized\n    + latex[\n      lhs_end:\n      rhs_start\n    ]\n    + rhs_normalized\n    + latex[\n      rhs_end:\n    ]\n  )\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _depth2_presentations():\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  return (\n    presentation,\n    closure,\n  )\n\n\ndef test_phase156_r6_repair1_equation2_preserves_distinct_lhs_and_rhs():\n  (\n    presentation,\n    closure,\n  ) = _depth2_presentations()\n\n  rendered_steps = tuple(\n    _render_generic_narrative_step(\n      node.proof_step\n    )\n    for node in closure.nodes\n  )\n\n  assert (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}$"\n    in rendered_steps\n  )\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}$"\n    not in rendered_steps\n  )\n\n\ndef test_phase156_r6_repair1_public_numbered_chain_has_canonical_equation2():\n  (\n    presentation,\n    closure,\n  ) = _depth2_presentations()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  assert (\n    r"$2\\nu\' = "\n    r"\\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$"\n    in rendered\n  )\n  assert (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n    in rendered\n  )\n  assert (\n    "(1) と (2) より,"\n    in rendered\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$"\n    in rendered\n  )\n\n\ndef test_phase156_r6_repair1_equation3_is_immediately_after_equation2_derivation():\n  (\n    presentation,\n    closure,\n  ) = _depth2_presentations()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  equation_two = (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n  )\n  connector = "(1) と (2) より,"\n  equation_three = (\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$"\n  )\n  order_statement = (\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2$"\n  )\n\n  assert (\n    rendered.index(\n      equation_two\n    )\n    < rendered.index(\n      connector\n    )\n    < rendered.index(\n      equation_three\n    )\n    < rendered.index(\n      order_statement\n    )\n  )\n'


def _replace_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    text
  )
  function = next(
    (
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
    ),
    None,
  )

  if function is None:
    raise RuntimeError(
      "missing function: "
      + function_name
    )

  lines = text.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :function.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :function.end_lineno
    ]
  )

  return (
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ]
  )


def _backup(
  path: Path,
  package_dir: Path,
) -> None:
  backup_path = (
    package_dir
    / "backup_before_apply"
    / path
  )
  backup_path.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_path,
  )


def patch_production(
  repo_root: Path,
  package_dir: Path,
) -> None:
  relative = Path(
    "toda_group_proof_generic_narrative_renderer.py"
  )
  path = (
    repo_root
    / relative
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "_normalize_generic_narrative_step_latex",
    NORMALIZE_FUNCTION,
  )

  _backup(
    relative,
    package_dir,
  )
  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_generic_narrative_renderer.py"
  )
  print(
    "  lhs/rhs normalization now uses original non-overlapping spans"
  )


def write_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r6_repair1_relation_side_normalization.py"
  )
  path.write_text(
    FOCUSED_TEST,
    encoding="utf-8",
  )

  print(
    "Wrote "
    + str(
      path.relative_to(
        repo_root
      )
    )
  )


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = package_dir.parent

  patch_production(
    repo_root,
    package_dir,
  )
  write_test(
    repo_root
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
