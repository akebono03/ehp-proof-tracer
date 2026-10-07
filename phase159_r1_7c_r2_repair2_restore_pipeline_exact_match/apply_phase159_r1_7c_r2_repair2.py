from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
PRE_R2_BACKUP = (
  ROOT
  / "phase159_r1_7c_r2_backup_before_apply"
  / "toda_group_proof_narrative_renderer.py"
)
TEST = ROOT / "tests" / "test_phase159_r1_7c_r2_repair2_restore_pipeline.py"
BACKUP_DIR = ROOT / "phase159_r1_7c_r2_repair2_backup_before_apply"

HELPERS = 'def _phase159_r1_7c_inline_math_content(\n  line: str,\n) -> str | None:\n  if line.count(\n    "$"\n  ) != 2:\n    return None\n\n  math_start = line.find(\n    "$"\n  )\n  math_end = line.find(\n    "$",\n    math_start + 1,\n  )\n\n  if (\n    math_start < 0\n    or math_end < 0\n  ):\n    return None\n\n  content = line[\n    math_start + 1:\n    math_end\n  ]\n\n  tag_number = (\n    _phase158_public_equation_tag_number(\n      content\n    )\n  )\n\n  if tag_number is not None:\n    content = content.replace(\n      (\n        r"\\tag{"\n        + str(\n          tag_number\n        )\n        + "}"\n      ),\n      "",\n      1,\n    )\n\n  return content.strip()\n\n\ndef _phase159_r1_7c_rendered_step_math_content(\n  proof_step: ProofStep,\n) -> str | None:\n  rendered = (\n    _render_generic_narrative_step(\n      proof_step\n    )\n  )\n\n  if (\n    not rendered\n    or rendered.count(\n      "$"\n    )\n    != 2\n  ):\n    return None\n\n  math_start = rendered.find(\n    "$"\n  )\n  math_end = rendered.find(\n    "$",\n    math_start + 1,\n  )\n\n  if (\n    math_start < 0\n    or math_end < 0\n  ):\n    return None\n\n  return rendered[\n    math_start + 1:\n    math_end\n  ].strip()\n\n\ndef _phase159_r1_7c_exact_step_line_indices(\n  proof_body: list[\n    str\n  ],\n  proof_step: ProofStep,\n) -> tuple[\n  int,\n  ...,\n]:\n  expected = (\n    _phase159_r1_7c_rendered_step_math_content(\n      proof_step\n    )\n  )\n\n  if expected is None:\n    return ()\n\n  return tuple(\n    index\n    for index, line in enumerate(\n      proof_body\n    )\n    if (\n      _phase159_r1_7c_inline_math_content(\n        line\n      )\n      == expected\n    )\n  )\n\n\ndef _phase159_r1_7c_equality_transitivity_chain_latex(\n  proof_step: ProofStep,\n) -> str | None:\n  conclusion = proof_step.conclusion\n  inference_rule = proof_step.inference_rule\n\n  if (\n    inference_rule is None\n    or inference_rule.name\n    != "equality transitivity"\n    or not isinstance(\n      conclusion,\n      Relation,\n    )\n    or conclusion.relation_type\n    is not RelationType.EQUALITY\n    or len(\n      proof_step.premises\n    )\n    != 2\n  ):\n    return None\n\n  first_step, second_step = (\n    proof_step.premises\n  )\n  first = first_step.conclusion\n  second = second_step.conclusion\n\n  if (\n    not isinstance(\n      first,\n      Relation,\n    )\n    or first.relation_type\n    is not RelationType.EQUALITY\n    or not isinstance(\n      second,\n      Relation,\n    )\n    or second.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return None\n\n  if (\n    first.lhs == conclusion.lhs\n    and first.rhs == second.lhs\n    and second.rhs == conclusion.rhs\n  ):\n    middle = first.rhs\n  elif (\n    second.lhs == conclusion.lhs\n    and second.rhs == first.lhs\n    and first.rhs == conclusion.rhs\n  ):\n    middle = second.rhs\n  else:\n    return None\n\n  try:\n    return (\n      render_toda_expression_latex(\n        conclusion.lhs\n      )\n      + " = "\n      + render_toda_expression_latex(\n        middle\n      )\n      + " = "\n      + render_toda_expression_latex(\n        conclusion.rhs\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return None\n\n\ndef _phase159_r1_7c_reference_prefix(\n  line: str,\n) -> str:\n  math_start = line.find(\n    "$"\n  )\n\n  if math_start < 0:\n    return ""\n\n  prefix = line[\n    :math_start\n  ]\n\n  if (\n    prefix.endswith(\n      "より, "\n    )\n    or prefix.endswith(\n      "より,"\n    )\n  ):\n    return prefix\n\n  return ""\n\n\ndef _phase159_r1_7c_equation_number_reused(\n  proof_body: list[\n    str\n  ],\n  number: int,\n  ignored_indices: frozenset[\n    int\n  ],\n) -> bool:\n  marker = (\n    "("\n    + str(\n      number\n    )\n    + ")"\n  )\n\n  return any(\n    marker in line\n    for index, line in enumerate(\n      proof_body\n    )\n    if index not in ignored_indices\n  )\n\n\ndef _phase159_r1_7c_collapse_equality_transitivity_chains(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  result = list(\n    proof_body\n  )\n\n  for node in semantic_presentation.nodes:\n    proof_step = node.proof_step\n    chain_latex = (\n      _phase159_r1_7c_equality_transitivity_chain_latex(\n        proof_step\n      )\n    )\n\n    if chain_latex is None:\n      continue\n\n    first_step, second_step = (\n      proof_step.premises\n    )\n    first = first_step.conclusion\n    second = second_step.conclusion\n    conclusion = proof_step.conclusion\n\n    if (\n      first.lhs == conclusion.lhs\n      and first.rhs == second.lhs\n      and second.rhs == conclusion.rhs\n    ):\n      ordered_steps = (\n        first_step,\n        second_step,\n      )\n    elif (\n      second.lhs == conclusion.lhs\n      and second.rhs == first.lhs\n      and first.rhs == conclusion.rhs\n    ):\n      ordered_steps = (\n        second_step,\n        first_step,\n      )\n    else:\n      continue\n\n    first_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        ordered_steps[\n          0\n        ],\n      )\n    )\n    second_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        ordered_steps[\n          1\n        ],\n      )\n    )\n    conclusion_indices = (\n      _phase159_r1_7c_exact_step_line_indices(\n        result,\n        proof_step,\n      )\n    )\n\n    if (\n      len(\n        first_indices\n      )\n      != 1\n      or len(\n        second_indices\n      )\n      != 1\n      or len(\n        conclusion_indices\n      )\n      != 1\n    ):\n      continue\n\n    first_index = first_indices[\n      0\n    ]\n    second_index = second_indices[\n      0\n    ]\n    conclusion_index = (\n      conclusion_indices[\n        0\n      ]\n    )\n\n    if not (\n      first_index\n      < second_index\n      < conclusion_index\n    ):\n      continue\n\n    first_number = (\n      _phase158_public_equation_tag_number(\n        result[\n          first_index\n        ]\n      )\n    )\n    second_number = (\n      _phase158_public_equation_tag_number(\n        result[\n          second_index\n        ]\n      )\n    )\n\n    if (\n      first_number is None\n      or second_number is None\n    ):\n      continue\n\n    connector_indices = tuple(\n      index\n      for index in range(\n        second_index + 1,\n        conclusion_index,\n      )\n      if (\n        _phase158_public_equation_connector_numbers(\n          result[\n            index\n          ]\n        )\n        == (\n          first_number,\n          second_number,\n        )\n      )\n    )\n\n    if len(\n      connector_indices\n    ) != 1:\n      continue\n\n    connector_index = (\n      connector_indices[\n        0\n      ]\n    )\n    local_indices = frozenset(\n      (\n        first_index,\n        second_index,\n        connector_index,\n        conclusion_index,\n      )\n    )\n\n    if (\n      _phase159_r1_7c_equation_number_reused(\n        result,\n        first_number,\n        local_indices,\n      )\n      or _phase159_r1_7c_equation_number_reused(\n        result,\n        second_number,\n        local_indices,\n      )\n    ):\n      continue\n\n    allowed_nonblank_indices = {\n      first_index,\n      second_index,\n      connector_index,\n      conclusion_index,\n    }\n\n    if any(\n      result[\n        index\n      ].strip()\n      and index\n      not in allowed_nonblank_indices\n      for index in range(\n        first_index,\n        conclusion_index + 1,\n      )\n    ):\n      continue\n\n    prefix = (\n      _phase159_r1_7c_reference_prefix(\n        result[\n          first_index\n        ]\n      )\n    )\n    replacement = (\n      prefix\n      + "$"\n      + chain_latex\n      + "$."\n    )\n\n    result[\n      first_index:\n      conclusion_index + 1\n    ] = [\n      replacement,\n    ]\n\n  return (\n    _phase158_normalize_public_equation_numbers(\n      result\n    )\n  )\n\n\ndef _phase159_r1_7c_normalize_public_equality_chains(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "\\n## 証明\\n"\n\n  if proof_marker not in rendered:\n    return rendered\n\n  prefix, proof = rendered.split(\n    proof_marker,\n    1,\n  )\n  proof_lines = proof.rstrip().splitlines()\n\n  normalized_lines = (\n    _phase159_r1_7c_collapse_equality_transitivity_chains(\n      presentation,\n      proof_lines,\n    )\n  )\n\n  return (\n    prefix\n    + proof_marker\n    + "\\n".join(\n      normalized_lines\n    ).rstrip()\n    + "\\n"\n  )\n'
WRAPPER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  return (\n    _phase159_r1_7c_normalize_public_equality_chains(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_CONTENT = 'import inspect\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _phase159_r1_7c_collapse_equality_transitivity_chains,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7c_r2_repair2_pi6_3_collapses_transitivity_chain():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  assert (\n    r"$2\\nu\' = \\eta_{3}\\eta_{4}\\eta_{5} = \\eta_{3}^{3}$."\n    in rendered\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$."\n    not in rendered\n  )\n  assert (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = \\eta_{3}^{3}\\tag{2}$."\n    not in rendered\n  )\n  assert "(1) と (2) より," not in rendered\n\n\ndef test_phase159_r1_7c_r2_repair2_preserves_pi6_map_property_style():\n  rendered = _render(\n    3,\n    3,\n  )\n\n  assert (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ は全射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r2_repair2_preserves_pi11_exactness_and_map_style():\n  rendered = _render(\n    4,\n    7,\n  )\n\n  assert (\n    "\\\\[\\n"\n    r"\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} "\n    r"\\xrightarrow{\\Delta} \\pi_{8}^{2}."\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    r"$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は全射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r2_repair2_helper_has_no_group_special_case():\n  source = inspect.getsource(\n    _phase159_r1_7c_collapse_equality_transitivity_chains\n  )\n\n  forbidden = (\n    "pi6",\n    "(6, 3)",\n    "nu_prime",\n    "ν\'",\n    "Proposition 5.6",\n    "Proposition 5.15",\n  )\n\n  for fragment in forbidden:\n    assert fragment not in source\n'


def function_source(
  source: str,
  function_name: str,
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
    lines[
      target.lineno - 1:
      target.end_lineno
    ]
  )


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


def remove_phase159_r1_7c_functions(
  source: str,
) -> str:
  tree = ast.parse(
    source
  )
  target_names = {
    node.name
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name.startswith(
        "_phase159_r1_7c_"
      )
    )
  }

  for name in sorted(
    target_names
  ):
    source = replace_function(
      source,
      name,
      "",
    )

  return source


def insert_before_render(
  source: str,
  insertion: str,
) -> str:
  tree = ast.parse(
    source
  )
  target = next(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name
      == "render_toda_group_proof_narrative_markdown"
    )
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

  if not PRE_R2_BACKUP.exists():
    raise RuntimeError(
      "missing pre-R2 renderer backup: "
      + str(
        PRE_R2_BACKUP
      )
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )

  current = RENDERER.read_text(
    encoding="utf-8-sig"
  )
  pre_r2 = PRE_R2_BACKUP.read_text(
    encoding="utf-8-sig"
  )

  preexisting_render = function_source(
    pre_r2,
    "render_toda_group_proof_narrative_markdown",
  )
  preexisting_render = preexisting_render.replace(
    "def render_toda_group_proof_narrative_markdown(",
    (
      "def "
      "_phase159_r1_7c_preexisting_"
      "render_toda_group_proof_narrative_markdown("
    ),
    1,
  )

  current = remove_phase159_r1_7c_functions(
    current
  )
  current = replace_function(
    current,
    "render_toda_group_proof_narrative_markdown",
    (
      preexisting_render.rstrip()
      + "\n\n"
      + WRAPPER.rstrip()
    ),
  )
  current = insert_before_render(
    current,
    HELPERS,
  )

  ast.parse(
    current
  )

  RENDERER.write_text(
    current,
    encoding="utf-8",
  )
  TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7c R2 repair2 applied."
  )
  print(
    "Pre-R2 public renderer pipeline restored from backup."
  )
  print(
    "Equality-chain normalization added as a final wrapper only."
  )
  print(
    "Exact inline-math matching replaces substring matching."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
