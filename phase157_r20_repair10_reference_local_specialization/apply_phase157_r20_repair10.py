from __future__ import annotations

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair10_reference_local_specialization.py"
)

HELPERS = 'def _phase157_r20_reference_scalar_value(\n  value,\n  symbol,\n  binding: int,\n):\n  if isinstance(\n    value,\n    int,\n  ):\n    return value\n\n  if isinstance(\n    value,\n    ScalarSymbol,\n  ):\n    if value == symbol:\n      return binding\n\n    return None\n\n  if isinstance(\n    value,\n    ScalarSum,\n  ):\n    left = (\n      _phase157_r20_reference_scalar_value(\n        value.left,\n        symbol,\n        binding,\n      )\n    )\n    right = (\n      _phase157_r20_reference_scalar_value(\n        value.right,\n        symbol,\n        binding,\n      )\n    )\n\n    if (\n      left is None\n      or right is None\n    ):\n      return None\n\n    return left + right\n\n  return None\n\n\ndef _phase157_r20_specialize_reference_value(\n  value,\n  symbol,\n  binding: int,\n):\n  if isinstance(\n    value,\n    ScalarSymbol,\n  ):\n    if value == symbol:\n      return binding\n\n    return value\n\n  if isinstance(\n    value,\n    ScalarSum,\n  ):\n    left = (\n      _phase157_r20_specialize_reference_value(\n        value.left,\n        symbol,\n        binding,\n      )\n    )\n    right = (\n      _phase157_r20_specialize_reference_value(\n        value.right,\n        symbol,\n        binding,\n      )\n    )\n\n    if (\n      isinstance(\n        left,\n        int,\n      )\n      and isinstance(\n        right,\n        int,\n      )\n    ):\n      return left + right\n\n    return replace(\n      value,\n      left=left,\n      right=right,\n    )\n\n  if isinstance(\n    value,\n    tuple,\n  ):\n    return tuple(\n      _phase157_r20_specialize_reference_value(\n        item,\n        symbol,\n        binding,\n      )\n      for item in value\n    )\n\n  if isinstance(\n    value,\n    list,\n  ):\n    return [\n      _phase157_r20_specialize_reference_value(\n        item,\n        symbol,\n        binding,\n      )\n      for item in value\n    ]\n\n  if isinstance(\n    value,\n    dict,\n  ):\n    return {\n      key: (\n        _phase157_r20_specialize_reference_value(\n          item,\n          symbol,\n          binding,\n        )\n      )\n      for key, item in value.items()\n    }\n\n  if not is_dataclass(\n    value\n  ):\n    return value\n\n  changes = {}\n\n  for field in fields(\n    value\n  ):\n    if not field.init:\n      continue\n\n    original = getattr(\n      value,\n      field.name,\n    )\n    specialized = (\n      _phase157_r20_specialize_reference_value(\n        original,\n        symbol,\n        binding,\n      )\n    )\n\n    if specialized != original:\n      changes[\n        field.name\n      ] = specialized\n\n  if not changes:\n    return value\n\n  return replace(\n    value,\n    **changes,\n  )\n\n\ndef _phase157_r20_nested_primary_groups(\n  value,\n) -> tuple[\n  TodaPrimaryGroup,\n  ...,\n]:\n  groups = []\n\n  def walk(\n    current,\n  ):\n    if isinstance(\n      current,\n      TodaPrimaryGroup,\n    ):\n      groups.append(\n        current\n      )\n      return\n\n    if isinstance(\n      current,\n      tuple,\n    ):\n      for item in current:\n        walk(\n          item\n        )\n      return\n\n    if isinstance(\n      current,\n      list,\n    ):\n      for item in current:\n        walk(\n          item\n        )\n      return\n\n    if isinstance(\n      current,\n      dict,\n    ):\n      for item in current.values():\n        walk(\n          item\n        )\n      return\n\n    if not is_dataclass(\n      current\n    ):\n      return\n\n    for field in fields(\n      current\n    ):\n      walk(\n        getattr(\n          current,\n          field.name,\n        )\n      )\n\n  walk(\n    value\n  )\n\n  unique = []\n\n  for group in groups:\n    if group not in unique:\n      unique.append(\n        group\n      )\n\n  return tuple(\n    unique\n  )\n\n\ndef _phase157_r20_reference_descendants(\n  presentation: TodaGroupProofPresentation,\n  proof_step: ProofStep,\n) -> tuple[\n  ProofStep,\n  ...,\n]:\n  consumers_by_step_id = {}\n\n  for edge in presentation.edges:\n    consumers_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  frontier = list(\n    consumers_by_step_id.get(\n      id(\n        proof_step\n      ),\n      (),\n    )\n  )\n  seen = {\n    id(\n      proof_step\n    )\n  }\n  descendants = []\n\n  while frontier:\n    current = frontier.pop(\n      0\n    )\n    current_id = id(\n      current\n    )\n\n    if current_id in seen:\n      continue\n\n    seen.add(\n      current_id\n    )\n    descendants.append(\n      current\n    )\n    frontier.extend(\n      consumers_by_step_id.get(\n        current_id,\n        (),\n      )\n    )\n\n  return tuple(\n    descendants\n  )\n\n\ndef _phase157_r20_reference_range_allows(\n  aggregate_statement,\n  symbol,\n  binding: int,\n) -> bool:\n  if not is_dataclass(\n    aggregate_statement\n  ):\n    return True\n\n  matching_ranges = tuple(\n    value\n    for field in fields(\n      aggregate_statement\n    )\n    for value in (\n      getattr(\n        aggregate_statement,\n        field.name,\n      ),\n    )\n    if (\n      isinstance(\n        value,\n        ScalarGreaterEqualStatement,\n      )\n      and value.left == symbol\n      and isinstance(\n        value.right,\n        int,\n      )\n    )\n  )\n\n  return all(\n    binding\n    >= range_statement.right\n    for range_statement\n    in matching_ranges\n  )\n\n\ndef _phase157_r20_specialize_reference_relation(\n  presentation: TodaGroupProofPresentation,\n  proof_step: ProofStep,\n  relation: Relation,\n):\n  group = relation.lhs\n\n  if not isinstance(\n    group,\n    TodaPrimaryGroup,\n  ):\n    return None\n\n  symbol = (\n    group.sphere_dimension\n  )\n\n  if not isinstance(\n    symbol,\n    ScalarSymbol,\n  ):\n    return None\n\n  descendants = (\n    _phase157_r20_reference_descendants(\n      presentation,\n      proof_step,\n    )\n  )\n\n  concrete_groups = []\n\n  for descendant in descendants:\n    concrete_groups.extend(\n      _phase157_r20_nested_primary_groups(\n        descendant.conclusion\n      )\n    )\n\n  specializations = []\n\n  for concrete_group in concrete_groups:\n    if (\n      not isinstance(\n        concrete_group.group_dimension,\n        int,\n      )\n      or not isinstance(\n        concrete_group.sphere_dimension,\n        int,\n      )\n    ):\n      continue\n\n    binding = (\n      concrete_group.sphere_dimension\n    )\n\n    expected_sphere = (\n      _phase157_r20_reference_scalar_value(\n        group.sphere_dimension,\n        symbol,\n        binding,\n      )\n    )\n    expected_dimension = (\n      _phase157_r20_reference_scalar_value(\n        group.group_dimension,\n        symbol,\n        binding,\n      )\n    )\n\n    if (\n      expected_sphere\n      != concrete_group.sphere_dimension\n      or expected_dimension\n      != concrete_group.group_dimension\n    ):\n      continue\n\n    if not (\n      _phase157_r20_reference_range_allows(\n        proof_step.conclusion,\n        symbol,\n        binding,\n      )\n    ):\n      continue\n\n    specialized = (\n      _phase157_r20_specialize_reference_value(\n        relation,\n        symbol,\n        binding,\n      )\n    )\n\n    if specialized not in specializations:\n      specializations.append(\n        specialized\n      )\n\n  if len(\n    specializations\n  ) != 1:\n    return None\n\n  return specializations[\n    0\n  ]\n\n\ndef _phase157_r20_canonical_fixed_reference_line(\n  proof_step: ProofStep,\n  rendered_statement: str,\n) -> str:\n  boundary = (\n    classify_toda_literature_statement_step(\n      proof_step\n    )\n  )\n\n  if (\n    boundary is not None\n    and boundary.component_key\n    == "hopf_right_composition_formula"\n  ):\n    return (\n      r"$H(\\alpha\\circ E\\beta)"\n      r" = H(\\alpha)\\circ E\\beta$."\n    )\n\n  return rendered_statement\n'
AGGREGATE_FUNCTION = 'def _phase153_r6_reference_aggregate_component(\n  presentation: TodaGroupProofPresentation,\n  entry,\n  proof_step: ProofStep,\n):\n  statement = proof_step.conclusion\n\n  if not is_dataclass(\n    statement\n  ):\n    return None\n\n  relation_components = tuple(\n    value\n    for field in fields(\n      statement\n    )\n    for value in (\n      getattr(\n        statement,\n        field.name,\n      ),\n    )\n    if (\n      isinstance(\n        value,\n        Relation,\n      )\n      and _phase153_r6_group_relation_generators(\n        value\n      )\n    )\n  )\n\n  if not relation_components:\n    return None\n\n  external_consumers = tuple(\n    edge.parent_step\n    for edge in presentation.edges\n    if (\n      edge.premise_step\n      is proof_step\n      and extract_toda_group_proof_step_literature_reference(\n        edge.parent_step\n      )\n      != entry.reference\n    )\n  )\n\n  direct_matches = []\n\n  for component in relation_components:\n    generators = (\n      _phase153_r6_group_relation_generators(\n        component\n      )\n    )\n\n    if any(\n      _phase153_r6_nested_value_contains(\n        consumer.conclusion,\n        generator,\n      )\n      for consumer in external_consumers\n      for generator in generators\n    ):\n      direct_matches.append(\n        component\n      )\n\n  if len(\n    direct_matches\n  ) == 1:\n    return direct_matches[\n      0\n    ]\n\n  specialized_matches = []\n\n  for component in relation_components:\n    specialized = (\n      _phase157_r20_specialize_reference_relation(\n        presentation,\n        proof_step,\n        component,\n      )\n    )\n\n    if (\n      specialized is not None\n      and specialized\n      not in specialized_matches\n    ):\n      specialized_matches.append(\n        specialized\n      )\n\n  if len(\n    specialized_matches\n  ) != 1:\n    return None\n\n  return specialized_matches[\n    0\n  ]\n'
STATEMENT_LINES_FUNCTION = 'def _toda_group_proof_narrative_reference_statement_lines_by_number(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> dict[\n  int,\n  tuple[\n    str,\n    ...,\n  ],\n]:\n  statement_lines_by_reference_number = {}\n\n  for entry in reference_entries:\n    candidate_steps = []\n    rendered_by_step_id = {}\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n      rendered_statement = (\n        _phase157_r20_canonical_fixed_reference_line(\n          proof_step,\n          rendered_statement,\n        )\n      )\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          proof_step,\n          rendered_statement,\n        )\n      ):\n        continue\n\n      if (\n        rendered_statement\n        in seen_rendered_statements\n      ):\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n      rendered_by_step_id[\n        id(\n          proof_step\n        )\n      ] = rendered_statement\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n\n    aggregate_specializations = tuple(\n      (\n        proof_step,\n        _phase153_r6_reference_aggregate_component(\n          presentation,\n          entry,\n          proof_step,\n        ),\n      )\n      for proof_step in selected_steps\n      if is_dataclass(\n        proof_step.conclusion\n      )\n    )\n    aggregate_specializations = tuple(\n      pair\n      for pair in aggregate_specializations\n      if pair[\n        1\n      ] is not None\n    )\n\n    if len(\n      aggregate_specializations\n    ) == 1:\n      selected_steps = (\n        aggregate_specializations[\n          0\n        ][\n          0\n        ],\n      )\n\n    rendered_selected_by_step_id = {\n      id(\n        proof_step\n      ): (\n        _phase157_r20_canonical_fixed_reference_line(\n          proof_step,\n          _phase153_r6_render_reference_statement(\n            presentation,\n            entry,\n            proof_step,\n            rendered_by_step_id[\n              id(\n                proof_step\n              )\n            ],\n          ),\n        )\n      )\n      for proof_step in selected_steps\n    }\n\n    statement_lines = (\n      _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(\n        selected_steps,\n        rendered_selected_by_step_id,\n      )\n    )\n\n    if statement_lines:\n      statement_lines_by_reference_number[\n        entry.number\n      ] = statement_lines\n\n  return statement_lines_by_reference_number\n'
MAP_DEPENDENCIES_FUNCTION = 'def insert_toda_group_proof_narrative_map_property_dependencies(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def reference_entry_for_step(\n    proof_step: ProofStep,\n  ):\n    direct = tuple(\n      entry\n      for entry in reference_entries\n      if any(\n        candidate is proof_step\n        for candidate in entry.proof_steps\n      )\n    )\n\n    if len(\n      direct\n    ) == 1:\n      return direct[\n        0\n      ]\n\n    reference = (\n      extract_toda_group_proof_step_literature_reference(\n        proof_step\n      )\n    )\n\n    if (\n      reference is None\n      or reference.locator is None\n    ):\n      return None\n\n    by_locator = tuple(\n      entry\n      for entry in reference_entries\n      if (\n        entry.reference.locator\n        == reference.locator\n      )\n    )\n\n    if len(\n      by_locator\n    ) != 1:\n      return None\n\n    return by_locator[\n      0\n    ]\n\n  def reference_number_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    entry = reference_entry_for_step(\n      proof_step\n    )\n\n    if entry is None:\n      return None\n\n    return entry.number\n\n  def display_line(\n    proof_step: ProofStep,\n  ) -> str | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    entry = reference_entry_for_step(\n      proof_step\n    )\n\n    if entry is not None:\n      rendered = (\n        _phase153_r6_render_reference_statement(\n          presentation,\n          entry,\n          proof_step,\n          rendered,\n        )\n      )\n      rendered = (\n        _phase157_r20_canonical_fixed_reference_line(\n          proof_step,\n          rendered,\n        )\n      )\n\n    reference_number = (\n      reference_number_for_step(\n        proof_step\n      )\n    )\n\n    if reference_number is None:\n      return rendered\n\n    return (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]より, "\n      + rendered\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = display_line(\n      proof_step\n    )\n\n    if not rendered:\n      return None\n\n    target_key = match_key(\n      rendered\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  relevant_roles = {\n    TodaProofDependencyRole.EHP_EXACTNESS,\n    TodaProofDependencyRole.EHP_WINDOW,\n    TodaProofDependencyRole.GROUP_STRUCTURE,\n    TodaProofDependencyRole.MAP_PROPERTY,\n    TodaProofDependencyRole.RELATION,\n  }\n\n  visiting = set()\n\n  def ensure_before(\n    proof_step: ProofStep,\n    anchor_index: int,\n  ) -> int:\n    proof_step_id = id(\n      proof_step\n    )\n\n    if proof_step_id in visiting:\n      return anchor_index\n\n    visiting.add(\n      proof_step_id\n    )\n\n    boundary = (\n      classify_toda_literature_statement_step(\n        proof_step\n      )\n    )\n    is_fixed_boundary = (\n      boundary is not None\n      and boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n    )\n\n    if not is_fixed_boundary:\n      for premise in proof_step.premises:\n        premise_role = (\n          classify_toda_proof_step_role(\n            premise\n          )\n        )\n\n        if premise_role not in relevant_roles:\n          continue\n\n        anchor_index = ensure_before(\n          premise,\n          anchor_index,\n        )\n\n    line = display_line(\n      proof_step\n    )\n\n    if line is None:\n      visiting.remove(\n        proof_step_id\n      )\n      return anchor_index\n\n    current_index = (\n      paragraph_index_for_step(\n        proof_step\n      )\n    )\n\n    if current_index is not None:\n      if current_index < anchor_index:\n        visiting.remove(\n          proof_step_id\n        )\n        return anchor_index\n\n      paragraph = paragraphs.pop(\n        current_index\n      )\n      paragraphs.insert(\n        anchor_index,\n        paragraph,\n      )\n\n      visiting.remove(\n        proof_step_id\n      )\n      return anchor_index + 1\n\n    paragraphs.insert(\n      anchor_index,\n      line,\n    )\n\n    visiting.remove(\n      proof_step_id\n    )\n    return anchor_index + 1\n\n  visible_map_steps = []\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n\n    if (\n      classify_toda_proof_step_role(\n        proof_step\n      )\n      is not TodaProofDependencyRole.MAP_PROPERTY\n    ):\n      continue\n\n    if (\n      paragraph_index_for_step(\n        proof_step\n      )\n      is None\n    ):\n      continue\n\n    visible_map_steps.append(\n      proof_step\n    )\n\n  for map_step in visible_map_steps:\n    map_index = paragraph_index_for_step(\n      map_step\n    )\n\n    if map_index is None:\n      continue\n\n    for premise in map_step.premises:\n      role = classify_toda_proof_step_role(\n        premise\n      )\n\n      if role not in relevant_roles:\n        continue\n\n      map_index = ensure_before(\n        premise,\n        map_index,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair10() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair10_public_references_are_dependency_specialized():\n  rendered = _render_pi6_3_repair10()\n\n  headers = (\n    "**[R1] Proposition 5.6.**",\n    "**[R2] (5.3).**",\n    "**[R3] Proposition 5.3.**",\n    "**[R4] Proposition 5.1.**",\n    "**[R5] Proposition 2.2.**",\n  )\n\n  for header in headers:\n    assert header in rendered\n\n  reference = rendered.split(\n    "---",\n    1,\n  )[0]\n\n  r3 = reference.split(\n    "**[R3] Proposition 5.3.**",\n    1,\n  )[1].split(\n    "**[R4]",\n    1,\n  )[0]\n\n  assert (\n    r"\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}"\n    in r3\n  )\n  assert r"\\pi_{5}^{3}" not in r3\n  assert r"\\pi_{4}^{2}" not in r3\n\n  r4 = reference.split(\n    "**[R4] Proposition 5.1.**",\n    1,\n  )[1].split(\n    "**[R5]",\n    1,\n  )[0]\n\n  assert (\n    r"\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}"\n    in r4\n  )\n  assert r"\\pi_{3}^{2}" not in r4\n\n  r5 = reference.split(\n    "**[R5] Proposition 2.2.**",\n    1,\n  )[1]\n\n  assert (\n    r"H(\\alpha\\circ E\\beta)"\n    in r5\n  )\n  assert "lpha" not in r5\n\n\ndef test_phase157_r20_repair10_body_uses_same_reference_specializations():\n  rendered = _render_pi6_3_repair10()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert "[R3]より" in body\n  assert "[R4]より" in body\n  assert "[R5]より" in body\n\n  assert (\n    r"\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}"\n    in body\n  )\n  assert (\n    r"\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}"\n    in body\n  )\n'


def function_range(
  source: str,
  name: str,
):
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def insert_before_function(
  source: str,
  before_name: str,
  addition: str,
) -> str:
  start, _end = function_range(
    source,
    before_name,
  )

  return (
    source[:start]
    + addition.rstrip()
    + "\n\n\n"
    + source[start:]
  )


def add_import_block(
  source: str,
  block: str,
) -> str:
  if block in source:
    return source

  marker = "from proof import ("

  index = source.find(
    marker
  )

  if index < 0:
    raise RuntimeError(
      "proof import block not found"
    )

  return (
    source[:index]
    + block
    + "\n"
    + source[index:]
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair10_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  source = add_import_block(
    source,
    """from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
""",
  )

  if (
    "def _phase157_r20_reference_scalar_value("
    not in source
  ):
    source = insert_before_function(
      source,
      "_phase153_r6_reference_aggregate_component",
      HELPERS,
    )

  source = replace_function(
    source,
    "_phase153_r6_reference_aggregate_component",
    AGGREGATE_FUNCTION,
  )
  source = replace_function(
    source,
    "_toda_group_proof_narrative_reference_statement_lines_by_number",
    STATEMENT_LINES_FUNCTION,
  )
  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_map_property_dependencies",
    MAP_DEPENDENCIES_FUNCTION,
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair10 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed:",
    TARGET,
  )
  print(
    "Added test:",
    TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
