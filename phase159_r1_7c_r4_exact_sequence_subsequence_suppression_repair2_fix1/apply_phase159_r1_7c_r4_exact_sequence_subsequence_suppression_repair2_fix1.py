from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PROD = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_7c_r4_exact_sequence_late_prefix_suppression_repair2.py"

HELPER_NAME = "suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements"
HELPER_SOURCE = 'def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  retained = []\n  prior_sequence_cores = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    if (\n      not stripped.startswith(\n        "$"\n      )\n      or r"\\xrightarrow{"\n      not in stripped\n    ):\n      retained.append(\n        paragraph\n      )\n      continue\n\n    closing_math_index = stripped.find(\n      "$",\n      1,\n    )\n\n    if closing_math_index < 0:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    sequence_core = stripped[\n      1:\n      closing_math_index\n    ]\n    arrow_count = sequence_core.count(\n      r"\\xrightarrow{"\n    )\n\n    if arrow_count < 1:\n      retained.append(\n        paragraph\n      )\n      continue\n\n    is_late_prefix_restatement = any(\n      prior_core.startswith(\n        sequence_core\n      )\n      and prior_core != sequence_core\n      and prior_core.count(\n        r"\\xrightarrow{"\n      ) > arrow_count\n      for prior_core in prior_sequence_cores\n    )\n\n    if is_late_prefix_restatement:\n      continue\n\n    prior_sequence_cores.append(\n      sequence_core\n    )\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from toda_group_proof_narrative_contribution_renderer import (\n  suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements,\n)\n\n\ndef test_phase159_r1_7c_r4_late_shorter_prefix_is_suppressed():\n  longer = (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}$."\n  )\n  shorter = (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1}$."\n  )\n  markdown = (\n    longer\n    + "\\n\\n"\n    + r"$\\pi_{2}^{1}=0$."\n    + "\\n\\n"\n    + shorter\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      markdown\n    )\n  )\n\n  assert longer in rendered\n  assert shorter not in rendered\n\n\ndef test_phase159_r1_7c_r4_earlier_shorter_exactness_is_preserved():\n  shorter = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  longer = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$."\n  )\n  markdown = (\n    shorter\n    + "\\n\\n"\n    + longer\n  )\n\n  rendered = (\n    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(\n      markdown\n    )\n  )\n\n  assert shorter in rendered\n  assert longer in rendered\n'


def insert_helper_if_missing(
  source: str,
) -> str:
  marker = (
    "def "
    + HELPER_NAME
    + "("
  )

  if marker in source:
    return source

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

  return (
    source[:render_index]
    + HELPER_SOURCE.rstrip()
    + "\n\n\n"
    + source[render_index:]
  )


def insert_call_if_missing(
  source: str,
) -> str:
  call_text = (
    "  rendered = (\n"
    "    "
    + HELPER_NAME
    + "(\n"
    "      rendered\n"
    "    )\n"
    "  )\n\n"
  )

  if call_text in source:
    return source

  render_marker = (
    "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown("
  )
  render_start = source.find(
    render_marker
  )

  if render_start < 0:
    raise SystemExit(
      "public contribution renderer not found"
    )

  anchor = (
    "  generic_used_step_ids = (\n"
  )
  anchor_index = source.find(
    anchor,
    render_start,
  )

  if anchor_index < 0:
    raise SystemExit(
      "generic_used_step_ids anchor not found"
    )

  return (
    source[:anchor_index]
    + call_text
    + source[anchor_index:]
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

  source = insert_helper_if_missing(
    source
  )
  source = insert_call_if_missing(
    source
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
    "Phase 159 R1-7c R4 exact-sequence suppression repair2 fix1 applied."
  )
  print(
    "Production design unchanged."
  )
  print(
    "Apply logic now anchors directly on generic_used_step_ids."
  )


if __name__ == "__main__":
  main()
