from pathlib import Path

ROOT = Path.cwd()
NEW_CLOSURE = 'def build_toda_group_proof_narrative_semantic_closure_presentation(\n  presentation: TodaGroupProofPresentation,\n) -> TodaGroupProofPresentation:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if presentation.max_depth == 0:\n    return presentation\n\n  provenance = (\n    extract_toda_recursive_proof_provenance(\n      presentation.source_replay.group_result\n    )\n  )\n  selected_step_ids = {\n    id(\n      node.proof_step\n    )\n    for node in presentation.nodes\n  }\n  original_step_ids = frozenset(\n    selected_step_ids\n  )\n  edges_by_parent_step_id = {}\n\n  for edge in provenance.edges:\n    edges_by_parent_step_id.setdefault(\n      id(\n        edge.parent_step\n      ),\n      [],\n    ).append(\n      edge\n    )\n\n  order_calculation_step_ids = set()\n\n  for node in presentation.nodes:\n    order_statement = (\n      node.proof_step.conclusion\n    )\n\n    if (\n      not isinstance(\n        order_statement,\n        Relation,\n      )\n      or order_statement.relation_type\n      is not RelationType.ORDER\n    ):\n      continue\n\n    for edge in edges_by_parent_step_id.get(\n      id(\n        node.proof_step\n      ),\n      (),\n    ):\n      premise_statement = (\n        edge.premise_step.conclusion\n      )\n\n      if (\n        isinstance(\n          premise_statement,\n          Relation,\n        )\n        and premise_statement.relation_type\n        is RelationType.EQUALITY\n      ):\n        order_calculation_step_ids.add(\n          id(\n            edge.premise_step\n          )\n        )\n\n  for calculation_step_id in (\n    order_calculation_step_ids\n  ):\n    for edge in edges_by_parent_step_id.get(\n      calculation_step_id,\n      (),\n    ):\n      premise_statement = (\n        edge.premise_step.conclusion\n      )\n\n      if (\n        not isinstance(\n          premise_statement,\n          Relation,\n        )\n        or premise_statement.relation_type\n        is not RelationType.EQUALITY\n      ):\n        continue\n\n      selected_step_ids.add(\n        id(\n          edge.premise_step\n        )\n      )\n\n  changed = True\n\n  while changed:\n    changed = False\n\n    for edge in provenance.edges:\n      if (\n        id(\n          edge.parent_step\n        )\n        not in selected_step_ids\n      ):\n        continue\n\n      key = (\n        _inference_rule_name(\n          edge.parent_step\n        ),\n        edge.premise_index,\n      )\n\n      if (\n        key\n        not in _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX\n      ):\n        continue\n\n      premise_step_id = id(\n        edge.premise_step\n      )\n\n      if premise_step_id in selected_step_ids:\n        continue\n\n      selected_step_ids.add(\n        premise_step_id\n      )\n      changed = True\n\n  if selected_step_ids == original_step_ids:\n    return presentation\n\n  replay_step_by_proof_step_id = {\n    id(\n      replay_step.proof_step\n    ): replay_step\n    for replay_step in presentation.source_replay.steps\n  }\n\n  for node in provenance.nodes:\n    proof_step_id = id(\n      node.proof_step\n    )\n\n    if (\n      proof_step_id not in selected_step_ids\n      or proof_step_id\n      in replay_step_by_proof_step_id\n    ):\n      continue\n\n    replay_step_by_proof_step_id[\n      proof_step_id\n    ] = TodaGroupResultProofReplayStep(\n      depth=node.shortest_depth,\n      proof_step=node.proof_step,\n      role=node.role,\n    )\n\n  ordered_steps = tuple(\n    replay_step_by_proof_step_id[\n      id(\n        node.proof_step\n      )\n    ]\n    for node in provenance.nodes\n    if (\n      id(\n        node.proof_step\n      )\n      in selected_step_ids\n    )\n  )\n  closure_max_depth = max(\n    replay_step.depth\n    for replay_step in ordered_steps\n  )\n  source_replay = presentation.source_replay\n  closure_replay = (\n    TodaGroupResultProofReplayResult(\n      group_result=source_replay.group_result,\n      source_entry=source_replay.source_entry,\n      root_step=source_replay.root_step,\n      steps=ordered_steps,\n      max_depth=closure_max_depth,\n    )\n  )\n\n  return build_toda_group_proof_presentation(\n    closure_replay\n  )\n'
NEW_SCOPE_TEST = 'from proof import (\n  Relation,\n  RelationType,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\nEQ1 = r"2\\nu\' = \\eta_{3}E\\eta_{3}\\eta_{5}"\nEQ2 = (\n  r"\\eta_{3}E\\eta_{3}\\eta_{5} = "\n  r"\\eta_{3}^{3}"\n)\nUNRELATED_GROUP = (\n  r"\\pi_{4}^{2} = "\n  r"\\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\}"\n)\nUNRELATED_HOPF_1 = (\n  r"H\\left(\\nu\'\\right) = E^{2}\\eta_{3}"\n)\nUNRELATED_HOPF_2 = (\n  r"E^{2}\\eta_{3} = \\eta_{5}"\n)\n\n\ndef _presentation(\n  n,\n  k,\n  depth,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = (\n    build_toda_group_result_proof_replay(\n      group_result,\n      max_depth=depth,\n    )\n  )\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase148_rc2_5_depth_zero_semantic_closure_is_identity():\n  presentation = _presentation(\n    9,\n    7,\n    0,\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  assert closure is presentation\n  assert closure.max_depth == 0\n  assert len(\n    closure.nodes\n  ) == 1\n\n\ndef test_phase148_rc2_5_order_calculation_closure_adds_only_required_chain_and_definition():\n  presentation = _presentation(\n    3,\n    3,\n    2,\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  original_ids = {\n    id(\n      node.proof_step\n    )\n    for node in presentation.nodes\n  }\n  added_nodes = tuple(\n    node\n    for node in closure.nodes\n    if id(\n      node.proof_step\n    ) not in original_ids\n  )\n  rendered = tuple(\n    _render_generic_narrative_step(\n      node.proof_step\n    )\n    for node in added_nodes\n  )\n  added_equalities = tuple(\n    node\n    for node in added_nodes\n    if (\n      isinstance(\n        node.proof_step.conclusion,\n        Relation,\n      )\n      and node.proof_step.conclusion.relation_type\n      is RelationType.EQUALITY\n    )\n  )\n\n  assert len(\n    added_nodes\n  ) == 3\n  assert len(\n    added_equalities\n  ) == 2\n  assert any(\n    EQ1 in value\n    for value in rendered\n  )\n  assert any(\n    EQ2 in value\n    for value in rendered\n  )\n  assert all(\n    UNRELATED_GROUP not in value\n    for value in rendered\n  )\n  assert all(\n    UNRELATED_HOPF_1 not in value\n    for value in rendered\n  )\n  assert all(\n    UNRELATED_HOPF_2 not in value\n    for value in rendered\n  )\n'


def replace_function(path, name, replacement):
  text = path.read_text(encoding="utf-8")
  start = text.index("def " + name + "(")
  next_def = text.find("\ndef ", start + 4)
  end = len(text) if next_def == -1 else next_def + 1
  suffix = "" if next_def == -1 else text[end:]
  path.write_text(
    text[:start] + replacement.rstrip() + "\n\n" + suffix,
    encoding="utf-8",
  )


def replace_exact(path, old, new):
  text = path.read_text(encoding="utf-8")
  if old not in text:
    raise RuntimeError(
      "Expected local R2 text not found: " + str(path)
    )
  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )


def main():
  replace_function(
    ROOT / "toda_group_proof_narrative_semantics.py",
    "build_toda_group_proof_narrative_semantic_closure_presentation",
    NEW_CLOSURE,
  )

  p = ROOT / "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py"
  text = p.read_text(encoding="utf-8")
  old_group = """  assert rendered.count(
    r"$\\pi_{6}^{3} = "
    r"\\mathbb{Z}/4\\{\\nu'\\}$"
  ) == 0
"""
  new_group = old_group.replace("== 0", "== 1")
  if old_group in text:
    text = text.replace(old_group, new_group, 1)
  p.write_text(text, encoding="utf-8")

  legacy_files = (
    "tests/test_phase133_7_group_proof_narrative_labels.py",
    "tests/test_phase134_3_pi6_3_numbered_narrative.py",
    "tests/test_phase134_5_pi6_3_reference_fact_split.py",
    "tests/test_phase134_6_pi6_3_mathbook_narrative.py",
    "tests/test_phase134_7_pi6_3_final_narrative.py",
    "tests/test_phase134_9_pi6_3_snapshot.py",
    "tests/test_phase136_1_pi6_3_narrative_prose.py",
    "tests/test_phase136_2_pi6_3_narrative_structure.py",
  )
  wrong_name = "test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_legacy_direct_route"
  restored_name = "test_phase144_6_supersedes_legacy_pi6_3_narrative_contract"
  wrong_body = r"""def test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_legacy_direct_route():
  expected, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert actual != expected
  assert r"\\tag{1}" in actual
  assert r"\\tag{2}" in actual
  assert r"\\tag{3}" in actual
  assert "(1) と (2) より、" in actual
  assert r"\\tag{1}" not in expected
"""
  restored_body = """def test_phase144_6_supersedes_legacy_pi6_3_narrative_contract():
  expected, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert actual == expected
"""
  for rel in legacy_files:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if wrong_name in text:
      start = text.index("def " + wrong_name + "(")
      next_def = text.find("\ndef ", start + 4)
      end = len(text) if next_def == -1 else next_def + 1
      suffix = "" if next_def == -1 else text[end:]
      text = text[:start] + restored_body.rstrip() + "\n\n" + suffix
      path.write_text(text, encoding="utf-8")

  parity = (
    (
      "tests/test_phase144_6_pi6_generic_production_route.py",
      "test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_direct_contribution_renderer",
      "test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer",
    ),
    (
      "tests/test_phase144_6_public_route_cutover.py",
      "test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_direct_contribution_renderer",
      "test_phase144_6_public_pi6_3_equals_contribution_renderer",
    ),
  )
  for rel, wrong, restored in parity:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if wrong not in text:
      continue
    start = text.index("def " + wrong + "(")
    next_def = text.find("\ndef ", start + 4)
    end = len(text) if next_def == -1 else next_def + 1
    suffix = "" if next_def == -1 else text[end:]
    restored_body = f"""def {restored}():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_presentation_data()

  expected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  actual = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert actual == expected
"""
    text = text[:start] + restored_body.rstrip() + "\n\n" + suffix
    path.write_text(text, encoding="utf-8")

  p = ROOT / "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
  text = p.read_text(encoding="utf-8")
  old = """  assert len(
    added_nodes
  ) == 3
  assert sum(
    isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
    for node in added_nodes
  ) == 1
"""
  new = """  assert len(
    added_nodes
  ) == 3
  assert sum(
    isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
    for node in added_nodes
  ) == 1
"""
  if old not in text:
    raise RuntimeError("R25-9b R2 expectation not found")
  p.write_text(text.replace(old, new, 1), encoding="utf-8")

  (ROOT / "tests/test_phase148_rc2_5_semantic_closure_scope.py").write_text(
    NEW_SCOPE_TEST,
    encoding="utf-8",
  )

  print("Phase 148 RC2-5 Repair R4 applied.")
  print("Production: order-calculation semantic closure.")
  print("Tests: R2 accidental changes repaired; RC2 expectations retained.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
