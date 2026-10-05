from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair47_injective_image_order_reason.py"
)

NEW_HELPER = 'def _injective_image_order_reason(\n  proof_step: ProofStep,\n) -> TodaGroupProofNarrativeReason | None:\n  conclusion = proof_step.conclusion\n\n  if (\n    not isinstance(\n      conclusion,\n      Relation,\n    )\n    or conclusion.relation_type\n    is not RelationType.ORDER\n  ):\n    return None\n\n  group_premises = tuple(\n    premise\n    for premise in proof_step.premises\n    if (\n      isinstance(\n        premise.conclusion,\n        Relation,\n      )\n      and premise.conclusion.relation_type\n      is RelationType.EQUALITY\n      and isinstance(\n        premise.conclusion.rhs,\n        FiniteCyclicGroup,\n      )\n    )\n  )\n  injective_premises = tuple(\n    premise\n    for premise in proof_step.premises\n    if isinstance(\n      premise.conclusion,\n      TodaSuspensionInjectiveStatement,\n    )\n  )\n\n  compatible_pairs = []\n\n  for group_premise in group_premises:\n    group_statement = group_premise.conclusion\n    source_group = group_statement.lhs\n    finite_group = group_statement.rhs\n\n    if (\n      finite_group.order\n      != conclusion.rhs\n    ):\n      continue\n\n    for injective_premise in injective_premises:\n      injective_statement = (\n        injective_premise.conclusion\n      )\n\n      if (\n        injective_statement.map.source_group\n        != source_group\n      ):\n        continue\n\n      compatible_pairs.append(\n        (\n          group_premise,\n          injective_premise,\n        )\n      )\n\n  if len(\n    compatible_pairs\n  ) != 1:\n    return None\n\n  group_premise, injective_premise = (\n    compatible_pairs[\n      0\n    ]\n  )\n\n  return TodaGroupProofNarrativeReason(\n    kind=(\n      TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    ),\n    premise_steps=(\n      group_premise,\n      injective_premise,\n    ),\n    conclusion_step=proof_step,\n  )\n'
RENDERER_CASE = '  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .INJECTIVE_IMAGE_ORDER\n  ):\n    if len(\n      reason.premise_steps\n    ) != 2:\n      return None\n\n    group_statement = (\n      reason.premise_steps[\n        0\n      ].conclusion\n    )\n    injective_statement = (\n      reason.premise_steps[\n        1\n      ].conclusion\n    )\n    order_statement = (\n      reason.conclusion_step.conclusion\n    )\n\n    finite_group = group_statement.rhs\n    source_generator_latex = (\n      _render_generic_narrative_expression_latex(\n        finite_group.generator\n      )\n    )\n    target_latex = (\n      _render_generic_narrative_expression_latex(\n        order_statement.lhs\n      )\n    )\n    order = finite_group.order\n\n    if (\n      not source_generator_latex\n      or not target_latex\n    ):\n      return None\n\n    if (\n      type(\n        injective_statement.map\n      ).__name__\n      not in (\n        "TodaSuspensionMap",\n        "TodaIteratedSuspensionMap",\n      )\n    ):\n      return None\n\n    return (\n      "この群構造と $E$ の単射性より, "\n      f"$E({source_generator_latex})"\n      f"={target_latex}\\\\neq0$ であり, "\n      "単射写像は元の位数を保つ.\\n"\n      "したがって, "\n    )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_reason_renderer import (\n  render_toda_group_proof_narrative_reason_sentence,\n)\nfrom toda_group_proof_narrative_reasons import (\n  TodaGroupProofNarrativeReasonKind,\n  build_toda_group_proof_narrative_reason_sidecar,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\nTARGET = (\n  r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2$"\n)\n\n\ndef _repair47_data():\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  semantic_sidecar = (\n    build_toda_group_proof_narrative_semantic_sidecar(\n      presentation\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n\n  return (\n    raw,\n    presentation,\n    reason_sidecar,\n  )\n\n\ndef test_phase157_r20_repair47_eta_order_gets_generic_injective_image_reason():\n  (\n    raw,\n    presentation,\n    reason_sidecar,\n  ) = _repair47_data()\n\n  target_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      _render_generic_narrative_step(\n        node.proof_step\n      )\n      == TARGET\n    )\n  )\n\n  assert len(\n    target_steps\n  ) == 1\n\n  reasons = tuple(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.conclusion_step\n      is target_steps[\n        0\n      ]\n    )\n  )\n\n  matching = tuple(\n    reason\n    for reason in reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    )\n  )\n\n  assert len(\n    matching\n  ) == 1\n  assert len(\n    matching[\n      0\n    ].premise_steps\n  ) == 2\n\n\ndef test_phase157_r20_repair47_reason_sentence_exposes_nonzero_suspension_image():\n  (\n    raw,\n    presentation,\n    reason_sidecar,\n  ) = _repair47_data()\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    )\n  )\n\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n\n  assert sentence is not None\n  assert (\n    r"$E(\\eta_{2}^{3})="\n    r"\\eta_{3}^{3}\\neq0$"\n    in sentence\n  )\n  assert (\n    "単射写像は元の位数を保つ."\n    in sentence\n  )\n\n\ndef test_phase157_r20_repair47_public_narrative_places_reason_before_eta_order():\n  (\n    raw,\n    presentation,\n    reason_sidecar,\n  ) = _repair47_data()\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  body = rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n  reason_text = (\n    "この群構造と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})="\n    r"\\eta_{3}^{3}\\neq0$ であり, "\n    "単射写像は元の位数を保つ."\n  )\n  order_text = (\n    r"$\\operatorname{ord}"\n    r"\\left(\\eta_{3}^{3}\\right) = 2$."\n  )\n\n  assert reason_text in body\n  assert order_text in body\n  assert body.index(\n    reason_text\n  ) < body.index(\n    order_text\n  )\n\n\ndef test_phase157_r20_repair47_existing_nu_prime_order_reason_remains():\n  (\n    raw,\n    presentation,\n    reason_sidecar,\n  ) = _repair47_data()\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  body = rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n    r"$4\\nu\'=0$ かつ $2\\nu\'\\neq0$ である."\n    in body\n  )\n'


def function_range(
  source: str,
  name: str,
) -> tuple[
  int,
  int,
]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )
      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def add_reason_kind(
  source: str,
) -> str:
  old = """  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
  MULTIPLE_RELATION_TO_ORDER = (
"""

  new = """  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
  INJECTIVE_IMAGE_ORDER = (
    "injective_image_order"
  )
  MULTIPLE_RELATION_TO_ORDER = (
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "reason-kind anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def add_reason_helper(
  source: str,
) -> str:
  if (
    "def _injective_image_order_reason("
    in source
  ):
    raise RuntimeError(
      "repair47 helper already exists"
    )

  anchor = (
    "def _multiple_relation_to_order_reason(\n"
  )

  if source.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "reason-helper anchor was not found exactly once"
    )

  return source.replace(
    anchor,
    NEW_HELPER.rstrip()
    + "\n\n\n"
    + anchor,
    1,
  )


def update_reason_builder(
  source: str,
) -> str:
  old = """    multiple_order_reason = _multiple_relation_to_order_reason(
      node.proof_step
    )
    if multiple_order_reason is not None:
      append_if_visible(multiple_order_reason)

    final_group_structure_reason = _final_group_structure_reason(
"""

  new = """    injective_image_order_reason = (
      _injective_image_order_reason(
        node.proof_step
      )
    )
    if injective_image_order_reason is not None:
      append_if_visible(
        injective_image_order_reason
      )

    multiple_order_reason = _multiple_relation_to_order_reason(
      node.proof_step
    )
    if multiple_order_reason is not None:
      append_if_visible(multiple_order_reason)

    final_group_structure_reason = _final_group_structure_reason(
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "reason-builder anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def update_reason_renderer(
  source: str,
) -> str:
  old = """  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .MULTIPLE_RELATION_TO_ORDER
  ):
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "reason-renderer anchor was not found exactly once"
    )

  return source.replace(
    old,
    RENDERER_CASE.rstrip()
    + "\n\n"
    + old,
    1,
  )


def main() -> int:
  for path in (
    REASONS,
    RENDERER,
  ):
    if not path.is_file():
      raise RuntimeError(
        "Run from repository root."
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair47_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    REASONS,
    backup / REASONS.name,
  )
  shutil.copy2(
    RENDERER,
    backup / RENDERER.name,
  )

  reasons_source = REASONS.read_text(
    encoding="utf-8"
  )
  renderer_source = RENDERER.read_text(
    encoding="utf-8"
  )

  reasons_source = add_reason_kind(
    reasons_source
  )
  reasons_source = add_reason_helper(
    reasons_source
  )
  reasons_source = update_reason_builder(
    reasons_source
  )
  renderer_source = update_reason_renderer(
    renderer_source
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  combined = (
    reasons_source
    + "\n"
    + renderer_source
  )

  for token in forbidden:
    if token in combined:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    reasons_source,
    str(
      REASONS
    ),
    "exec",
  )
  compile(
    renderer_source,
    str(
      RENDERER
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  REASONS.write_text(
    reasons_source,
    encoding="utf-8",
    newline="\n",
  )
  RENDERER.write_text(
    renderer_source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair47 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    REASONS,
  )
  print(
    "Changed production file:",
    RENDERER,
  )
  print(
    "Added test:",
    TEST,
  )
  print("")
  print(
    "Import changes: none"
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      combined.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
