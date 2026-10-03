from __future__ import annotations

import ast
import shutil
from pathlib import Path


IMPORT_OLD = 'from toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\n'
IMPORT_NEW = 'from toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_expression_latex,\n  _render_generic_narrative_step,\n)\n'
REASON_FUNCTION = 'def render_toda_group_proof_narrative_reason_sentence(\n  reason: TodaGroupProofNarrativeReason,\n) -> str | None:\n  if not isinstance(\n    reason,\n    TodaGroupProofNarrativeReason,\n  ):\n    raise TypeError(\n      "reason must be a "\n      "TodaGroupProofNarrativeReason"\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .DEFINITION_APPLICABILITY\n  ):\n    application = reason.reference_application\n\n    if application is None or len(application.bindings) != 1:\n      return (\n        "この前提条件を満たすので, "\n        "次の定義を用いる."\n      )\n\n    binding = application.bindings[0]\n    reference_label = application.reference.label\n    formal_latex = render_toda_expression_latex(\n      binding.formal_variable\n    )\n    instantiated_latex = render_toda_expression_latex(\n      binding.instantiated_expression\n    )\n\n    return (\n      "この前提条件を満たすので, "\n      f"{reference_label} を適用できる.\\n"\n      f"{reference_label} の "\n      f"${formal_latex}$ を "\n      f"${instantiated_latex}$ と定めると, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_MAP_PROPERTY\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    exactness_statement = (\n      reason.premise_steps[1].conclusion\n    )\n    window = exactness_statement.window\n    first_map_name = window.first_map.name\n    second_map_name = window.second_map.name\n\n    return (\n      "この完全性と "\n      f"${first_map_name}=0$ より, "\n      f"$\\\\ker {second_map_name}"\n      f"=\\\\operatorname{{Im}}{first_map_name}=0$ "\n      "である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .MULTIPLE_RELATION_TO_ORDER\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    order_statement = reason.premise_steps[0].conclusion\n    equality_statement = reason.premise_steps[1].conclusion\n    ordered_latex = (\n      _render_generic_narrative_expression_latex(\n        order_statement.lhs\n      )\n    )\n    target_latex = (\n      _render_generic_narrative_expression_latex(\n        equality_statement.lhs.expression\n      )\n    )\n\n    return (\n      f"$\\\\operatorname{{ord}}({ordered_latex})=2$ "\n      f"かつ $2{target_latex}={ordered_latex}$ より, "\n      f"$4{target_latex}=0$ かつ "\n      f"$2{target_latex}\\\\neq0$ である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .FINAL_GROUP_STRUCTURE\n  ):\n    if len(reason.premise_steps) != 7:\n      return None\n\n    left_group_statement = reason.premise_steps[0].conclusion\n    right_group_statement = reason.premise_steps[4].conclusion\n    order_statement = reason.premise_steps[5].conclusion\n    membership_statement = reason.premise_steps[6].conclusion\n\n    left_order = left_group_statement.rhs.order\n    right_order = right_group_statement.rhs.order\n    middle_order = left_order * right_order\n    generator_latex = render_toda_expression_latex(\n      membership_statement.element\n    )\n\n    return (\n      "この短完全列と両端の群の位数より, "\n      f"中央の群の位数は ${left_order}\\\\cdot"\n      f"{right_order}={middle_order}$ である.\\n"\n      f"また, ${generator_latex}$ は中央の群に属し, "\n      f"$\\\\operatorname{{ord}}({generator_latex})"\n      f"={order_statement.rhs}={middle_order}$ であるから, "\n      f"${generator_latex}$ は中央の群を生成する.\\n"\n      "したがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:\n    return (\n      "この完全性, 既知の群構造, および写像の像に関する結果を合わせると, "\n      "対象となる写像の像と核が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:\n    return (\n      "この群構造と写像による移送の結果を合わせると, "\n      "対象の群の位数と写像の単射性が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:\n    return "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "\n\n  return None\n'
FOCUSED_TEST = 'import inspect\n\nfrom tests.test_phase143_19_method_evidence import (\n  _method_evidence_data,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_reason_renderer import (\n  render_toda_group_proof_narrative_reason_sentence,\n)\nfrom toda_group_proof_narrative_reasons import (\n  TodaGroupProofNarrativeReasonKind,\n  build_toda_group_proof_narrative_reason_sidecar,\n)\n\n\ndef _pi6_reason_data():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n  ) = _method_evidence_data(\n    3,\n    3,\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .MULTIPLE_RELATION_TO_ORDER\n    )\n  )\n  return (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason,\n  )\n\n\ndef test_phase156_r6_3_reason_sentence_uses_canonical_eta_cube():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason,\n  ) = _pi6_reason_data()\n\n  sentence = render_toda_group_proof_narrative_reason_sentence(\n    reason\n  )\n\n  assert sentence is not None\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$"\n    in sentence\n  )\n  assert (\n    r"$2\\nu\'=\\eta_{3}^{3}$"\n    in sentence\n  )\n  assert (\n    r"\\operatorname{ord}(\\eta_{3}\\eta_{4}\\eta_{5})"\n    not in sentence\n  )\n  assert (\n    r"2\\nu\'=\\eta_{3}\\eta_{4}\\eta_{5}"\n    not in sentence\n  )\n\n\ndef test_phase156_r6_3_public_reason_prose_matches_canonical_equation3():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason,\n  ) = _pi6_reason_data()\n\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  equation_three = (\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$"\n  )\n  canonical_reason = (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n  )\n\n  assert equation_three in rendered\n  assert canonical_reason in rendered\n  assert (\n    rendered.index(\n      equation_three\n    )\n    < rendered.index(\n      canonical_reason\n    )\n  )\n\n\ndef test_phase156_r6_3_reason_renderer_has_no_pi6_specific_branch():\n  import toda_group_proof_narrative_reason_renderer as module\n\n  source = inspect.getsource(\n    module\n  )\n\n  forbidden_fragments = (\n    "(6, 3)",\n    "pi6",\n    "nu_prime",\n    "ν′",\n    "Proposition 5.6",\n  )\n\n  for fragment in forbidden_fragments:\n    assert fragment not in source\n'


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
  relative: Path,
  repo_root: Path,
  package_dir: Path,
) -> None:
  source = (
    repo_root
    / relative
  )
  destination = (
    package_dir
    / "backup_before_apply"
    / relative
  )
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    source,
    destination,
  )


def patch_reason_renderer(
  repo_root: Path,
  package_dir: Path,
) -> None:
  relative = Path(
    "toda_group_proof_narrative_reason_renderer.py"
  )
  path = (
    repo_root
    / relative
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )

  if IMPORT_OLD in text:
    updated = text.replace(
      IMPORT_OLD,
      IMPORT_NEW,
      1,
    )
  elif IMPORT_NEW in text:
    updated = text
  else:
    raise RuntimeError(
      "generic narrative renderer import block not found"
    )

  updated = _replace_function(
    updated,
    "render_toda_group_proof_narrative_reason_sentence",
    REASON_FUNCTION,
  )

  _backup(
    relative,
    repo_root,
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
    "Updated toda_group_proof_narrative_reason_renderer.py"
  )
  print(
    "  MULTIPLE_RELATION_TO_ORDER now uses canonical expression rendering"
  )


def write_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r6_3_reason_prose_canonicalization.py"
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

  patch_reason_renderer(
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
