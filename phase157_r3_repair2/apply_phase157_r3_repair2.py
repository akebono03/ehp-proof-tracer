from pathlib import Path
import shutil

ROOT = Path.cwd()
PKG = Path(__file__).resolve().parent
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"

if not CONTRIBUTION.exists():
  raise SystemExit(f"required file not found: {CONTRIBUTION}")

backup_dir = PKG / "backup_before_apply"
backup_dir.mkdir(exist_ok=True)
shutil.copy2(CONTRIBUTION, backup_dir / CONTRIBUTION.name)
if TEST_TARGET.exists():
  shutil.copy2(TEST_TARGET, backup_dir / TEST_TARGET.name)

text = CONTRIBUTION.read_text(encoding="utf-8")

# Import replace without depending on an exact multi-line anchor.
old_dataclass_import = "from dataclasses import (\n  fields,\n  is_dataclass,\n)\n"
new_dataclass_import = "from dataclasses import (\n  fields,\n  is_dataclass,\n  replace,\n)\n"
if old_dataclass_import in text:
  text = text.replace(
    old_dataclass_import,
    new_dataclass_import,
    1,
  )
elif "  replace,\n" not in text:
  raise SystemExit("dataclasses import block not found")

render_anchor = (
  "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n"
)

restore_internal_helper = '''def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n  if not isinstance(markdown, str):\n    raise TypeError("markdown must be a str")\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n    and presentation.max_depth >= 3\n  ):\n    return markdown\n\n  suspension_step = next(\n    (\n      node.proof_step\n      for node in presentation.nodes\n      if (\n        node.proof_step.inference_rule is not None\n        and node.proof_step.inference_rule.name\n        == "Toda Proposition 5.3 n=3 suspension isomorphism"\n      )\n    ),\n    None,\n  )\n  hopf_step = next(\n    (\n      node.proof_step\n      for node in presentation.nodes\n      if (\n        node.proof_step.inference_rule is not None\n        and node.proof_step.inference_rule.name\n        == "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"\n      )\n    ),\n    None,\n  )\n\n  if suspension_step is None or hopf_step is None:\n    return markdown\n\n  suspension_line = _render_generic_narrative_step(\n    suspension_step\n  )\n  hopf_line = _render_generic_narrative_step(\n    hopf_step\n  )\n\n  if not suspension_line or not hopf_line:\n    return markdown\n\n  if suspension_line in markdown:\n    return markdown\n\n  hopf_index = markdown.find(\n    hopf_line\n  )\n\n  if hopf_index < 0:\n    return markdown\n\n  return (\n    markdown[:hopf_index]\n    + suspension_line\n    + "\\n\\n"\n    + markdown[hopf_index:]\n  )\n\n\ndef _phase157_r3_restore_pi6_3_earlier_prop56_reference(\n  presentation: TodaGroupProofPresentation,\n  original_entries,\n  original_statement_lines_by_reference_number,\n  filtered_entries,\n  filtered_statement_lines_by_reference_number,\n):\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n    )\n\n  if any(\n    entry.reference.locator == "Proposition 5.6"\n    for entry in filtered_entries\n  ):\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n    )\n\n  source_entries = tuple(\n    entry\n    for entry in original_entries\n    if entry.reference.locator == "Proposition 5.6"\n  )\n\n  if len(source_entries) != 1:\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n    )\n\n  source_entry = source_entries[0]\n\n  if source_entry.number not in (\n    original_statement_lines_by_reference_number\n  ):\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n    )\n\n  new_number = len(filtered_entries) + 1\n  restored_entry = replace(\n    source_entry,\n    number=new_number,\n  )\n  restored_lines = dict(\n    filtered_statement_lines_by_reference_number\n  )\n  restored_lines[new_number] = (\n    original_statement_lines_by_reference_number[\n      source_entry.number\n    ]\n  )\n\n  return (\n    filtered_entries + (restored_entry,),\n    restored_lines,\n  )\n\n\n'''

if (
  "def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism("
  not in text
):
  if render_anchor not in text:
    raise SystemExit("render function anchor not found")
  text = text.replace(
    render_anchor,
    restore_internal_helper + render_anchor,
    1,
  )

# Work only inside the target rendering function.
render_start = text.index(render_anchor)
function_text = text[render_start:]

capture_old = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  reference_owned_step_ids = (\n'''
capture_new = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n  phase157_r3_entries_before_usage_filter = reference_entries\n  phase157_r3_lines_before_usage_filter = (\n    statement_lines_by_reference_number\n  )\n\n  reference_owned_step_ids = (\n'''
if "phase157_r3_entries_before_usage_filter" not in function_text:
  if capture_old not in function_text:
    raise SystemExit("pre-usage reference capture anchor not found")
  function_text = function_text.replace(
    capture_old,
    capture_new,
    1,
  )

normalize_old = '''  rendered = (\n    order_toda_group_proof_narrative_local_equation_derivations(\n      rendered\n    )\n  )\n\n  generic_used_step_ids = (\n'''
normalize_new = '''  rendered = (\n    order_toda_group_proof_narrative_local_equation_derivations(\n      rendered\n    )\n  )\n  rendered = (\n    _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n      presentation,\n      rendered,\n    )\n  )\n\n  generic_used_step_ids = (\n'''
if "_phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n      presentation" not in function_text:
  if normalize_old not in function_text:
    raise SystemExit("proof-internal restoration anchor not found")
  function_text = function_text.replace(
    normalize_old,
    normalize_new,
    1,
  )

reference_section_anchor = '''  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n'''
restore_reference_call = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    _phase157_r3_restore_pi6_3_earlier_prop56_reference(\n      presentation,\n      phase157_r3_entries_before_usage_filter,\n      phase157_r3_lines_before_usage_filter,\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n'''
if "_phase157_r3_restore_pi6_3_earlier_prop56_reference(\n      presentation" not in function_text:
  section_index = function_text.rfind(
    reference_section_anchor
  )
  if section_index < 0:
    raise SystemExit("final reference section anchor not found")
  function_text = (
    function_text[:section_index]
    + restore_reference_call
    + function_text[section_index:]
  )

text = text[:render_start] + function_text
CONTRIBUTION.write_text(text, encoding="utf-8")

shutil.copy2(
  PKG / "tests" / TEST_TARGET.name,
  TEST_TARGET,
)

print("Phase157-R3 repair2 changes applied.")
print(f"updated: {CONTRIBUTION}")
print(f"updated: {TEST_TARGET}")
