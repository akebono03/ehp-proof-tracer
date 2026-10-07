from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6d_target_group_fact_order.py"
)

HELPER = 'def _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_number = (\n    _phase159_r1_6c_reference_number(\n      rendered,\n      "(5.1)",\n    )\n  )\n\n  if reference_number is None:\n    return rendered\n\n  all_steps = (\n    _phase159_r1_6c_recursive_proof_steps(\n      presentation.root_step\n    )\n  )\n\n  for surjective_step in all_steps:\n    if not isinstance(\n      surjective_step.conclusion,\n      TodaHopfInvariantSurjectiveStatement,\n    ):\n      continue\n\n    target_group = (\n      surjective_step.conclusion.map.target_group\n    )\n\n    target_group_step = next(\n      (\n        proof_step\n        for proof_step in all_steps\n        if (\n          isinstance(\n            proof_step.conclusion,\n            Relation,\n          )\n          and proof_step.conclusion.lhs\n          == target_group\n          and (\n            _phase159_r1_6c_step_reference_locator(\n              proof_step\n            )\n            == "(5.1)"\n          )\n        )\n      ),\n      None,\n    )\n\n    if target_group_step is None:\n      continue\n\n    target_group_line = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "] より, "\n      + _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          target_group_step\n        )\n      )\n    )\n\n    source_paragraph = (\n      target_group_line\n      + "\\n\\n"\n    )\n\n    if source_paragraph not in rendered:\n      continue\n\n    rendered_surjective = (\n      _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          surjective_step\n        )\n      )\n    )\n\n    match = re.match(\n      r"^\\$(?P<math>.+)\\$ は全射\\.$",\n      rendered_surjective,\n    )\n\n    if match is None:\n      continue\n\n    display_prefix = (\n      "\\\\[\\n"\n      + match.group(\n        "math"\n      )\n      + r"\\quad\\text{は全射}. \\qquad ("\n    )\n\n    display_start = rendered.find(\n      display_prefix\n    )\n\n    if display_start < 0:\n      continue\n\n    display_end = rendered.find(\n      "\\n\\\\]",\n      display_start,\n    )\n\n    if display_end < 0:\n      continue\n\n    display_end += len(\n      "\\n\\\\]"\n    )\n\n    source_index = rendered.find(\n      source_paragraph\n    )\n\n    if source_index < 0:\n      continue\n\n    without_source = (\n      rendered[\n        :source_index\n      ]\n      + rendered[\n        source_index\n        + len(\n          source_paragraph\n        ):\n      ]\n    )\n\n    if source_index < display_start:\n      display_start = without_source.find(\n        display_prefix\n      )\n\n      if display_start < 0:\n        continue\n\n      display_end = without_source.find(\n        "\\n\\\\]",\n        display_start,\n      )\n\n      if display_end < 0:\n        continue\n\n      display_end += len(\n        "\\n\\\\]"\n      )\n\n    insertion = (\n      "\\n\\n"\n      + target_group_line\n    )\n\n    return (\n      without_source[\n        :display_end\n      ]\n      + insertion\n      + without_source[\n        display_end:\n      ]\n    )\n\n  return rendered\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_reference_map_property_wording(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_canonicalize_toda_51_reference(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_remove_redundant_exactness_sentence(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_link_proof_reasons(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_render_statement_numbers(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6d_finalize_reference_and_linkage(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_6d_center_structural_formulas(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(\n      presentation,\n      rendered,\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'
NEW_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase159_r1_6d_repair2_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_r1_6d_target_group_fact_follows_surjectivity():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_repair2_pi3_2_presentation()\n    )\n  )\n\n  surjective = (\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n  )\n  target_group = (\n    r"[R1] より, $\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n  )\n  isomorphism = (\n    r"(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n  )\n  eta_definition = (\n    r"$H(\\eta_{2}) = \\iota_{3}$ となる "\n    r"$\\eta_{2} \\in \\pi_{3}^{2}$ が一意に存在する."\n  )\n\n  assert surjective in rendered\n  assert target_group in rendered\n  assert isomorphism in rendered\n  assert eta_definition in rendered\n\n  assert (\n    rendered.index(\n      surjective\n    )\n    < rendered.index(\n      target_group\n    )\n    < rendered.index(\n      isomorphism\n    )\n    < rendered.index(\n      eta_definition\n    )\n  )\n\n\ndef test_phase159_r1_6d_target_group_fact_is_not_before_surjectivity():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_repair2_pi3_2_presentation()\n    )\n  )\n\n  zero_map = (\n    r"完全性より, $\\Delta: \\pi_{3}^{3} "\n    r"\\to \\pi_{1}^{1}$ は零写像."\n  )\n  target_group = (\n    r"[R1] より, $\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n  )\n  surjective = (\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n  )\n\n  assert (\n    rendered.index(\n      zero_map\n    )\n    < rendered.index(\n      surjective\n    )\n    < rendered.index(\n      target_group\n    )\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(
      RENDERER
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6d_repair2_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    RENDERER,
    backup_dir / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  anchor = (
    "def render_toda_group_proof_narrative_markdown("
  )
  anchor_index = source.find(
    anchor
  )

  if anchor_index < 0:
    raise RuntimeError(
      "public render function not found"
    )

  if (
    "def _phase159_r1_6d_reorder_target_group_fact_after_surjectivity("
    not in source
  ):
    source = (
      source[:anchor_index]
      + HELPER.rstrip()
      + "\n\n\n"
      + source[anchor_index:]
    )

  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    NEW_TEST.rstrip() + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6d repair2 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Moved the Toda (5.1) target-group fact "
    "to immediately after the relevant surjectivity statement."
  )


if __name__ == "__main__":
  main()
