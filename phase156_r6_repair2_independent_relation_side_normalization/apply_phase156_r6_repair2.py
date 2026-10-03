from __future__ import annotations

import ast
import shutil
from pathlib import Path


NORMALIZE_FUNCTION = 'def _normalize_generic_narrative_step_latex(\n  proof_step: ProofStep,\n  latex: str,\n) -> str:\n  statement = proof_step.conclusion\n\n  if not hasattr(\n    statement,\n    "lhs",\n  ):\n    return latex\n\n  if not hasattr(\n    statement,\n    "rhs",\n  ):\n    return latex\n\n  replacements = []\n  search_start = 0\n\n  for expression in (\n    statement.lhs,\n    statement.rhs,\n  ):\n    rendered_expression = (\n      _try_render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    if rendered_expression is None:\n      continue\n\n    normalized_expression = (\n      _render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    expression_start = latex.find(\n      rendered_expression,\n      search_start,\n    )\n\n    if expression_start < 0:\n      continue\n\n    expression_end = (\n      expression_start\n      + len(\n        rendered_expression\n      )\n    )\n    search_start = expression_end\n\n    if (\n      normalized_expression\n      == rendered_expression\n    ):\n      continue\n\n    replacements.append(\n      (\n        expression_start,\n        expression_end,\n        normalized_expression,\n      )\n    )\n\n  normalized = latex\n\n  for (\n    expression_start,\n    expression_end,\n    normalized_expression,\n  ) in reversed(\n    replacements\n  ):\n    normalized = (\n      normalized[\n        :expression_start\n      ]\n      + normalized_expression\n      + normalized[\n        expression_end:\n      ]\n    )\n\n  return normalized\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_blocks import (\n  TodaGroupProofNarrativeMathematicalBlockRole,\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _data(\n  depth: int = 2,\n):\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  sidecar = build_toda_group_proof_narrative_semantic_sidecar(\n    presentation\n  )\n  blocks = build_toda_group_proof_narrative_blocks(\n    presentation,\n    semantic_sidecar=sidecar,\n  )\n  return (\n    raw,\n    presentation,\n    blocks,\n  )\n\n\ndef test_phase156_r6_repair2_order_relation_normalizes_expression_lhs_with_scalar_rhs():\n  (\n    raw,\n    presentation,\n    blocks,\n  ) = _data()\n\n  order_steps = tuple(\n    proof_step\n    for block in blocks\n    if block.role\n    is TodaGroupProofNarrativeMathematicalBlockRole.ORDER\n    for proof_step in block.steps\n  )\n  eta_order_step = next(\n    proof_step\n    for proof_step in order_steps\n    if proof_step.conclusion.rhs == 2\n  )\n\n  assert (\n    _render_generic_narrative_step(\n      eta_order_step\n    )\n    == (\n      r"$\\operatorname{ord}\\left("\n      r"\\eta_{3}^{3}"\n      r"\\right) = 2$"\n    )\n  )\n\n\ndef test_phase156_r6_repair2_equality_relation_still_keeps_distinct_canonical_sides():\n  (\n    raw,\n    presentation,\n    blocks,\n  ) = _data()\n\n  rendered_steps = tuple(\n    _render_generic_narrative_step(\n      node.proof_step\n    )\n    for node in presentation.nodes\n  )\n\n  assert (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}$"\n    in rendered_steps\n  )\n  assert (\n    r"$\\eta_{3}^{3} = \\eta_{3}^{3}$"\n    not in rendered_steps\n  )\n\n\ndef test_phase156_r6_repair2_public_chain_and_order_are_canonical():\n  (\n    raw,\n    presentation,\n    blocks,\n  ) = _data()\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n\n  equation_one = (\n    r"$2\\nu\' = "\n    r"\\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$"\n  )\n  equation_two = (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n  )\n  connector = "(1) と (2) より,"\n  equation_three = (\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$"\n  )\n  order_statement = (\n    r"$\\operatorname{ord}\\left("\n    r"\\eta_{3}^{3}"\n    r"\\right) = 2$"\n  )\n\n  assert (\n    rendered.index(\n      equation_one\n    )\n    < rendered.index(\n      equation_two\n    )\n    < rendered.index(\n      connector\n    )\n    < rendered.index(\n      equation_three\n    )\n    < rendered.index(\n      order_statement\n    )\n  )\n\n\ndef test_phase156_r6_repair2_public_order_is_not_left_in_expanded_eta_form():\n  (\n    raw,\n    presentation,\n    blocks,\n  ) = _data()\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n\n  assert (\n    r"$\\operatorname{ord}\\left("\n    r"\\eta_{3}\\eta_{4}\\eta_{5}"\n    r"\\right) = 2$"\n    not in rendered\n  )\n'


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
    "  relation sides now normalize independently"
  )


def write_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r6_repair2_independent_relation_side_normalization.py"
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
