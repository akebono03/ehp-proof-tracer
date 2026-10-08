from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

RENDERER = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = REPO_ROOT / "tests" / "test_phase161_r4_repair1_pi4_2_semantic_frontier.py"

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

FRONTIER_FUNCTION = 'def _toda_group_proof_narrative_reference_frontier_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  children_by_step_id = {}\n\n  for edge in presentation.edges:\n    children_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  root_step = presentation.root_step\n  frontier_step_ids = set()\n\n  for entry in reference_entries:\n    for source_step in entry.proof_steps:\n      queue = deque(\n        [\n          source_step,\n        ]\n      )\n      visited = set()\n\n      while queue:\n        current_step = queue.popleft()\n        current_step_id = id(\n          current_step\n        )\n\n        if current_step_id in visited:\n          continue\n\n        visited.add(\n          current_step_id\n        )\n\n        if current_step is root_step:\n          frontier_step_ids.add(\n            id(\n              source_step\n            )\n          )\n          break\n\n        for child_step in children_by_step_id.get(\n          current_step_id,\n          (),\n        ):\n          if child_step is root_step:\n            frontier_step_ids.add(\n              id(\n                source_step\n              )\n            )\n            queue.clear()\n            break\n\n          child_reference = (\n            extract_toda_group_proof_step_literature_reference(\n              child_step\n            )\n          )\n\n          if (\n            child_reference is not None\n            and child_reference != entry.reference\n          ):\n            child_boundary = (\n              classify_toda_literature_statement_step(\n                child_step\n              )\n            )\n\n            if (\n              child_boundary is not None\n              and child_boundary.classification\n              is TodaLiteratureStatementClassification.FIXED_STATEMENT\n            ):\n              continue\n\n            root_reference = (\n              extract_toda_group_proof_step_literature_reference(\n                root_step\n              )\n            )\n\n            if child_reference != root_reference:\n              continue\n\n          queue.append(\n            child_step\n          )\n\n  return frozenset(\n    frontier_step_ids\n  )\n'
FRONTIER_FILTER_FUNCTION = 'def _filter_toda_group_proof_narrative_reference_entries_to_frontier(\n  reference_entries,\n  statement_lines_by_reference_number,\n  frontier_step_ids: frozenset[int],\n):\n  retained_entries = tuple(\n    entry\n    for entry in reference_entries\n    if any(\n      id(\n        proof_step\n      )\n      in frontier_step_ids\n      for proof_step in entry.proof_steps\n    )\n  )\n\n  number_map = {\n    entry.number: new_number\n    for new_number, entry in enumerate(\n      retained_entries,\n      start=1,\n    )\n  }\n\n  filtered_entries = tuple(\n    replace(\n      entry,\n      number=number_map[\n        entry.number\n      ],\n    )\n    for entry in retained_entries\n  )\n\n  filtered_statement_lines = {\n    number_map[\n      entry.number\n    ]: statement_lines_by_reference_number[\n      entry.number\n    ]\n    for entry in retained_entries\n    if entry.number\n    in statement_lines_by_reference_number\n  }\n\n  return (\n    filtered_entries,\n    filtered_statement_lines,\n  )\n'
PLAN_FUNCTION = 'def _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n):\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  root_step = presentation.root_step\n\n  if not isinstance(\n    root_step.conclusion,\n    Relation,\n  ):\n    return None\n\n  target_group = (\n    root_step.conclusion.lhs\n  )\n\n  if not isinstance(\n    target_group,\n    TodaPrimaryGroup,\n  ):\n    return None\n\n  target_dimension = (\n    target_group.group_dimension\n  )\n\n  if (\n    not isinstance(\n      target_dimension,\n      int,\n    )\n    or isinstance(\n      target_dimension,\n      bool,\n    )\n  ):\n    return None\n\n  matches = []\n\n  for entry in reference_entries:\n    for proof_step in entry.proof_steps:\n      boundary = (\n        classify_toda_literature_statement_step(\n          proof_step\n        )\n      )\n\n      if (\n        boundary is None\n        or boundary.classification\n        is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n        or boundary.component_key\n        != "eta2_composition_isomorphism"\n      ):\n        continue\n\n      statement = proof_step.conclusion\n      source_group = getattr(\n        statement,\n        "source_group",\n        None,\n      )\n      map_target_group = getattr(\n        statement,\n        "target_group",\n        None,\n      )\n      composition = getattr(\n        statement,\n        "composition",\n        None,\n      )\n\n      if (\n        not isinstance(\n          source_group,\n          TodaPrimaryGroup,\n        )\n        or not isinstance(\n          map_target_group,\n          TodaPrimaryGroup,\n        )\n        or composition is None\n      ):\n        continue\n\n      symbol = (\n        map_target_group.group_dimension\n      )\n\n      if not isinstance(\n        symbol,\n        ScalarSymbol,\n      ):\n        continue\n\n      specialized_source = (\n        _phase159_r1_7c_r3_specialize_primary_group(\n          source_group,\n          symbol,\n          target_dimension,\n        )\n      )\n      specialized_target = (\n        _phase159_r1_7c_r3_specialize_primary_group(\n          map_target_group,\n          symbol,\n          target_dimension,\n        )\n      )\n\n      if (\n        specialized_source is None\n        or specialized_target != target_group\n      ):\n        continue\n\n      source_steps = tuple(\n        premise_step\n        for premise_step in root_step.premises\n        if (\n          isinstance(\n            premise_step.conclusion,\n            Relation,\n          )\n          and premise_step.conclusion.lhs\n          == specialized_source\n        )\n      )\n\n      if len(\n        source_steps\n      ) != 1:\n        continue\n\n      source_step = source_steps[\n        0\n      ]\n      source_structure = (\n        source_step.conclusion.rhs\n      )\n      target_structure = (\n        root_step.conclusion.rhs\n      )\n      source_generator = getattr(\n        source_structure,\n        "generator",\n        None,\n      )\n      target_generator = getattr(\n        target_structure,\n        "generator",\n        None,\n      )\n      source_order = getattr(\n        source_structure,\n        "order",\n        None,\n      )\n      target_order = getattr(\n        target_structure,\n        "order",\n        None,\n      )\n\n      if (\n        source_generator is None\n        or target_generator is None\n        or source_order != target_order\n      ):\n        continue\n\n      matches.append(\n        (\n          entry,\n          proof_step,\n          source_step,\n          specialized_source,\n          specialized_target,\n          source_generator,\n          target_generator,\n          target_dimension,\n        )\n      )\n\n  if len(\n    matches\n  ) != 1:\n    return None\n\n  return matches[\n    0\n  ]\n'
TEST_SOURCE = 'from homotopy_groups import (\n  TodaPrimaryGroup,\n)\nfrom proof import (\n  Relation,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_repair1_pi4_2_presentations():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  semantic = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    semantic,\n  )\n\n\ndef _phase161_r4_repair1_entries():\n  _, presentation = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return (\n    presentation,\n    entries,\n  )\n\n\ndef test_phase161_r4_repair1_toda52_runtime_fields_drive_specialization():\n  presentation, entries = (\n    _phase161_r4_repair1_entries()\n  )\n  plan = (\n    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n      presentation,\n      entries,\n    )\n  )\n\n  assert plan is not None\n\n  (\n    _,\n    fixed_step,\n    source_step,\n    specialized_source,\n    specialized_target,\n    _,\n    _,\n    target_dimension,\n  ) = plan\n\n  assert getattr(\n    fixed_step.conclusion,\n    "source_group",\n    None,\n  ) is not None\n  assert getattr(\n    fixed_step.conclusion,\n    "target_group",\n    None,\n  ) is not None\n  assert getattr(\n    fixed_step.conclusion,\n    "composition",\n    None,\n  ) is not None\n\n  assert target_dimension == 4\n  assert specialized_source == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=3,\n  )\n  assert specialized_target == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=2,\n  )\n\n  assert isinstance(\n    source_step.conclusion,\n    Relation,\n  )\n\n\ndef test_phase161_r4_repair1_fixed_toda52_is_frontier_but_prop44_is_not():\n  presentation, entries = (\n    _phase161_r4_repair1_entries()\n  )\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n\n  toda52 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "(5.2)"\n  )\n  prop44 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "Proposition 4.4"\n  )\n\n  assert any(\n    id(\n      proof_step\n    )\n    in frontier_step_ids\n    for proof_step in toda52.proof_steps\n  )\n  assert all(\n    id(\n      proof_step\n    )\n    not in frontier_step_ids\n    for proof_step in prop44.proof_steps\n  )\n\n\ndef test_phase161_r4_repair1_public_pi4_2_has_general_reference_and_specialized_body():\n  raw, _ = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert (\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}$"\n    in reference\n  )\n\n  assert "Proposition 4.4" not in reference\n\n  assert (\n    r"[R1]を $i=4$ に適用すると, "\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}$ "\n    r"は同型である."\n    in body\n  )\n  assert (\n    r"\\eta_{3} \\mapsto"\n    in body\n  )\n\n  assert r"\\pi_{i}^{3}" not in body\n  assert r"\\pi_{i}^{2}" not in body\n  assert r"\\pi_{i - 1}^{1}" not in body\n  assert "分解写像の第二成分" not in body\n  assert "Proposition 4.4" not in body\n\n\ndef test_phase161_r4_repair1_keeps_target_and_qed():\n  raw, _ = (\n    _phase161_r4_repair1_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in rendered\n  )\n  assert "□" in rendered\n'

RENDER_FUNCTION_NAME = (
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"
)

ROOT_EXCLUSION_ANCHOR = """  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
"""

ROOT_EXCLUSION_REPLACEMENT = ROOT_EXCLUSION_ANCHOR + """
  phase161_r4_frontier_step_ids = (
    _toda_group_proof_narrative_reference_frontier_step_ids(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    _filter_toda_group_proof_narrative_reference_entries_to_frontier(
      reference_entries,
      statement_lines_by_reference_number,
      phase161_r4_frontier_step_ids,
    )
  )
"""


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

  required_functions = (
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    "_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan",
    "specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application",
    RENDER_FUNCTION_NAME,
  )

  tree = ast.parse(
    source
  )
  existing_function_names = {
    node.name
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  for function_name in required_functions:
    if function_name not in existing_function_names:
      raise RuntimeError(
        f"Required R4 function is missing: {function_name}"
      )

  updated = _replace_function(
    source,
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    FRONTIER_FUNCTION,
  )
  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan",
    PLAN_FUNCTION,
  )

  if (
    "_filter_toda_group_proof_narrative_reference_entries_to_frontier"
    not in updated
  ):
    updated = _insert_before_function(
      updated,
      "_toda_group_proof_narrative_reference_frontier_step_ids",
      FRONTIER_FILTER_FUNCTION,
    )

  render_function = _extract_function(
    updated,
    RENDER_FUNCTION_NAME,
  )

  if (
    "phase161_r4_frontier_step_ids"
    not in render_function
  ):
    count = render_function.count(
      ROOT_EXCLUSION_ANCHOR
    )

    if count != 1:
      raise RuntimeError(
        "Expected one root-exclusion anchor in render function, "
        f"found {count}."
      )

    render_function = render_function.replace(
      ROOT_EXCLUSION_ANCHOR,
      ROOT_EXCLUSION_REPLACEMENT,
      1,
    )

    updated = _replace_function(
      updated,
      RENDER_FUNCTION_NAME,
      render_function,
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

  RENDERER.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
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

  for function_name in (
    "_filter_toda_group_proof_narrative_reference_entries_to_frontier",
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    "_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan",
    "specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application",
    RENDER_FUNCTION_NAME,
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
    / "test_phase161_r4_repair1_pi4_2_semantic_frontier.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    RENDERER,
  )
  print(
    "Wrote:",
    TEST,
  )
  print(
    "Full changed/new functions and test file written to output/."
  )


if __name__ == "__main__":
  main()
