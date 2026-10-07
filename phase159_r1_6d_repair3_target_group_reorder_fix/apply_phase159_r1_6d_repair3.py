from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

HELPER = 'def _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  all_steps = (\n    _phase159_r1_6c_recursive_proof_steps(\n      presentation.root_step\n    )\n  )\n\n  for surjective_step in all_steps:\n    if not isinstance(\n      surjective_step.conclusion,\n      TodaHopfInvariantSurjectiveStatement,\n    ):\n      continue\n\n    target_group = (\n      surjective_step.conclusion.map.target_group\n    )\n    target_group_latex = (\n      render_toda_primary_group_latex(\n        target_group\n      )\n    )\n\n    rendered_surjective = (\n      _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          surjective_step\n        )\n      )\n    )\n\n    surjective_match = re.match(\n      r"^\\$(?P<math>.+)\\$ は全射\\.$",\n      rendered_surjective,\n    )\n\n    if surjective_match is None:\n      continue\n\n    display_prefix = (\n      "\\\\[\\n"\n      + surjective_match.group(\n        "math"\n      )\n      + r"\\quad\\text{は全射}. \\qquad ("\n    )\n\n    display_start = rendered.find(\n      display_prefix\n    )\n\n    if display_start < 0:\n      continue\n\n    display_end = rendered.find(\n      "\\n\\\\]",\n      display_start,\n    )\n\n    if display_end < 0:\n      continue\n\n    display_end += len(\n      "\\n\\\\]"\n    )\n\n    target_group_pattern = re.compile(\n      r"^\\[R[0-9]+\\] より, \\$"\n      + re.escape(\n        target_group_latex\n      )\n      + r" = .+\\$\\.$",\n      flags=re.MULTILINE,\n    )\n\n    target_group_match = (\n      target_group_pattern.search(\n        rendered\n      )\n    )\n\n    if target_group_match is None:\n      continue\n\n    target_group_line = (\n      target_group_match.group(\n        0\n      )\n    )\n\n    if (\n      target_group_match.start()\n      > display_end\n    ):\n      continue\n\n    source_start = (\n      target_group_match.start()\n    )\n    source_end = (\n      target_group_match.end()\n    )\n\n    while (\n      source_end < len(\n        rendered\n      )\n      and rendered[\n        source_end\n      ]\n      == "\\n"\n    ):\n      source_end += 1\n\n    without_source = (\n      rendered[\n        :source_start\n      ]\n      + rendered[\n        source_end:\n      ]\n    )\n\n    display_start = without_source.find(\n      display_prefix\n    )\n\n    if display_start < 0:\n      continue\n\n    display_end = without_source.find(\n      "\\n\\\\]",\n      display_start,\n    )\n\n    if display_end < 0:\n      continue\n\n    display_end += len(\n      "\\n\\\\]"\n    )\n\n    return (\n      without_source[\n        :display_end\n      ]\n      + "\\n\\n"\n      + target_group_line\n      + without_source[\n        display_end:\n      ]\n    )\n\n  return rendered\n'


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
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ]
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
      "phase159_r1_6d_repair3_backup_"
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

  source = replace_function(
    source,
    "_phase159_r1_6d_reorder_target_group_fact_after_surjectivity",
    HELPER,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6d repair3 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Repaired target-group fact reordering "
    "to match the rendered [R] target-group line "
    "by the surjective map target group."
  )


if __name__ == "__main__":
  main()
