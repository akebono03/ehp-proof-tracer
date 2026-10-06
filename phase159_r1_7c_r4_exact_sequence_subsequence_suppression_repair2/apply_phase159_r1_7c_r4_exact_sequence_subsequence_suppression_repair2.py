from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PROD = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_7c_r4_exact_sequence_late_prefix_suppression_repair2.py"

ORIGINAL_MERGE = 'def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  exactness_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if classify_toda_proof_step_role(\n      node.proof_step\n    )\n    is TodaProofDependencyRole.EHP_EXACTNESS\n  )\n\n  for left_step in exactness_steps:\n    left_window = getattr(\n      left_step.conclusion,\n      "window",\n      None,\n    )\n\n    if left_window is None:\n      continue\n\n    for right_step in exactness_steps:\n      if right_step is left_step:\n        continue\n\n      right_window = getattr(\n        right_step.conclusion,\n        "window",\n        None,\n      )\n\n      if right_window is None:\n        continue\n\n      if not (\n        left_window.middle_term\n        == right_window.source_term\n        and left_window.target_term\n        == right_window.middle_term\n        and _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n        == _toda_group_proof_narrative_map_name_latex(\n          right_window.first_map\n        )\n      ):\n        continue\n\n      left_line = (\n        _render_generic_narrative_step(\n          left_step\n        )\n      )\n      right_line = (\n        _render_generic_narrative_step(\n          right_step\n        )\n      )\n\n      left_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == left_line.strip()\n        ),\n        None,\n      )\n      right_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == right_line.strip()\n        ),\n        None,\n      )\n\n      if (\n        left_index is None\n        or right_index is None\n      ):\n        continue\n\n      first_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.first_map\n        )\n      )\n      second_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n      )\n      third_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          right_window.second_map\n        )\n      )\n\n      if None in (\n        first_map,\n        second_map,\n        third_map,\n      ):\n        continue\n\n      bare_sequence = (\n        "$"\n        + render_toda_primary_group_latex(\n          left_window.source_term\n        )\n        + r" \\xrightarrow{"\n        + first_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.middle_term\n        )\n        + r" \\xrightarrow{"\n        + second_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.target_term\n        )\n        + r" \\xrightarrow{"\n        + third_map\n        + "} "\n        + render_toda_primary_group_latex(\n          right_window.target_term\n        )\n        + "$"\n      )\n      merged = (\n        bare_sequence\n        + " は完全である."\n      )\n\n      bare_indices = tuple(\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip().rstrip(\n          "."\n        )\n        == bare_sequence\n      )\n\n      introduction_index = (\n        bare_indices[\n          0\n        ]\n        if len(\n          bare_indices\n        ) == 1\n        else None\n      )\n\n      removal_indices = {\n        left_index,\n        right_index,\n      }\n\n      if introduction_index is not None:\n        removal_indices.add(\n          introduction_index\n        )\n        insertion_index = (\n          introduction_index\n        )\n      else:\n        insertion_index = min(\n          left_index,\n          right_index,\n        )\n\n      for index in sorted(\n        removal_indices,\n        reverse=True,\n      ):\n        paragraphs.pop(\n          index\n        )\n\n      removed_before_insertion = sum(\n        1\n        for index in removal_indices\n        if index < insertion_index\n      )\n      insertion_index -= (\n        removed_before_insertion\n      )\n\n      paragraphs.insert(\n        insertion_index,\n        merged,\n      )\n\n      return "\\n\\n".join(\n        paragraphs\n      )\n\n  return markdown\n'
NEW_HELPER = 'def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  retained = []\n  prior_sequence_cores = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    if (\n      not stripped.startswith(\n        "$"\n      )\n      or r"\\xrightarrow{"\n      not in stripped\n    ):\n      retained.append(\n        paragraph\n      )\n      continue\n\n    closing_math_index = stripped.find(\n      "$",\n      1,\n    )\n\n    if closing_math_index < 0:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    sequence_core = stripped[\n      1:\n      closing_math_index\n    ]\n    arrow_count = sequence_core.count(\n      r"\\xrightarrow{"\n    )\n\n    if arrow_count < 1:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    is_late_prefix_restatement = any(\n      prior_core.startswith(\n        sequence_core\n      )\n      and prior_core != sequence_core\n      and prior_core.count(\n        r"\\xrightarrow{"\n      ) > arrow_count\n      for prior_core in prior_sequence_cores\n    )\n\n    if is_late_prefix_restatement:\n      continue\n\n    prior_sequence_cores.append(\n      sequence_core\n    )\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from toda_group_proof_narrative_contribution_renderer import (\n  suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements,\n)\n\n\ndef test_phase159_r1_7c_r4_late_shorter_prefix_is_suppressed():\n  longer = (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}$."\n  )\n  shorter = (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1}$."\n  )\n  markdown = (\n    longer\n    + "\\n\\n"\n    + r"$\\pi_{2}^{1}=0$."\n    + "\\n\\n"\n    + shorter\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      markdown\n    )\n  )\n\n  assert longer in rendered\n  assert shorter not in rendered\n\n\ndef test_phase159_r1_7c_r4_earlier_shorter_exactness_is_preserved():\n  shorter = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  longer = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$."\n  )\n  markdown = (\n    shorter\n    + "\\n\\n"\n    + longer\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      markdown\n    )\n  )\n\n  assert shorter in rendered\n  assert longer in rendered\n'
CALL_ANCHOR = '  rendered = (\n    order_toda_group_proof_narrative_injective_image_order_reason(\n      rendered,\n      reason_sidecar,\n    )\n  )\n\n  generic_used_step_ids = (\n'
REPLACEMENT = '  rendered = (\n    order_toda_group_proof_narrative_injective_image_order_reason(\n      rendered,\n      reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      rendered\n    )\n  )\n\n  generic_used_step_ids = (\n'


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
        ORIGINAL_MERGE,
    )

    render_marker = (
        "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown("
    )
    render_index = source.find(
        render_marker
    )
    if render_index < 0:
        raise SystemExit(
            "public contribution renderer not found"
        )

    if (
        "def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements("
        not in source
    ):
        source = (
            source[:render_index]
            + NEW_HELPER.rstrip()
            + "\n\n\n"
            + source[render_index:]
        )

    if REPLACEMENT not in source:
        if CALL_ANCHOR not in source:
            raise SystemExit(
                "late suppression insertion anchor not found"
            )
        source = source.replace(
            CALL_ANCHOR,
            REPLACEMENT,
            1,
        )

    PROD.write_text(
        source,
        encoding="utf-8",
    )
    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 R1-7c R4 exact-sequence suppression repair2 applied."
    )
    print(
        "Restored existing exactness merge behavior."
    )
    print(
        "Added late-only prefix restatement suppression."
    )


if __name__ == "__main__":
    main()
