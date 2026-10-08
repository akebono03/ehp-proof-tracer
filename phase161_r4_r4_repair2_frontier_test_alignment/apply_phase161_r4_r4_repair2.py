from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TEST = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r4_restore_global_frontier.py"
)
OUTPUT_DIR = PACKAGE_DIR / "output"

TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n  _toda_group_proof_narrative_root_fixed_statement_internal_step_ids,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_r4_presentations(\n  n: int,\n  k: int,\n  depth: int,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    presentation,\n  )\n\n\ndef _phase161_r4_r4_pi4_2_entries(\n  presentation,\n):\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return entries\n\n\ndef _phase161_r4_r4_phase156_frontier_entries(\n  presentation,\n):\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return entries\n\n\ndef test_phase161_r4_r4_pi4_2_root_fixed_internality_hides_prop44_only():\n  (\n    raw,\n    presentation,\n  ) = _phase161_r4_r4_presentations(\n    2,\n    2,\n    2,\n  )\n  entries = (\n    _phase161_r4_r4_pi4_2_entries(\n      presentation\n    )\n  )\n\n  internal_step_ids = (\n    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n      presentation\n    )\n  )\n\n  prop44 = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 n=2 specialization"\n    )\n  )\n  restriction = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 second-summand restriction"\n    )\n  )\n\n  assert id(\n    prop44\n  ) in internal_step_ids\n  assert id(\n    restriction\n  ) in internal_step_ids\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert "Proposition 4.4" not in reference\n  assert (\n    r"\\pi_{i - 1}^{1} \\oplus "\n    r"\\pi_{i}^{3} \\to "\n    r"\\pi_{i}^{2}"\n    not in body\n  )\n  assert "分解写像の第二成分" not in body\n  assert "[R1]" in body\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n\n\ndef test_phase161_r4_r4_restores_phase156_global_frontier_contract():\n  (\n    _,\n    presentation,\n  ) = _phase161_r4_r4_presentations(\n    3,\n    3,\n    2,\n  )\n  entries = (\n    _phase161_r4_r4_phase156_frontier_entries(\n      presentation\n    )\n  )\n\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  frontier_locators = {\n    entry.reference.locator\n    for entry in entries\n    if any(\n      id(\n        proof_step\n      )\n      in frontier_step_ids\n      for proof_step in entry.proof_steps\n    )\n  }\n\n  assert "(5.3)" in frontier_locators\n  assert "Proposition 5.3" in frontier_locators\n  assert "Lemma 5.4" in frontier_locators\n  assert "(5.2)" in frontier_locators\n  assert "Proposition 5.1" not in frontier_locators\n\n  assert (\n    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n      presentation\n    )\n    == frozenset()\n  )\n'


def main():
  if not TEST.exists():
    raise RuntimeError(
      f"Expected existing R4-R4 test file: {TEST}"
    )

  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r4_restore_global_frontier.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TEST,
  )
  print(
    "Production changes: NONE"
  )
  print(
    "Updated full test file written to output/."
  )


if __name__ == "__main__":
  main()
