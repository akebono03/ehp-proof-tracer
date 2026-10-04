from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
REASON_RENDERER = (
  ROOT
  / "toda_group_proof_narrative_reason_renderer.py"
)
CONTRIBUTION_RENDERER = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair48_injective_image_reason_ordering.py"
)

NEW_FUNCTION = 'def order_toda_group_proof_narrative_injective_image_order_reason(\n  markdown: str,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reason_sidecar,\n    TodaGroupProofNarrativeReasonSidecar,\n  ):\n    raise TypeError(\n      "reason_sidecar must be a "\n      "TodaGroupProofNarrativeReasonSidecar"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]"\n      )\n\n      if marker_end >= 0:\n        suffix = stripped[\n          marker_end + 1:\n        ]\n\n        for prefix in (\n          "より, ",\n          "を用いて, ",\n        ):\n          if suffix.startswith(\n            prefix\n          ):\n            stripped = suffix[\n              len(\n                prefix\n              ):\n            ]\n            break\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def paragraph_index_for_step(\n    proof_step,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n    matching = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matching\n    ) != 1:\n      return None\n\n    return matching[\n      0\n    ]\n\n  def visible_reason_paragraph(\n    reason: TodaGroupProofNarrativeReason,\n  ) -> str | None:\n    sentence = (\n      render_toda_group_proof_narrative_reason_sentence(\n        reason\n      )\n    )\n\n    if sentence is None:\n      return None\n\n    lines = sentence.splitlines()\n\n    while (\n      lines\n      and lines[\n        -1\n      ].strip()\n      in {\n        "以上より,",\n        "したがって,",\n        "これより,",\n        "これらより,",\n      }\n    ):\n      lines.pop()\n\n    rendered = "\\n".join(\n      lines\n    ).strip()\n\n    return (\n      rendered\n      if rendered\n      else None\n    )\n\n  for reason in reason_sidecar.reasons:\n    if (\n      reason.kind\n      is not TodaGroupProofNarrativeReasonKind\n      .INJECTIVE_IMAGE_ORDER\n    ):\n      continue\n\n    reason_paragraph = (\n      visible_reason_paragraph(\n        reason\n      )\n    )\n\n    if reason_paragraph is None:\n      continue\n\n    reason_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip()\n      == reason_paragraph\n    )\n\n    if len(\n      reason_indices\n    ) != 1:\n      continue\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      continue\n\n    premise_indices = tuple(\n      index\n      for premise in reason.premise_steps\n      for index in (\n        paragraph_index_for_step(\n          premise\n        ),\n      )\n      if index is not None\n    )\n\n    if len(\n      premise_indices\n    ) != len(\n      reason.premise_steps\n    ):\n      continue\n\n    if max(\n      premise_indices\n    ) >= conclusion_index:\n      continue\n\n    reason_index = reason_indices[\n      0\n    ]\n\n    if (\n      reason_index\n      == conclusion_index - 1\n      and reason_index\n      > max(\n        premise_indices\n      )\n    ):\n      continue\n\n    paragraph = paragraphs.pop(\n      reason_index\n    )\n\n    conclusion_index = (\n      paragraph_index_for_step(\n        reason.conclusion_step\n      )\n    )\n\n    if conclusion_index is None:\n      paragraphs.insert(\n        reason_index,\n        paragraph,\n      )\n      continue\n\n    paragraphs.insert(\n      conclusion_index,\n      paragraph,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _body_pi6_3_repair48() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  return rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n\ndef test_phase157_r20_repair48_injective_image_reason_follows_both_visible_premises():\n  body = _body_pi6_3_repair48()\n\n  group_structure = (\n    "[R1]より, "\n    r"$\\pi_{5}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n  )\n  injective = (\n    r"$E: \\pi_{5}^{2} \\to "\n    r"\\pi_{6}^{3}$ は単射である."\n  )\n  reason = (\n    "この群構造と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})="\n    r"\\eta_{3}^{3}\\neq0$ であり, "\n    "単射写像は元の位数を保つ."\n  )\n  conclusion = (\n    r"$\\operatorname{ord}"\n    r"\\left(\\eta_{3}^{3}\\right) = 2$."\n  )\n\n  assert body.index(\n    group_structure\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    injective\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    reason\n  ) < body.index(\n    conclusion\n  )\n\n\ndef test_phase157_r20_repair48_reason_is_immediately_before_eta_order():\n  body = _body_pi6_3_repair48()\n\n  reason = (\n    "この群構造と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})="\n    r"\\eta_{3}^{3}\\neq0$ であり, "\n    "単射写像は元の位数を保つ."\n  )\n  conclusion = (\n    r"$\\operatorname{ord}"\n    r"\\left(\\eta_{3}^{3}\\right) = 2$."\n  )\n\n  paragraphs = tuple(\n    paragraph.strip()\n    for paragraph in body.split(\n      "\\n\\n"\n    )\n    if paragraph.strip()\n  )\n\n  reason_index = paragraphs.index(\n    reason\n  )\n  conclusion_index = paragraphs.index(\n    conclusion\n  )\n\n  assert (\n    conclusion_index\n    == reason_index + 1\n  )\n\n\ndef test_phase157_r20_repair48_prop22_dependency_order_remains_correct():\n  body = _body_pi6_3_repair48()\n\n  fixed_reference = (\n    "[R5]より, "\n    r"$H(\\alpha\\circ E\\beta) = "\n    r"H(\\alpha)\\circ E\\beta$."\n  )\n  specialization = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"H\\left(\\nu\'\\right)\\eta_{6}\\tag{7}$."\n  )\n  value = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right) = "\n    r"\\eta_{5}^{2}\\tag{8}$."\n  )\n\n  assert body.index(\n    fixed_reference\n  ) < body.index(\n    specialization\n  ) < body.index(\n    value\n  )\n'


def update_reason_renderer(
  source: str,
) -> str:
  if (
    "def order_toda_group_proof_narrative_injective_image_order_reason("
    in source
  ):
    raise RuntimeError(
      "repair48 reason-ordering function already exists"
    )

  anchor = (
    "\ndef _toda_group_proof_narrative_reason_insertion_index(\n"
  )

  if source.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "repair48 reason-renderer anchor was not found exactly once"
    )

  return source.replace(
    anchor,
    "\n\n"
    + NEW_FUNCTION.rstrip()
    + "\n\n"
    + anchor.lstrip(
      "\n"
    ),
    1,
  )


def update_contribution_import(
  source: str,
) -> str:
  old = """from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
"""

  new = """from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
  order_toda_group_proof_narrative_injective_image_order_reason,
)
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair48 contribution import anchor "
      "was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def update_contribution_pipeline(
  source: str,
) -> str:
  old = """  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
"""

  new = """  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )
  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  generic_used_step_ids = (
"""

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair48 pipeline anchor was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> int:
  for path in (
    REASON_RENDERER,
    CONTRIBUTION_RENDERER,
  ):
    if not path.is_file():
      raise RuntimeError(
        "Run from repository root."
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair48_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    REASON_RENDERER,
    backup / REASON_RENDERER.name,
  )
  shutil.copy2(
    CONTRIBUTION_RENDERER,
    backup / CONTRIBUTION_RENDERER.name,
  )

  reason_source = REASON_RENDERER.read_text(
    encoding="utf-8"
  )
  contribution_source = CONTRIBUTION_RENDERER.read_text(
    encoding="utf-8"
  )

  reason_source = update_reason_renderer(
    reason_source
  )
  contribution_source = update_contribution_import(
    contribution_source
  )
  contribution_source = update_contribution_pipeline(
    contribution_source
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  combined = (
    reason_source
    + "\n"
    + contribution_source
  )

  for token in forbidden:
    if token in combined:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    reason_source,
    str(
      REASON_RENDERER
    ),
    "exec",
  )
  compile(
    contribution_source,
    str(
      CONTRIBUTION_RENDERER
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

  REASON_RENDERER.write_text(
    reason_source,
    encoding="utf-8",
    newline="\n",
  )
  CONTRIBUTION_RENDERER.write_text(
    contribution_source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair48 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    REASON_RENDERER,
  )
  print(
    "Changed production file:",
    CONTRIBUTION_RENDERER,
  )
  print(
    "Added test:",
    TEST,
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
