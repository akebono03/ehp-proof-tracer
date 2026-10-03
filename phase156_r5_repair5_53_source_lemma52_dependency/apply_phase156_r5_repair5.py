from __future__ import annotations

import ast
import shutil
from pathlib import Path


RULE_FUNCTIONS = (
  "toda_53_nu_prime_lemma52_hopf_inference_rule",
  "toda_53_nu_prime_lemma52_double_inference_rule",
  "toda_53_nu_prime_lemma52_membership_inference_rule",
)

NEW_REASON_SENTENCE = 'def render_toda_group_proof_narrative_reason_sentence(\n  reason: TodaGroupProofNarrativeReason,\n) -> str | None:\n  if not isinstance(\n    reason,\n    TodaGroupProofNarrativeReason,\n  ):\n    raise TypeError(\n      "reason must be a "\n      "TodaGroupProofNarrativeReason"\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .DEFINITION_APPLICABILITY\n  ):\n    application = reason.reference_application\n\n    if application is None or len(application.bindings) != 1:\n      return (\n        "この前提条件を満たすので, "\n        "次の定義を用いる."\n      )\n\n    if len(reason.premise_steps) != 1:\n      return None\n\n    premise_line = _render_generic_narrative_step(\n      reason.premise_steps[0]\n    )\n    if not premise_line:\n      return None\n\n    binding = application.bindings[0]\n    reference_label = application.reference.label\n    formal_latex = render_toda_expression_latex(\n      binding.formal_variable\n    )\n    instantiated_latex = render_toda_expression_latex(\n      binding.instantiated_expression\n    )\n\n    return (\n      f"{premise_line}\\n"\n      "この前提条件のもとで, "\n      f"{reference_label} の "\n      f"${formal_latex}$ を "\n      f"${instantiated_latex}$ として適用する."\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_MAP_PROPERTY\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    exactness_statement = (\n      reason.premise_steps[1].conclusion\n    )\n    window = exactness_statement.window\n    first_map_name = window.first_map.name\n    second_map_name = window.second_map.name\n\n    return (\n      "この完全性と "\n      f"${first_map_name}=0$ より, "\n      f"$\\\\ker {second_map_name}"\n      f"=\\\\operatorname{{Im}}{first_map_name}=0$ "\n      "である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .MULTIPLE_RELATION_TO_ORDER\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    order_statement = reason.premise_steps[0].conclusion\n    equality_statement = reason.premise_steps[1].conclusion\n    ordered_latex = render_toda_expression_latex(order_statement.lhs)\n    target_latex = render_toda_expression_latex(\n      equality_statement.lhs.expression\n    )\n\n    return (\n      f"$\\\\operatorname{{ord}}({ordered_latex})=2$ "\n      f"かつ $2{target_latex}={ordered_latex}$ より, "\n      f"$4{target_latex}=0$ かつ "\n      f"$2{target_latex}\\\\neq0$ である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .FINAL_GROUP_STRUCTURE\n  ):\n    if len(reason.premise_steps) != 7:\n      return None\n\n    left_group_statement = reason.premise_steps[0].conclusion\n    right_group_statement = reason.premise_steps[4].conclusion\n    order_statement = reason.premise_steps[5].conclusion\n    membership_statement = reason.premise_steps[6].conclusion\n\n    left_order = left_group_statement.rhs.order\n    right_order = right_group_statement.rhs.order\n    middle_order = left_order * right_order\n    generator_latex = render_toda_expression_latex(\n      membership_statement.element\n    )\n\n    return (\n      "この短完全列と両端の群の位数より, "\n      f"中央の群の位数は ${left_order}\\\\cdot"\n      f"{right_order}={middle_order}$ である.\\n"\n      f"また, ${generator_latex}$ は中央の群に属し, "\n      f"$\\\\operatorname{{ord}}({generator_latex})"\n      f"={order_statement.rhs}={middle_order}$ であるから, "\n      f"${generator_latex}$ は中央の群を生成する.\\n"\n      "したがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:\n    return (\n      "この完全性, 既知の群構造, および写像の像に関する結果を合わせると, "\n      "対象となる写像の像と核が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:\n    return (\n      "この群構造と写像による移送の結果を合わせると, "\n      "対象の群の位数と写像の単射性が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:\n    return "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "\n\n  return None\n'
NEW_INSERTION_INDEX = 'def _toda_group_proof_narrative_reason_insertion_index(\n  markdown: str,\n  reason: TodaGroupProofNarrativeReason,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> int | None:\n  conclusion_line = _render_generic_narrative_step(\n    reason.conclusion_step\n  )\n  if conclusion_line:\n    conclusion_index = markdown.find(conclusion_line)\n    if conclusion_index >= 0:\n      if (\n        reason.kind\n        is TodaGroupProofNarrativeReasonKind\n        .DEFINITION_APPLICABILITY\n      ):\n        insertion_index = (\n          conclusion_index\n          + len(\n            conclusion_line\n          )\n        )\n        while (\n          insertion_index\n          < len(\n            markdown\n          )\n          and markdown[\n            insertion_index\n          ] == "\\n"\n        ):\n          insertion_index += 1\n\n        return insertion_index\n\n      return conclusion_index\n\n  children_by_step_id = {}\n  for edge in reason_sidecar.presentation.edges:\n    children_by_step_id.setdefault(\n      id(edge.premise_step),\n      [],\n    ).append(edge.parent_step)\n\n  queue = list(\n    children_by_step_id.get(\n      id(reason.conclusion_step),\n      (),\n    )\n  )\n  visited_step_ids = {\n    id(reason.conclusion_step),\n  }\n\n  while queue:\n    next_queue = []\n    for proof_step in queue:\n      proof_step_id = id(proof_step)\n      if proof_step_id in visited_step_ids:\n        continue\n      visited_step_ids.add(proof_step_id)\n\n      rendered_line = _render_generic_narrative_step(\n        proof_step\n      )\n      if rendered_line:\n        rendered_index = markdown.find(rendered_line)\n        if rendered_index >= 0:\n          return rendered_index\n\n      next_queue.extend(\n        children_by_step_id.get(\n          proof_step_id,\n          (),\n        )\n      )\n    queue = next_queue\n\n  return None\n'
NEW_PHASE150_TEST = 'def test_phase150_rc4_5b_3_renderer_uses_typed_reference_and_binding():\n  presentation, semantic_sidecar, reason_sidecar = _pi6_data()\n  sentence = render_toda_group_proof_narrative_reason_sentence(\n    reason_sidecar.reasons[0]\n  )\n  assert sentence == (\n    "$2\\\\eta_{3} = 0$\\n"\n    "この前提条件のもとで, "\n    "Lemma 5.2 の $\\\\beta$ を $\\\\nu\'$ として適用する."\n  )\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  toda_53_nu_prime_lemma52_double_inference_rule,\n  toda_53_nu_prime_lemma52_hopf_inference_rule,\n  toda_53_nu_prime_lemma52_membership_inference_rule,\n)\n\n\ndef _pi6_3_data(\n  depth: int = 2,\n):\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  sidecar = build_toda_group_proof_narrative_semantic_sidecar(\n    presentation\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n  return presentation, sidecar, rendered\n\n\ndef test_phase156_r5_repair5_53_is_source_for_lemma52_specialization_consequences():\n  rules = (\n    toda_53_nu_prime_lemma52_hopf_inference_rule(),\n    toda_53_nu_prime_lemma52_double_inference_rule(),\n    toda_53_nu_prime_lemma52_membership_inference_rule(),\n  )\n\n  for rule in rules:\n    reference = rule.literature_reference\n    assert reference is not None\n    assert reference.label == "Toda (5.3)"\n    assert reference.locator == "(5.3)"\n\n\ndef test_phase156_r5_repair5_lemma52_remains_internal_reference_application():\n  presentation, sidecar, rendered = _pi6_3_data()\n\n  assert len(\n    sidecar.reference_application_semantics\n  ) == 1\n  application = (\n    sidecar.reference_application_semantics[\n      0\n    ]\n  )\n  assert application.reference.label == "Lemma 5.2"\n\n\ndef test_phase156_r5_repair5_reference_section_uses_53_not_lemma52():\n  presentation, sidecar, rendered = _pi6_3_data()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n\n  assert "(5.3)" in reference_part\n  assert "Lemma 5.2.**" not in reference_part\n\n\ndef test_phase156_r5_repair5_body_places_53_membership_before_lemma52_application():\n  presentation, sidecar, rendered = _pi6_3_data()\n  body = "まず" + rendered.split(\n    "まず",\n    1,\n  )[1]\n\n  bracket = (\n    "$\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}$"\n  )\n  precondition = "$2\\\\eta_{3} = 0$"\n  application = (\n    "この前提条件のもとで, "\n    "Lemma 5.2 の $\\\\beta$ を $\\\\nu\'$ として適用する."\n  )\n\n  assert bracket in body\n  assert precondition in body\n  assert application in body\n  assert body.index(\n    bracket\n  ) < body.index(\n    precondition\n  ) < body.index(\n    application\n  )\n'


def _function_source(
  text: str,
  function: ast.FunctionDef,
) -> str:
  lines = text.splitlines(
    keepends=True
  )
  return "".join(
    lines[
      function.lineno - 1:
      function.end_lineno
    ]
  )


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

  old_source = _function_source(
    text,
    function,
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
  end = start + len(
    old_source
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


def patch_toda_rules(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = repo_root / "toda_rules.py"
  text = path.read_text(
    encoding="utf-8-sig"
  )
  tree = ast.parse(
    text
  )
  functions = {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  updated = text

  for function_name in RULE_FUNCTIONS:
    function = functions.get(
      function_name
    )
    if function is None:
      raise RuntimeError(
        "missing function: "
        + function_name
      )

    function_text = _function_source(
      text,
      function,
    )

    old = (
      'literature_reference=LiteratureReference(\n'
      '      label="Toda Lemma 5.2",\n'
      '      author="H. Toda",\n'
      '      title="Composition Methods in Homotopy Groups of Spheres",\n'
      '      year=1962,\n'
      '      locator="Lemma 5.2",\n'
      '    ),'
    )
    new = (
      'literature_reference=LiteratureReference(\n'
      '      label="Toda (5.3)",\n'
      '      author="H. Toda",\n'
      '      title="Composition Methods in Homotopy Groups of Spheres",\n'
      '      year=1962,\n'
      '      locator="(5.3)",\n'
      '    ),'
    )

    if new in function_text:
      continue

    if old not in function_text:
      raise RuntimeError(
        function_name
        + ": expected repair2 Lemma 5.2 reference block was not found"
      )

    new_function_text = function_text.replace(
      old,
      new,
      1,
    )
    updated = updated.replace(
      function_text,
      new_function_text,
      1,
    )

  backup_dir = package_dir / "backup_before_apply"
  backup_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_dir / path.name,
  )

  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  updated_tree = ast.parse(
    updated
  )
  updated_functions = {
    node.name: node
    for node in updated_tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }
  output = []
  for function_name in RULE_FUNCTIONS:
    output.append(
      _function_source(
        updated,
        updated_functions[
          function_name
        ],
      )
    )
    output.append(
      "\n\n"
    )

  (
    package_dir
    / "changed_toda_rule_functions_after.txt"
  ).write_text(
    "".join(
      output
    ),
    encoding="utf-8",
  )

  print(
    "Updated toda_rules.py:"
  )
  for function_name in RULE_FUNCTIONS:
    print(
      "  "
      + function_name
      + " source attribution -> Toda (5.3)"
    )


def patch_reason_renderer(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_group_proof_narrative_reason_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "render_toda_group_proof_narrative_reason_sentence",
    NEW_REASON_SENTENCE,
  )
  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_reason_insertion_index",
    NEW_INSERTION_INDEX,
  )

  backup_dir = package_dir / "backup_before_apply"
  backup_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_dir / path.name,
  )

  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  (
    package_dir
    / "changed_reason_renderer_functions_after.txt"
  ).write_text(
    NEW_REASON_SENTENCE
    + "\n\n"
    + NEW_INSERTION_INDEX,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_reason_renderer.py"
  )


def patch_phase150_test(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase150_rc4_5b_3_reference_binding.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "test_phase150_rc4_5b_3_renderer_uses_typed_reference_and_binding",
    NEW_PHASE150_TEST,
  )

  backup_dir = package_dir / "backup_before_apply"
  backup_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_dir / path.name,
  )

  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  (
    package_dir
    / "changed_phase150_test_after.txt"
  ).write_text(
    NEW_PHASE150_TEST,
    encoding="utf-8",
  )

  print(
    "Updated tests/test_phase150_rc4_5b_3_reference_binding.py"
  )


def write_focused_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair5_53_source_lemma52_dependency.py"
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

  patch_toda_rules(
    repo_root,
    package_dir,
  )
  patch_reason_renderer(
    repo_root,
    package_dir,
  )
  patch_phase150_test(
    repo_root,
    package_dir,
  )
  write_focused_test(
    repo_root
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
