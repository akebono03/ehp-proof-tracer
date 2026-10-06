from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PROD = ROOT / "toda_group_proof_narrative_contribution_renderer.py"

MERGE_SOURCE = 'def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  exactness_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if classify_toda_proof_step_role(\n      node.proof_step\n    )\n    is TodaProofDependencyRole.EHP_EXACTNESS\n  )\n\n  for left_step in exactness_steps:\n    left_window = getattr(\n      left_step.conclusion,\n      "window",\n      None,\n    )\n\n    if left_window is None:\n      continue\n\n    for right_step in exactness_steps:\n      if right_step is left_step:\n        continue\n\n      right_window = getattr(\n        right_step.conclusion,\n        "window",\n        None,\n      )\n\n      if right_window is None:\n        continue\n\n      if not (\n        left_window.middle_term\n        == right_window.source_term\n        and left_window.target_term\n        == right_window.middle_term\n        and _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n        == _toda_group_proof_narrative_map_name_latex(\n          right_window.first_map\n        )\n      ):\n        continue\n\n      left_line = (\n        _render_generic_narrative_step(\n          left_step\n        )\n      )\n      right_line = (\n        _render_generic_narrative_step(\n          right_step\n        )\n      )\n\n      left_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == left_line.strip()\n        ),\n        None,\n      )\n      right_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == right_line.strip()\n        ),\n        None,\n      )\n\n      if (\n        left_index is None\n        or right_index is None\n      ):\n        continue\n\n      first_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.first_map\n        )\n      )\n      second_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n      )\n      third_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          right_window.second_map\n        )\n      )\n\n      if None in (\n        first_map,\n        second_map,\n        third_map,\n      ):\n        continue\n\n      bare_sequence = (\n        "$"\n        + render_toda_primary_group_latex(\n          left_window.source_term\n        )\n        + r" \\xrightarrow{"\n        + first_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.middle_term\n        )\n        + r" \\xrightarrow{"\n        + second_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.target_term\n        )\n        + r" \\xrightarrow{"\n        + third_map\n        + "} "\n        + render_toda_primary_group_latex(\n          right_window.target_term\n        )\n        + "$"\n      )\n      merged = (\n        bare_sequence\n        + " は完全である."\n      )\n\n      bare_indices = tuple(\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip().rstrip(\n          "."\n        )\n        == bare_sequence\n      )\n\n      introduction_index = (\n        bare_indices[\n          0\n        ]\n        if len(\n          bare_indices\n        ) == 1\n        else None\n      )\n\n      removal_indices = {\n        left_index,\n        right_index,\n      }\n\n      if introduction_index is not None:\n        removal_indices.add(\n          introduction_index\n        )\n        insertion_index = (\n          introduction_index\n        )\n      else:\n        insertion_index = min(\n          left_index,\n          right_index,\n        )\n\n      for index in sorted(\n        removal_indices,\n        reverse=True,\n      ):\n        paragraphs.pop(\n          index\n        )\n\n      removed_before_insertion = sum(\n        1\n        for index in removal_indices\n        if index < insertion_index\n      )\n      insertion_index -= (\n        removed_before_insertion\n      )\n\n      paragraphs.insert(\n        insertion_index,\n        merged,\n      )\n\n      return "\\n\\n".join(\n        paragraphs\n      )\n\n  return markdown\n'


def replace_function(
  source: str,
  function_name: str,
  new_source: str,
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
    raise SystemExit(
      f"function not found: {function_name}"
    )

  next_start = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      source
    )
  else:
    end = next_start + 1

  return (
    source[:start]
    + new_source.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  BACKUP.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    PROD,
    BACKUP / PROD.name,
  )

  source = PROD.read_text(
    encoding="utf-8"
  )

  source = replace_function(
    source,
    "merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows",
    MERGE_SOURCE,
  )

  helper_marker = (
    "def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements("
  )
  call_marker = (
    "    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n"
    "      rendered\n"
    "    )"
  )

  if helper_marker not in source:
    raise SystemExit(
      "late suppression helper missing; run repair2 fix1 first"
    )

  if call_marker not in source:
    raise SystemExit(
      "late suppression call missing; run repair2 fix1 first"
    )

  PROD.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R4 exact-sequence suppression repair2 fix2 applied."
  )
  print(
    "Restored merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows to current GitHub behavior."
  )
  print(
    "Late prefix suppression helper remains active."
  )


if __name__ == "__main__":
  main()
