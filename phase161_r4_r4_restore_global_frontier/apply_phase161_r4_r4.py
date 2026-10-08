from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

RENDERER = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = REPO_ROOT / "tests" / "test_phase161_r4_r4_restore_global_frontier.py"

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

FRONTIER_FUNCTION = 'def _toda_group_proof_narrative_reference_frontier_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  children_by_step_id = {}\n\n  for edge in presentation.edges:\n    children_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  root_step = presentation.root_step\n  root_reference = (\n    extract_toda_group_proof_step_literature_reference(\n      root_step\n    )\n  )\n  frontier_step_ids = set()\n\n  for entry in reference_entries:\n    for source_step in entry.proof_steps:\n      queue = deque(\n        [\n          source_step,\n        ]\n      )\n      visited = set()\n\n      while queue:\n        current_step = queue.popleft()\n        current_step_id = id(\n          current_step\n        )\n\n        if current_step_id in visited:\n          continue\n\n        visited.add(\n          current_step_id\n        )\n\n        if current_step is root_step:\n          frontier_step_ids.add(\n            id(\n              source_step\n            )\n          )\n          break\n\n        for child_step in children_by_step_id.get(\n          current_step_id,\n          (),\n        ):\n          if child_step is root_step:\n            frontier_step_ids.add(\n              id(\n                source_step\n              )\n            )\n            queue.clear()\n            break\n\n          child_reference = (\n            extract_toda_group_proof_step_literature_reference(\n              child_step\n            )\n          )\n\n          if (\n            child_reference is not None\n            and child_reference != entry.reference\n            and child_reference != root_reference\n          ):\n            continue\n\n          queue.append(\n            child_step\n          )\n\n  return frozenset(\n    frontier_step_ids\n  )\n'
ROOT_INTERNAL_HELPER = 'def _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n) -> frozenset[int]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  root_step = presentation.root_step\n  root_boundary = (\n    classify_toda_literature_statement_step(\n      root_step\n    )\n  )\n\n  if (\n    root_boundary is None\n    or root_boundary.classification\n    is not TodaLiteratureStatementClassification.PROOF_INTERNAL\n    or root_boundary.reference_locator is None\n  ):\n    return frozenset()\n\n  boundary_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    for boundary in (\n      classify_toda_literature_statement_step(\n        node.proof_step\n      ),\n    )\n    if (\n      boundary is not None\n      and boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n      and boundary.reference_locator\n      == root_boundary.reference_locator\n    )\n  )\n\n  if not boundary_steps:\n    return frozenset()\n\n  consumers_by_step_id = {}\n\n  for edge in presentation.edges:\n    consumers_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  root_ancestor_ids = {\n    id(\n      root_step\n    )\n  }\n  changed = True\n\n  while changed:\n    changed = False\n\n    for edge in presentation.edges:\n      if id(\n        edge.parent_step\n      ) not in root_ancestor_ids:\n        continue\n\n      premise_step_id = id(\n        edge.premise_step\n      )\n\n      if premise_step_id in root_ancestor_ids:\n        continue\n\n      root_ancestor_ids.add(\n        premise_step_id\n      )\n      changed = True\n\n  active_boundary_steps = tuple(\n    proof_step\n    for proof_step in boundary_steps\n    if id(\n      proof_step\n    ) in root_ancestor_ids\n  )\n\n  if not active_boundary_steps:\n    return frozenset()\n\n  closure_step_ids = {\n    id(\n      proof_step\n    )\n    for proof_step in active_boundary_steps\n  }\n  internal_step_ids = set()\n\n  changed = True\n\n  while changed:\n    changed = False\n\n    for edge in presentation.edges:\n      if id(\n        edge.parent_step\n      ) not in closure_step_ids:\n        continue\n\n      premise_step = edge.premise_step\n      premise_step_id = id(\n        premise_step\n      )\n\n      if (\n        premise_step is root_step\n        or premise_step_id in closure_step_ids\n      ):\n        continue\n\n      consumers = tuple(\n        consumers_by_step_id.get(\n          premise_step_id,\n          (),\n        )\n      )\n\n      if not consumers:\n        continue\n\n      if not all(\n        id(\n          consumer\n        )\n        in closure_step_ids\n        for consumer in consumers\n      ):\n        continue\n\n      closure_step_ids.add(\n        premise_step_id\n      )\n      internal_step_ids.add(\n        premise_step_id\n      )\n      changed = True\n\n  return frozenset(\n    internal_step_ids\n  )\n'
INTERNAL_FUNCTION = 'def _toda_group_proof_narrative_reference_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  selected_step_ids = set()\n\n  for entry in reference_entries:\n    candidate_steps = []\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          proof_step,\n          rendered_statement,\n        )\n      ):\n        continue\n\n      if rendered_statement in seen_rendered_statements:\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n\n    selected_step_ids.update(\n      id(\n        proof_step\n      )\n      for proof_step in selected_steps\n    )\n\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  root_fixed_internal_step_ids = (\n    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n      presentation\n    )\n  )\n\n  return frozenset(\n    (\n      {\n        step_id\n        for step_id in owned_step_ids\n        if step_id not in selected_step_ids\n      }\n      | set(\n        root_fixed_internal_step_ids\n      )\n    )\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n  _toda_group_proof_narrative_root_fixed_statement_internal_step_ids,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_r4_data(\n  n: int,\n  k: int,\n  depth: int,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return (\n    raw,\n    presentation,\n    entries,\n  )\n\n\ndef test_phase161_r4_r4_pi4_2_root_fixed_internality_hides_prop44_only():\n  (\n    raw,\n    presentation,\n    entries,\n  ) = _phase161_r4_r4_data(\n    2,\n    2,\n    2,\n  )\n\n  internal_step_ids = (\n    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n      presentation\n    )\n  )\n\n  prop44 = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 n=2 specialization"\n    )\n  )\n  restriction = next(\n    node.proof_step\n    for node in presentation.nodes\n    if (\n      node.proof_step.inference_rule\n      is not None\n      and node.proof_step.inference_rule.name\n      == "Toda Proposition 4.4 eta_2 second-summand restriction"\n    )\n  )\n\n  assert id(\n    prop44\n  ) in internal_step_ids\n  assert id(\n    restriction\n  ) in internal_step_ids\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert "Proposition 4.4" not in reference\n  assert (\n    r"\\pi_{i - 1}^{1} \\oplus "\n    r"\\pi_{i}^{3} \\to "\n    r"\\pi_{i}^{2}"\n    not in body\n  )\n  assert "分解写像の第二成分" not in body\n  assert "[R1]" in body\n  assert "$i=4$" in body\n  assert (\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}"\n    in body\n  )\n\n\ndef test_phase161_r4_r4_restores_pi6_3_global_frontier_contract():\n  (\n    _,\n    presentation,\n    entries,\n  ) = _phase161_r4_r4_data(\n    3,\n    3,\n    2,\n  )\n\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  frontier_locators = {\n    entry.reference.locator\n    for entry in entries\n    if any(\n      id(\n        proof_step\n      )\n      in frontier_step_ids\n      for proof_step in entry.proof_steps\n    )\n  }\n\n  assert "(5.3)" in frontier_locators\n  assert "Proposition 5.3" in frontier_locators\n  assert "Lemma 5.4" in frontier_locators\n  assert "(5.2)" in frontier_locators\n  assert "Proposition 5.1" not in frontier_locators\n\n  assert (\n    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(\n      presentation\n    )\n    == frozenset()\n  )\n'

EARLY_FRONTIER_BLOCK = """  phase161_r4_frontier_step_ids = (
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


def _functions(
  source: str,
):
  tree = ast.parse(
    source
  )

  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing function: {function_name}"
    )

  node = functions[
    function_name
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
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing insertion anchor: {function_name}"
    )

  node = functions[
    function_name
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


def _remove_function_if_present(
  source: str,
  function_name: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    return source

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )

  start = node.lineno - 1
  end = node.end_lineno

  while (
    end < len(
      lines
    )
    and not lines[
      end
    ].strip()
  ):
    end += 1

  return "".join(
    lines[
      :start
    ]
    + lines[
      end:
    ]
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing output function: {function_name}"
    )

  node = functions[
    function_name
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

  required = (
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    "_toda_group_proof_narrative_reference_internal_step_ids",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    "specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application",
  )

  functions = _functions(
    source
  )

  for function_name in required:
    if function_name not in functions:
      raise RuntimeError(
        f"Required current R4 function missing: {function_name}"
      )

  updated = _replace_function(
    source,
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    FRONTIER_FUNCTION,
  )

  updated = _remove_function_if_present(
    updated,
    "_toda_group_proof_narrative_fixed_frontier_internal_step_ids",
  )

  if (
    "_toda_group_proof_narrative_root_fixed_statement_internal_step_ids"
    not in _functions(
      updated
    )
  ):
    updated = _insert_before_function(
      updated,
      "_toda_group_proof_narrative_reference_internal_step_ids",
      ROOT_INTERNAL_HELPER,
    )

  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_reference_internal_step_ids",
    INTERNAL_FUNCTION,
  )

  count = updated.count(
    EARLY_FRONTIER_BLOCK
  )

  if count > 1:
    raise RuntimeError(
      "Multiple early R4 frontier blocks found."
    )

  if count == 1:
    updated = updated.replace(
      EARLY_FRONTIER_BLOCK,
      "",
      1,
    )

  updated = _remove_function_if_present(
    updated,
    "_filter_toda_group_proof_narrative_reference_entries_to_frontier",
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
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    "_toda_group_proof_narrative_root_fixed_statement_internal_step_ids",
    "_toda_group_proof_narrative_reference_internal_step_ids",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
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
    / "test_phase161_r4_r4_restore_global_frontier.py.txt"
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
    "Restored global frontier contract and localized pi_4^2 internality."
  )
  print(
    "Full changed/new functions and test written to output/."
  )


if __name__ == "__main__":
  main()
