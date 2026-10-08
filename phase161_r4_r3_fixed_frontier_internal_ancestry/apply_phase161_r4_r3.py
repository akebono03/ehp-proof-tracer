from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

RENDERER = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R4_TEST = REPO_ROOT / "tests" / "test_phase161_r4_pi4_2_specialization_frontier.py"
R4_REPAIR1_TEST = REPO_ROOT / "tests" / "test_phase161_r4_repair1_pi4_2_semantic_frontier.py"
R4_R3_TEST = REPO_ROOT / "tests" / "test_phase161_r4_r3_fixed_frontier_internal_ancestry.py"

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

FIXED_HELPER = 'def _toda_group_proof_narrative_fixed_frontier_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  fixed_frontier_step_ids = {\n    id(\n      proof_step\n    )\n    for entry in reference_entries\n    for proof_step in entry.proof_steps\n    for boundary in (\n      classify_toda_literature_statement_step(\n        proof_step\n      ),\n    )\n    if (\n      id(\n        proof_step\n      )\n      in frontier_step_ids\n      and boundary is not None\n      and boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n    )\n  }\n\n  if not fixed_frontier_step_ids:\n    return frozenset()\n\n  consumers_by_step_id = {}\n\n  for edge in presentation.edges:\n    consumers_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  closure_step_ids = set(\n    fixed_frontier_step_ids\n  )\n  internal_step_ids = set()\n\n  changed = True\n\n  while changed:\n    changed = False\n\n    for edge in presentation.edges:\n      parent_step_id = id(\n        edge.parent_step\n      )\n\n      if parent_step_id not in closure_step_ids:\n        continue\n\n      premise_step = edge.premise_step\n      premise_step_id = id(\n        premise_step\n      )\n\n      if (\n        premise_step\n        is presentation.root_step\n        or premise_step_id\n        in closure_step_ids\n        or premise_step_id\n        in frontier_step_ids\n      ):\n        continue\n\n      consumers = tuple(\n        consumers_by_step_id.get(\n          premise_step_id,\n          (),\n        )\n      )\n\n      if not consumers:\n        continue\n\n      if not all(\n        id(\n          consumer\n        )\n        in closure_step_ids\n        for consumer in consumers\n      ):\n        continue\n\n      closure_step_ids.add(\n        premise_step_id\n      )\n      internal_step_ids.add(\n        premise_step_id\n      )\n      changed = True\n\n  return frozenset(\n    internal_step_ids\n  )\n'
INTERNAL_FUNCTION = 'def _toda_group_proof_narrative_reference_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  selected_step_ids = set()\n\n  for entry in reference_entries:\n    candidate_steps = []\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          proof_step,\n          rendered_statement,\n        )\n      ):\n        continue\n\n      if rendered_statement in seen_rendered_statements:\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n\n    selected_step_ids.update(\n      id(\n        proof_step\n      )\n      for proof_step in selected_steps\n    )\n\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  fixed_frontier_internal_step_ids = (\n    _toda_group_proof_narrative_fixed_frontier_internal_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  return frozenset(\n    (\n      {\n        step_id\n        for step_id in owned_step_ids\n        if step_id not in selected_step_ids\n      }\n      | set(\n        fixed_frontier_internal_step_ids\n      )\n    )\n  )\n'
R4_TEST_SOURCE = 'from homotopy_groups import (\n  TodaPrimaryGroup,\n)\nfrom proof import (\n  Relation,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_pi4_2_presentations():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  semantic = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    semantic,\n  )\n\n\ndef _phase161_r4_frontier_entries():\n  _, presentation = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return (\n    presentation,\n    entries,\n  )\n\n\ndef test_phase161_r4_pi4_2_same_locator_fixed_statement_survives_root_exclusion():\n  presentation, entries = (\n    _phase161_r4_frontier_entries()\n  )\n\n  toda52_entries = tuple(\n    entry\n    for entry in entries\n    if entry.reference.locator == "(5.2)"\n  )\n\n  assert len(\n    toda52_entries\n  ) == 1\n\n  assert all(\n    proof_step is not presentation.root_step\n    for proof_step in toda52_entries[\n      0\n    ].proof_steps\n  )\n\n\ndef test_phase161_r4_pi4_2_specialization_plan_is_semantic():\n  presentation, entries = (\n    _phase161_r4_frontier_entries()\n  )\n  plan = (\n    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n      presentation,\n      entries,\n    )\n  )\n\n  assert plan is not None\n\n  (\n    _,\n    _,\n    source_step,\n    specialized_source,\n    specialized_target,\n    _,\n    _,\n    target_dimension,\n  ) = plan\n\n  assert target_dimension == 4\n\n  assert specialized_source == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=3,\n  )\n  assert specialized_target == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=2,\n  )\n\n  assert isinstance(\n    source_step.conclusion,\n    Relation,\n  )\n  assert (\n    source_step.conclusion.lhs\n    == specialized_source\n  )\n\n\ndef test_phase161_r4_pi4_2_public_reference_is_general_and_body_is_specialized():\n  raw, _ = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert (\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}$"\n    in reference\n  )\n\n  assert "Proposition 4.4" not in reference\n\n  assert "[R1]" in body\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n  assert "同型" in body\n\n  assert (\n    r"\\eta_{3} \\mapsto "\n    in body\n  )\n\n  assert (\n    r"\\pi_{i}^{3}"\n    not in body\n  )\n  assert (\n    r"\\pi_{i}^{2}"\n    not in body\n  )\n  assert (\n    r"\\pi_{i - 1}^{1}"\n    not in body\n  )\n  assert (\n    "分解写像の第二成分"\n    not in body\n  )\n  assert (\n    "Proposition 4.4"\n    not in body\n  )\n\n\ndef test_phase161_r4_pi4_2_keeps_target_and_qed():\n  raw, _ = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in rendered\n  )\n  assert "□" in rendered\n'
R4_REPAIR1_TEST_SOURCE = 'from homotopy_groups import (\n  TodaPrimaryGroup,\n)\nfrom proof import (\n  Relation,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_repair1_pi4_2_presentations():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  semantic = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    semantic,\n  )\n\n\ndef _phase161_r4_repair1_entries():\n  _, presentation = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return (\n    presentation,\n    entries,\n  )\n\n\ndef test_phase161_r4_repair1_toda52_runtime_fields_drive_specialization():\n  presentation, entries = (\n    _phase161_r4_repair1_entries()\n  )\n  plan = (\n    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n      presentation,\n      entries,\n    )\n  )\n\n  assert plan is not None\n\n  (\n    _,\n    fixed_step,\n    source_step,\n    specialized_source,\n    specialized_target,\n    _,\n    _,\n    target_dimension,\n  ) = plan\n\n  assert getattr(\n    fixed_step.conclusion,\n    "source_group",\n    None,\n  ) is not None\n  assert getattr(\n    fixed_step.conclusion,\n    "target_group",\n    None,\n  ) is not None\n  assert getattr(\n    fixed_step.conclusion,\n    "composition",\n    None,\n  ) is not None\n\n  assert target_dimension == 4\n  assert specialized_source == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=3,\n  )\n  assert specialized_target == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=2,\n  )\n\n  assert isinstance(\n    source_step.conclusion,\n    Relation,\n  )\n\n\ndef test_phase161_r4_repair1_fixed_toda52_is_frontier_but_prop44_is_not():\n  presentation, entries = (\n    _phase161_r4_repair1_entries()\n  )\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n\n  toda52 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "(5.2)"\n  )\n  prop44 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "Proposition 4.4"\n  )\n\n  assert any(\n    id(\n      proof_step\n    )\n    in frontier_step_ids\n    for proof_step in toda52.proof_steps\n  )\n  assert all(\n    id(\n      proof_step\n    )\n    not in frontier_step_ids\n    for proof_step in prop44.proof_steps\n  )\n\n\ndef test_phase161_r4_repair1_public_pi4_2_has_general_reference_and_specialized_body():\n  raw, _ = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert (\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}$"\n    in reference\n  )\n\n  assert "Proposition 4.4" not in reference\n\n  assert "[R1]" in body\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n  assert "同型" in body\n  assert (\n    r"\\eta_{3} \\mapsto"\n    in body\n  )\n\n  assert r"\\pi_{i}^{3}" not in body\n  assert r"\\pi_{i}^{2}" not in body\n  assert r"\\pi_{i - 1}^{1}" not in body\n  assert "分解写像の第二成分" not in body\n  assert "Proposition 4.4" not in body\n\n\ndef test_phase161_r4_repair1_keeps_target_and_qed():\n  raw, _ = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in rendered\n  )\n  assert "□" in rendered\n'
R4_R3_TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _filter_toda_group_proof_narrative_reference_entries_to_frontier,\n  _toda_group_proof_narrative_fixed_frontier_internal_step_ids,\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n  _toda_group_proof_narrative_reference_internal_step_ids,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_r3_pi4_2_data():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  semantic_sidecar = (\n    build_toda_group_proof_narrative_semantic_sidecar(\n      presentation\n    )\n  )\n  blocks = build_toda_group_proof_narrative_blocks(\n    presentation,\n    semantic_sidecar=semantic_sidecar,\n  )\n  arguments = build_toda_group_proof_narrative_arguments(\n    presentation,\n    blocks,\n    semantic_sidecar=semantic_sidecar,\n  )\n\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, statement_lines = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  entries, statement_lines = (\n    _filter_toda_group_proof_narrative_reference_entries_to_frontier(\n      entries,\n      statement_lines,\n      frontier_step_ids,\n    )\n  )\n\n  return (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    entries,\n  )\n\n\ndef test_phase161_r4_r3_prop44_steps_are_internal_to_fixed_toda52_frontier():\n  (\n    _,\n    presentation,\n    _,\n    _,\n    _,\n    entries,\n  ) = _phase161_r4_r3_pi4_2_data()\n\n  fixed_internal_step_ids = (\n    _toda_group_proof_narrative_fixed_frontier_internal_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  internal_step_ids = (\n    _toda_group_proof_narrative_reference_internal_step_ids(\n      presentation,\n      entries,\n    )\n  )\n\n  prop44_step = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 n=2 specialization"\n    )\n  )\n  restriction_step = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 second-summand restriction"\n    )\n  )\n\n  assert id(\n    prop44_step\n  ) in fixed_internal_step_ids\n  assert id(\n    restriction_step\n  ) in fixed_internal_step_ids\n\n  assert id(\n    prop44_step\n  ) in internal_step_ids\n  assert id(\n    restriction_step\n  ) in internal_step_ids\n\n\ndef test_phase161_r4_r3_public_body_stops_at_toda52_fixed_statement():\n  raw = _phase161_r4_r3_pi4_2_data()[\n    0\n  ]\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert "Proposition 4.4" not in reference\n\n  assert (\n    r"\\pi_{i - 1}^{1} \\oplus "\n    r"\\pi_{i}^{3} \\to "\n    r"\\pi_{i}^{2}"\n    not in body\n  )\n  assert "分解写像の第二成分" not in body\n\n  assert "[R1]" in body\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n  assert "同型" in body\n\n  assert (\n    r"\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n    in body\n  )\n  assert (\n    r"\\eta_{3} \\mapsto "\n    r"\\eta_{2}\\eta_{3}"\n    in body\n  )\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in body\n  )\n  assert "□" in body\n'


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  matches = tuple(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == function_name
    )
  )

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      f"Expected exactly one {function_name}, "
      f"found {len(matches)}."
    )

  node = matches[
    0
  ]
  lines = source.splitlines(
    keepends=True
  )
  replacement_lines = [
    line + "\n"
    for line in replacement.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + replacement_lines
    + lines[
      node.end_lineno:
    ]
  )


def _insert_before_function(
  source: str,
  function_name: str,
  addition: str,
) -> str:
  tree = ast.parse(
    source
  )
  matches = tuple(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == function_name
    )
  )

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      f"Expected exactly one {function_name}, "
      f"found {len(matches)}."
    )

  node = matches[
    0
  ]
  lines = source.splitlines(
    keepends=True
  )
  addition_lines = [
    line + "\n"
    for line in (
      addition.rstrip(
        "\n"
      )
      + "\n\n"
    ).split(
      "\n"
    )[
      :-1
    ]
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + addition_lines
    + lines[
      node.lineno - 1:
    ]
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  tree = ast.parse(
    source
  )
  matches = tuple(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == function_name
    )
  )

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      f"Expected exactly one {function_name}, "
      f"found {len(matches)}."
    )

  node = matches[
    0
  ]
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def main():
  source = RENDERER.read_text(
    encoding="utf-8"
  )

  required_names = (
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    "_toda_group_proof_narrative_reference_internal_step_ids",
    "_filter_toda_group_proof_narrative_reference_entries_to_frontier",
  )

  tree = ast.parse(
    source
  )
  names = {
    node.name
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  for required_name in required_names:
    if required_name not in names:
      raise RuntimeError(
        f"Required R4 function missing: {required_name}"
      )

  updated = source

  if (
    "_toda_group_proof_narrative_fixed_frontier_internal_step_ids"
    not in names
  ):
    updated = _insert_before_function(
      updated,
      "_toda_group_proof_narrative_reference_internal_step_ids",
      FIXED_HELPER,
    )

  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_reference_internal_step_ids",
    INTERNAL_FUNCTION,
  )

  ast.parse(
    updated
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )
  shutil.copy2(
    R4_TEST,
    BACKUP_DIR / R4_TEST.name,
  )
  shutil.copy2(
    R4_REPAIR1_TEST,
    BACKUP_DIR / R4_REPAIR1_TEST.name,
  )

  RENDERER.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )
  R4_TEST.write_text(
    R4_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  R4_REPAIR1_TEST.write_text(
    R4_REPAIR1_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  R4_R3_TEST.write_text(
    R4_R3_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for function_name in (
    "_toda_group_proof_narrative_fixed_frontier_internal_step_ids",
    "_toda_group_proof_narrative_reference_internal_step_ids",
  ):
    (
      OUTPUT_DIR
      / (
        function_name
        + ".py.txt"
      )
    ).write_text(
      _extract_function(
        updated,
        function_name,
      ),
      encoding="utf-8",
      newline="\n",
    )

  (
    OUTPUT_DIR
    / "test_phase161_r4_pi4_2_specialization_frontier.py.txt"
  ).write_text(
    R4_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_repair1_pi4_2_semantic_frontier.py.txt"
  ).write_text(
    R4_REPAIR1_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_r4_r3_fixed_frontier_internal_ancestry.py.txt"
  ).write_text(
    R4_R3_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    RENDERER,
  )
  print(
    "Updated:",
    R4_TEST,
  )
  print(
    "Updated:",
    R4_REPAIR1_TEST,
  )
  print(
    "Wrote:",
    R4_R3_TEST,
  )
  print(
    "Full changed/new functions and tests written to output/."
  )


if __name__ == "__main__":
  main()
