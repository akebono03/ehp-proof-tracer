from pathlib import Path
import shutil

ROOT = Path.cwd()
PKG = Path(__file__).resolve().parent
REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"

for required in (REFERENCES, CONTRIBUTION, ROOT / "toda_literature_statement_boundary.py"):
  if not required.exists():
    raise SystemExit(f"required file not found: {required}")

backup_dir = PKG / "backup_before_apply"
backup_dir.mkdir(exist_ok=True)
shutil.copy2(REFERENCES, backup_dir / REFERENCES.name)
shutil.copy2(CONTRIBUTION, backup_dir / CONTRIBUTION.name)
if TEST_TARGET.exists():
  shutil.copy2(TEST_TARGET, backup_dir / TEST_TARGET.name)

references_text = REFERENCES.read_text(encoding="utf-8")

helper_anchor = "def filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n"
helper_code = '''def restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage(\n  original_entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  original_statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  filtered_entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  filtered_statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  body_markdown: str,\n  root_step: ProofStep,\n) -> tuple[\n  tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  str,\n]:\n  if not isinstance(original_entries, tuple):\n    raise TypeError("original_entries must be a tuple")\n  if not isinstance(filtered_entries, tuple):\n    raise TypeError("filtered_entries must be a tuple")\n  if not isinstance(\n    original_statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "original_statement_lines_by_reference_number must be a dict"\n    )\n  if not isinstance(\n    filtered_statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "filtered_statement_lines_by_reference_number must be a dict"\n    )\n  if not isinstance(body_markdown, str):\n    raise TypeError("body_markdown must be a str")\n  if not isinstance(root_step, ProofStep):\n    raise TypeError("root_step must be a ProofStep")\n\n  if not _phase157_r3_is_pi6_3_root(root_step):\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n      body_markdown,\n    )\n\n  required_locator = "Proposition 5.6"\n  filtered_by_locator = {\n    entry.reference.locator: entry\n    for entry in filtered_entries\n  }\n\n  if required_locator in filtered_by_locator:\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n      body_markdown,\n    )\n\n  required_original_entries = tuple(\n    entry\n    for entry in original_entries\n    if entry.reference.locator == required_locator\n  )\n\n  if len(required_original_entries) != 1:\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n      body_markdown,\n    )\n\n  retained_locators = {\n    entry.reference.locator\n    for entry in filtered_entries\n  }\n  retained_locators.add(required_locator)\n\n  desired_original_entries = tuple(\n    entry\n    for entry in original_entries\n    if entry.reference.locator in retained_locators\n  )\n\n  if not desired_original_entries:\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n      body_markdown,\n    )\n\n  new_number_by_locator = {\n    entry.reference.locator: number\n    for number, entry in enumerate(\n      desired_original_entries,\n      start=1,\n    )\n  }\n\n  old_filtered_number_to_new_number = {\n    entry.number: new_number_by_locator[entry.reference.locator]\n    for entry in filtered_entries\n    if entry.reference.locator in new_number_by_locator\n  }\n\n  placeholder_by_old_number = {\n    old_number: f"__PHASE157_R3_REFERENCE_{old_number}__"\n    for old_number in old_filtered_number_to_new_number\n  }\n\n  remapped_body = body_markdown\n\n  for old_number, placeholder in placeholder_by_old_number.items():\n    remapped_body = remapped_body.replace(\n      f"[R{old_number}]",\n      placeholder,\n    )\n\n  for old_number, new_number in old_filtered_number_to_new_number.items():\n    remapped_body = remapped_body.replace(\n      placeholder_by_old_number[old_number],\n      f"[R{new_number}]",\n    )\n\n  desired_entries = tuple(\n    replace(\n      entry,\n      number=new_number_by_locator[entry.reference.locator],\n    )\n    for entry in desired_original_entries\n  )\n\n  desired_statement_lines = {\n    new_number_by_locator[entry.reference.locator]: (\n      original_statement_lines_by_reference_number[entry.number]\n    )\n    for entry in desired_original_entries\n    if entry.number in original_statement_lines_by_reference_number\n  }\n\n  return (\n    desired_entries,\n    desired_statement_lines,\n    remapped_body,\n  )\n\n\n'''

if "def restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage(" not in references_text:
  if helper_anchor not in references_text:
    raise SystemExit("references helper insertion anchor not found")
  references_text = references_text.replace(
    helper_anchor,
    helper_code + helper_anchor,
    1,
  )

REFERENCES.write_text(references_text, encoding="utf-8")

contribution_text = CONTRIBUTION.read_text(encoding="utf-8")

old_import = '''  filter_phase157_r3_pi6_3_reference_entries,\n  filter_toda_group_proof_narrative_reference_entries_by_body_usage,\n'''
new_import = '''  filter_phase157_r3_pi6_3_reference_entries,\n  filter_toda_group_proof_narrative_reference_entries_by_body_usage,\n  restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage,\n'''
if old_import not in contribution_text:
  raise SystemExit("contribution import anchor not found")
contribution_text = contribution_text.replace(old_import, new_import, 1)

render_anchor = "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n"
restore_internal_code = '''def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n  if not isinstance(markdown, str):\n    raise TypeError("markdown must be a str")\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n    and presentation.max_depth >= 3\n  ):\n    return markdown\n\n  suspension_step = next(\n    (\n      node.proof_step\n      for node in presentation.nodes\n      if (\n        node.proof_step.inference_rule is not None\n        and node.proof_step.inference_rule.name\n        == "Toda Proposition 5.3 n=3 suspension isomorphism"\n      )\n    ),\n    None,\n  )\n  hopf_step = next(\n    (\n      node.proof_step\n      for node in presentation.nodes\n      if (\n        node.proof_step.inference_rule is not None\n        and node.proof_step.inference_rule.name\n        == "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"\n      )\n    ),\n    None,\n  )\n\n  if suspension_step is None or hopf_step is None:\n    return markdown\n\n  suspension_line = _render_generic_narrative_step(\n    suspension_step\n  )\n  hopf_line = _render_generic_narrative_step(\n    hopf_step\n  )\n\n  if not suspension_line or not hopf_line:\n    return markdown\n\n  if suspension_line in markdown:\n    return markdown\n\n  hopf_index = markdown.find(hopf_line)\n\n  if hopf_index < 0:\n    return markdown\n\n  insertion = (\n    suspension_line\n    + "\\n\\n"\n  )\n\n  return (\n    markdown[:hopf_index]\n    + insertion\n    + markdown[hopf_index:]\n  )\n\n\n'''

if "def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(" not in contribution_text:
  if render_anchor not in contribution_text:
    raise SystemExit("contribution render insertion anchor not found")
  contribution_text = contribution_text.replace(
    render_anchor,
    restore_internal_code + render_anchor,
    1,
  )

capture_old = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  reference_owned_step_ids = (\n'''
capture_new = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n  phase157_r3_entries_before_usage_filter = reference_entries\n  phase157_r3_lines_before_usage_filter = (\n    statement_lines_by_reference_number\n  )\n\n  reference_owned_step_ids = (\n'''
if capture_old not in contribution_text:
  raise SystemExit("contribution capture anchor not found")
contribution_text = contribution_text.replace(capture_old, capture_new, 1)

normalize_old = '''  rendered = (\n    normalize_toda_group_proof_narrative_connectors(\n      rendered\n    )\n  )\n  rendered = (\n    order_toda_group_proof_narrative_local_equation_derivations(\n      rendered\n    )\n  )\n\n  generic_used_step_ids = (\n'''
normalize_new = '''  rendered = (\n    normalize_toda_group_proof_narrative_connectors(\n      rendered\n    )\n  )\n  rendered = (\n    order_toda_group_proof_narrative_local_equation_derivations(\n      rendered\n    )\n  )\n  rendered = (\n    _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n      presentation,\n      rendered,\n    )\n  )\n\n  generic_used_step_ids = (\n'''
if normalize_old not in contribution_text:
  raise SystemExit("contribution internal restoration anchor not found")
contribution_text = contribution_text.replace(normalize_old, normalize_new, 1)

final_filter_anchor = '''  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n'''
restore_call = '''  (\n    reference_entries,\n    statement_lines_by_reference_number,\n    rendered,\n  ) = (\n    restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage(\n      phase157_r3_entries_before_usage_filter,\n      phase157_r3_lines_before_usage_filter,\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n      presentation.root_step,\n    )\n  )\n\n'''
# Replace the final reference_section occurrence inside the target function only.
render_start = contribution_text.index(render_anchor)
section_index = contribution_text.index(final_filter_anchor, render_start)
contribution_text = (
  contribution_text[:section_index]
  + restore_call
  + contribution_text[section_index:]
)

CONTRIBUTION.write_text(contribution_text, encoding="utf-8")

shutil.copy2(PKG / "tests" / TEST_TARGET.name, TEST_TARGET)

print("Phase157-R3 repair1 changes applied.")
print(f"updated: {REFERENCES}")
print(f"updated: {CONTRIBUTION}")
print(f"updated: {TEST_TARGET}")
