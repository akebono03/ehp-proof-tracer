from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_7c_r2_repair6_semantic_rendered_equality_chain.py"
BACKUP_DIR = ROOT / "phase159_r1_7c_r2_repair6_backup_before_apply"

NEW_HELPER = 'def _phase159_r1_7c_rendered_equality_parts(\n  proof_step: ProofStep,\n) -> tuple[\n  str,\n  str,\n] | None:\n  content = (\n    _phase159_r1_7c_rendered_step_math_content(\n      proof_step\n    )\n  )\n\n  if (\n    content is None\n    or content.count(\n      " = "\n    )\n    != 1\n  ):\n    return None\n\n  left, right = content.split(\n    " = ",\n    1,\n  )\n\n  if (\n    not left\n    or not right\n  ):\n    return None\n\n  return (\n    left,\n    right,\n  )\n'
NEW_CHAIN = 'def _phase159_r1_7c_equality_transitivity_chain_latex(\n  proof_step: ProofStep,\n) -> str | None:\n  conclusion = proof_step.conclusion\n  inference_rule = proof_step.inference_rule\n\n  if (\n    inference_rule is None\n    or inference_rule.name\n    != "equality transitivity"\n    or not isinstance(\n      conclusion,\n      Relation,\n    )\n    or conclusion.relation_type\n    is not RelationType.EQUALITY\n    or len(\n      proof_step.premises\n    )\n    != 2\n  ):\n    return None\n\n  first_step, second_step = (\n    proof_step.premises\n  )\n  first = first_step.conclusion\n  second = second_step.conclusion\n\n  if (\n    not isinstance(\n      first,\n      Relation,\n    )\n    or first.relation_type\n    is not RelationType.EQUALITY\n    or not isinstance(\n      second,\n      Relation,\n    )\n    or second.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return None\n\n  first_parts = (\n    _phase159_r1_7c_rendered_equality_parts(\n      first_step\n    )\n  )\n  second_parts = (\n    _phase159_r1_7c_rendered_equality_parts(\n      second_step\n    )\n  )\n  conclusion_parts = (\n    _phase159_r1_7c_rendered_equality_parts(\n      proof_step\n    )\n  )\n\n  if (\n    first_parts is None\n    or second_parts is None\n    or conclusion_parts is None\n  ):\n    return None\n\n  first_left, first_right = (\n    first_parts\n  )\n  second_left, second_right = (\n    second_parts\n  )\n  conclusion_left, conclusion_right = (\n    conclusion_parts\n  )\n\n  if (\n    first_left == conclusion_left\n    and first_right == second_left\n    and second_right == conclusion_right\n  ):\n    middle = first_right\n  elif (\n    second_left == conclusion_left\n    and second_right == first_left\n    and first_right == conclusion_right\n  ):\n    middle = second_right\n  else:\n    return None\n\n  if middle == conclusion_right:\n    return None\n\n  return (\n    conclusion_left\n    + " = "\n    + middle\n    + " = "\n    + conclusion_right\n  )\n'
NEW_COLLAPSE = 'def _phase159_r1_7c_collapse_equality_transitivity_chains(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  result = list(\n    proof_body\n  )\n\n  for node in semantic_presentation.nodes:\n    proof_step = node.proof_step\n    chain_latex = (\n      _phase159_r1_7c_equality_transitivity_chain_latex(\n        proof_step\n      )\n    )\n\n    if chain_latex is None:\n      continue\n\n    first_step, second_step = (\n      proof_step.premises\n    )\n\n    first_parts = (\n      _phase159_r1_7c_rendered_equality_parts(\n        first_step\n      )\n    )\n    second_parts = (\n      _phase159_r1_7c_rendered_equality_parts(\n        second_step\n      )\n    )\n    conclusion_parts = (\n      _phase159_r1_7c_rendered_equality_parts(\n        proof_step\n      )\n    )\n\n    if (\n      first_parts is None\n      or second_parts is None\n      or conclusion_parts is None\n    ):\n      continue\n\n    first_left, first_right = (\n      first_parts\n    )\n    second_left, second_right = (\n      second_parts\n    )\n    conclusion_left, conclusion_right = (\n      conclusion_parts\n    )\n\n    if (\n      first_left == conclusion_left\n      and first_right == second_left\n      and second_right == conclusion_right\n    ):\n      ordered_steps = (\n        first_step,\n        second_step,\n      )\n      middle = first_right\n    elif (\n      second_left == conclusion_left\n      and second_right == first_left\n      and first_right == conclusion_right\n    ):\n      ordered_steps = (\n        second_step,\n        first_step,\n      )\n      middle = second_right\n    else:\n      continue\n\n    first_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        ordered_steps[\n          0\n        ],\n      )\n    )\n    second_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        ordered_steps[\n          1\n        ],\n      )\n    )\n    conclusion_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        proof_step,\n      )\n    )\n\n    if (\n      len(\n        first_indices\n      )\n      == 1\n      and len(\n        second_indices\n      )\n      == 1\n      and len(\n        conclusion_indices\n      )\n      == 1\n    ):\n      first_index = first_indices[\n        0\n      ]\n      second_index = second_indices[\n        0\n      ]\n      conclusion_index = (\n        conclusion_indices[\n          0\n        ]\n      )\n\n      if not (\n        first_index\n        < second_index\n        < conclusion_index\n      ):\n        continue\n\n      first_number = (\n        _phase158_public_equation_tag_number(\n          result[\n            first_index\n          ]\n        )\n      )\n      second_number = (\n        _phase158_public_equation_tag_number(\n          result[\n            second_index\n          ]\n        )\n      )\n\n      if (\n        first_number is None\n        or second_number is None\n      ):\n        continue\n\n      connector_indices = tuple(\n        index\n        for index in range(\n          second_index + 1,\n          conclusion_index,\n        )\n        if (\n          _phase158_public_equation_connector_numbers(\n            result[\n              index\n            ]\n          )\n          == (\n            first_number,\n            second_number,\n          )\n        )\n      )\n\n      if len(\n        connector_indices\n      ) != 1:\n        continue\n\n      connector_index = (\n        connector_indices[\n          0\n        ]\n      )\n      local_indices = frozenset(\n        (\n          first_index,\n          second_index,\n          connector_index,\n          conclusion_index,\n        )\n      )\n\n      if (\n        _phase159_r1_7c_equation_number_reused(\n          result,\n          first_number,\n          local_indices,\n        )\n        or _phase159_r1_7c_equation_number_reused(\n          result,\n          second_number,\n          local_indices,\n        )\n      ):\n        continue\n\n      allowed_nonblank_indices = {\n        first_index,\n        second_index,\n        connector_index,\n        conclusion_index,\n      }\n\n      if any(\n        result[\n          index\n        ].strip()\n        and index\n        not in allowed_nonblank_indices\n        for index in range(\n          first_index,\n          conclusion_index + 1,\n        )\n      ):\n        continue\n\n      prefix = (\n        _phase159_r1_7c_reference_prefix(\n          result[\n            first_index\n          ]\n        )\n      )\n      replacement = (\n        prefix\n        + "$"\n        + chain_latex\n        + "$."\n      )\n\n      result[\n        first_index:\n        conclusion_index + 1\n      ] = [\n        replacement,\n      ]\n      continue\n\n    projected_indices = []\n\n    for index, line in enumerate(\n      result\n    ):\n      content = (\n        _phase159_r1_7c_inline_math_content(\n          line\n        )\n      )\n\n      if content is None:\n        continue\n\n      if (\n        content.startswith(\n          conclusion_left\n          + " = "\n        )\n        and content.endswith(\n          " = "\n          + middle\n        )\n      ):\n        projected_indices.append(\n          index\n        )\n        continue\n\n      if content == (\n        conclusion_left\n        + " = "\n        + middle\n      ):\n        projected_indices.append(\n          index\n        )\n\n    if len(\n      projected_indices\n    ) != 1:\n      continue\n\n    projected_index = (\n      projected_indices[\n        0\n      ]\n    )\n    line = result[\n      projected_index\n    ]\n    math_start = line.find(\n      "$"\n    )\n    math_end = line.find(\n      "$",\n      math_start + 1,\n    )\n\n    if (\n      math_start < 0\n      or math_end < 0\n    ):\n      continue\n\n    result[\n      projected_index\n    ] = (\n      line[\n        :math_start + 1\n      ]\n      + chain_latex\n      + line[\n        math_end:\n      ]\n    )\n\n  return (\n    _phase158_normalize_public_equation_numbers(\n      result\n    )\n  )\n'
TEST_CONTENT = 'import inspect\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _phase159_r1_7c_collapse_equality_transitivity_chains,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7c_r2_repair6_pi6_3_uses_public_semantic_chain():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  expected = (\n    r"[R2] より, "\n    r"$2\\nu\' = \\eta_{3}\\eta_{4}\\eta_{5} "\n    r"= \\eta_{3}^{3}$."\n  )\n\n  assert expected in rendered\n  assert (\n    r"\\eta_{3}E\\eta_{3}\\eta_{5}"\n    not in rendered\n  )\n  assert "(1) と (2) より," not in rendered\n\n\ndef test_phase159_r1_7c_r2_repair6_identity_transitivity_stays_compact():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in rendered\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5} = \\eta_{5}$."\n    not in rendered\n  )\n\n\ndef test_phase159_r1_7c_r2_repair6_preserves_pi6_map_property_contract():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  assert (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ は全射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r2_repair6_preserves_pi11_exactness_contract():\n  rendered = _render(\n    4,\n    7,\n  )\n\n  assert (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    r"$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は全射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r2_repair6_has_no_group_or_theorem_special_case():\n  source = inspect.getsource(\n    _phase159_r1_7c_collapse_equality_transitivity_chains\n  )\n\n  forbidden = (\n    "pi6",\n    "(6, 3)",\n    "nu_prime",\n    "ν\'",\n    "Proposition 5.6",\n    "Proposition 5.15",\n  )\n\n  for fragment in forbidden:\n    assert fragment not in source\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  target = next(
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

  if target is None:
    raise RuntimeError(
      f"function not found: {function_name}"
    )

  if target.end_lineno is None:
    raise RuntimeError(
      f"function has no end line: {function_name}"
    )

  lines = source.splitlines(
    keepends=True
  )

  return "".join(
    (
      *lines[
        :target.lineno - 1
      ],
      replacement.rstrip()
      + "\n\n",
      *lines[
        target.end_lineno:
      ],
    )
  )


def insert_before_function(
  source: str,
  function_name: str,
  insertion: str,
) -> str:
  tree = ast.parse(
    source
  )
  target = next(
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

  if target is None:
    raise RuntimeError(
      f"function not found: {function_name}"
    )

  lines = source.splitlines(
    keepends=True
  )

  return "".join(
    (
      *lines[
        :target.lineno - 1
      ],
      insertion.rstrip()
      + "\n\n",
      *lines[
        target.lineno - 1:
      ],
    )
  )


def main() -> int:
  if not RENDERER.exists():
    raise RuntimeError(
      f"missing renderer: {RENDERER}"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  if (
    "def _phase159_r1_7c_rendered_equality_parts("
    not in source
  ):
    source = insert_before_function(
      source,
      "_phase159_r1_7c_equality_transitivity_chain_latex",
      NEW_HELPER,
    )

  source = replace_function(
    source,
    "_phase159_r1_7c_equality_transitivity_chain_latex",
    NEW_CHAIN,
  )
  source = replace_function(
    source,
    "_phase159_r1_7c_collapse_equality_transitivity_chains",
    NEW_COLLAPSE,
  )

  ast.parse(
    source
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
  )
  TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7c R2 repair6 applied."
  )
  print(
    "Public semantic equalities now drive equality-chain composition."
  )
  print(
    "Raw proof expressions remain unchanged."
  )
  print(
    "No group-specific branch added."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
