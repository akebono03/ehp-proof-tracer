from pathlib import Path

ROOT = Path.cwd()
NEW_CLOSURE = 'def build_toda_group_proof_narrative_semantic_closure_presentation(\n  presentation: TodaGroupProofPresentation,\n) -> TodaGroupProofPresentation:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if presentation.max_depth == 0:\n    return presentation\n\n  provenance = (\n    extract_toda_recursive_proof_provenance(\n      presentation.source_replay.group_result\n    )\n  )\n  selected_step_ids = {\n    id(\n      node.proof_step\n    )\n    for node in presentation.nodes\n  }\n  original_step_ids = frozenset(\n    selected_step_ids\n  )\n  equality_edges_by_parent_id = {}\n\n  for edge in provenance.edges:\n    parent_statement = edge.parent_step.conclusion\n    premise_statement = edge.premise_step.conclusion\n\n    if (\n      not isinstance(\n        parent_statement,\n        Relation,\n      )\n      or parent_statement.relation_type\n      is not RelationType.EQUALITY\n      or not isinstance(\n        premise_statement,\n        Relation,\n      )\n      or premise_statement.relation_type\n      is not RelationType.EQUALITY\n    ):\n      continue\n\n    equality_edges_by_parent_id.setdefault(\n      id(\n        edge.parent_step\n      ),\n      [],\n    ).append(\n      edge\n    )\n\n  for parent_step_id, equality_edges in (\n    equality_edges_by_parent_id.items()\n  ):\n    if (\n      parent_step_id not in original_step_ids\n      or len(\n        equality_edges\n      ) < 2\n    ):\n      continue\n\n    for edge in equality_edges:\n      selected_step_ids.add(\n        id(\n          edge.premise_step\n        )\n      )\n\n  changed = True\n\n  while changed:\n    changed = False\n\n    for edge in provenance.edges:\n      if (\n        id(\n          edge.parent_step\n        )\n        not in selected_step_ids\n      ):\n        continue\n\n      key = (\n        _inference_rule_name(\n          edge.parent_step\n        ),\n        edge.premise_index,\n      )\n\n      if (\n        key\n        not in _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX\n      ):\n        continue\n\n      premise_step_id = id(\n        edge.premise_step\n      )\n\n      if premise_step_id in selected_step_ids:\n        continue\n\n      selected_step_ids.add(\n        premise_step_id\n      )\n      changed = True\n\n  if selected_step_ids == original_step_ids:\n    return presentation\n\n  replay_step_by_proof_step_id = {\n    id(\n      replay_step.proof_step\n    ): replay_step\n    for replay_step in presentation.source_replay.steps\n  }\n\n  for node in provenance.nodes:\n    proof_step_id = id(\n      node.proof_step\n    )\n\n    if (\n      proof_step_id not in selected_step_ids\n      or proof_step_id\n      in replay_step_by_proof_step_id\n    ):\n      continue\n\n    replay_step_by_proof_step_id[\n      proof_step_id\n    ] = TodaGroupResultProofReplayStep(\n      depth=node.shortest_depth,\n      proof_step=node.proof_step,\n      role=node.role,\n    )\n\n  ordered_steps = tuple(\n    replay_step_by_proof_step_id[\n      id(\n        node.proof_step\n      )\n    ]\n    for node in provenance.nodes\n    if (\n      id(\n        node.proof_step\n      )\n      in selected_step_ids\n    )\n  )\n  closure_max_depth = max(\n    replay_step.depth\n    for replay_step in ordered_steps\n  )\n  source_replay = presentation.source_replay\n  closure_replay = (\n    TodaGroupResultProofReplayResult(\n      group_result=source_replay.group_result,\n      source_entry=source_replay.source_entry,\n      root_step=source_replay.root_step,\n      steps=ordered_steps,\n      max_depth=closure_max_depth,\n    )\n  )\n\n  return build_toda_group_proof_presentation(\n    closure_replay\n  )\n'
NEW_TEST = 'from proof import (\n  Relation,\n  RelationType,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\nEQ1 = r"2\\nu\' = \\eta_{3}E\\eta_{3}\\eta_{5}"\nEQ2 = (\n  r"\\eta_{3}E\\eta_{3}\\eta_{5} = "\n  r"\\eta_{3}^{3}"\n)\n\n\ndef _presentation(\n  n,\n  k,\n  depth,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = (\n    build_toda_group_result_proof_replay(\n      group_result,\n      max_depth=depth,\n    )\n  )\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase148_rc2_5_depth_zero_semantic_closure_is_identity():\n  presentation = _presentation(\n    9,\n    7,\n    0,\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  assert closure is presentation\n  assert closure.max_depth == 0\n  assert len(\n    closure.nodes\n  ) == 1\n\n\ndef test_phase148_rc2_5_calculation_closure_adds_only_required_equality_chain():\n  presentation = _presentation(\n    3,\n    3,\n    2,\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n  original_ids = {\n    id(\n      node.proof_step\n    )\n    for node in presentation.nodes\n  }\n  added_nodes = tuple(\n    node\n    for node in closure.nodes\n    if id(\n      node.proof_step\n    ) not in original_ids\n  )\n  added_equalities = tuple(\n    node\n    for node in added_nodes\n    if (\n      isinstance(\n        node.proof_step.conclusion,\n        Relation,\n      )\n      and node.proof_step.conclusion.relation_type\n      is RelationType.EQUALITY\n    )\n  )\n  rendered = tuple(\n    _render_generic_narrative_step(\n      node.proof_step\n    )\n    for node in added_equalities\n  )\n\n  assert len(\n    added_nodes\n  ) == 3\n  assert len(\n    added_equalities\n  ) == 2\n  assert any(\n    EQ1 in value\n    for value in rendered\n  )\n  assert any(\n    EQ2 in value\n    for value in rendered\n  )\n'

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

def replace_exact(path, old, new, count=-1):
  text = path.read_text(encoding="utf-8")
  if old not in text:
    raise RuntimeError("Expected text not found: " + str(path))
  path.write_text(
    text.replace(old, new, count),
    encoding="utf-8",
  )

def main():
  replace_function(
    ROOT / "toda_group_proof_narrative_semantics.py",
    "build_toda_group_proof_narrative_semantic_closure_presentation",
    NEW_CLOSURE,
  )

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
  old = """def test_phase144_6_supersedes_legacy_pi6_3_narrative_contract():
  expected, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert actual == expected
"""
  new = r"""def test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_legacy_direct_route():
  expected, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert actual != expected
  assert r"\tag{1}" in actual
  assert r"\tag{2}" in actual
  assert r"\tag{3}" in actual
  assert "(1) と (2) より、" in actual
  assert r"\tag{1}" not in expected
"""
  for rel in legacy_files:
    replace_exact(ROOT / rel, old, new)

  p = ROOT / "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py"
  text = p.read_text(encoding="utf-8")
  text = text.replace("  ) == 1\n", "  ) == 0\n", 1)
  marker = """  assert rendered.count(
    exactness
  ) == 1
"""
  text = text.replace(marker, marker.replace("== 1", "== 0"))
  p.write_text(text, encoding="utf-8")

  p = ROOT / "tests/test_phase143_49_dependency_label_narrative_policy.py"
  text = p.read_text(encoding="utf-8")
  old_phrase = """  assert (
    "次の完全列を考える."
    in rendered
  )
"""
  text = text.replace(
    old_phrase,
    old_phrase.replace("    in rendered", "    not in rendered"),
    2,
  )
  p.write_text(text, encoding="utf-8")

  p = ROOT / "tests/test_phase143_50_generic_statement_prose_renderer.py"
  text = p.read_text(encoding="utf-8")
  targets = (
    r"""  assert (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
    in rendered
  )
""",
    r"""  assert (
    r"$\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}$ は完全である."
    in rendered
  )
""",
  )
  for target in targets:
    text = text.replace(
      target,
      target.replace("    in rendered", "    not in rendered"),
    )
  p.write_text(text, encoding="utf-8")

  p = ROOT / "tests/test_phase143_63a_r_exactness_repair.py"
  text = p.read_text(encoding="utf-8")
  text = text.replace(
    "  assert rendered.count(expected) == 1\n",
    "  assert rendered.count(expected) == 0\n",
    2,
  )
  p.write_text(text, encoding="utf-8")

  p = ROOT / "tests/test_phase143_63a_residual_fallback_provenance.py"
  text = p.read_text(encoding="utf-8")
  target = r"""  assert (
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
    in rendered
  )
"""
  text = text.replace(
    target,
    target.replace("    in rendered", "    not in rendered"),
  )
  p.write_text(text, encoding="utf-8")

  parity = (
    (
      "tests/test_phase144_6_pi6_generic_production_route.py",
      "test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer",
    ),
    (
      "tests/test_phase144_6_public_route_cutover.py",
      "test_phase144_6_public_pi6_3_equals_contribution_renderer",
    ),
  )
  replacement = r"""def test_phase148_rc2_5_public_pi6_3_applies_semantic_closure_before_direct_contribution_renderer():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _pi6_3_presentation_data()

  direct = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert public != direct
  assert r"\tag{1}" in public
  assert r"\tag{2}" in public
  assert r"\tag{3}" in public
  assert "(1) と (2) より、" in public
  assert r"\tag{1}" not in direct
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in public
  )
"""
  for rel, name in parity:
    replace_function(ROOT / rel, name, replacement)

  p = ROOT / "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
  old_r25 = """  assert len(
    added_nodes
  ) == 1
  assert isinstance(
    added_nodes[
      0
    ].proof_step.conclusion,
    TodaBracketMembershipStatement,
  )
"""
  new_r25 = """  assert len(
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
  replace_exact(p, old_r25, new_r25)

  (ROOT / "tests/test_phase148_rc2_5_semantic_closure_scope.py").write_text(
    NEW_TEST,
    encoding="utf-8",
  )

  print("Phase 148 RC2-5 Repair R2 applied.")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())