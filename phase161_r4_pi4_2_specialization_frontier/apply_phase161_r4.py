from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

REFERENCES = REPO_ROOT / "toda_group_proof_narrative_references.py"
RENDERER = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = REPO_ROOT / "tests" / "test_phase161_r4_pi4_2_specialization_frontier.py"
R3_TEST = REPO_ROOT / "tests" / "test_phase161_pi4_2_restored_reference_relink.py"

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

EXCLUDE_FUNCTION = 'def exclude_toda_group_proof_narrative_root_reference(\n  entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  root_step: ProofStep,\n) -> tuple[\n  tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n]:\n  if not isinstance(entries, tuple):\n    raise TypeError("entries must be a tuple")\n\n  if not all(\n    isinstance(\n      entry,\n      TodaGroupProofNarrativeReferenceEntry,\n    )\n    for entry in entries\n  ):\n    raise TypeError(\n      "entries must contain only "\n      "TodaGroupProofNarrativeReferenceEntry objects"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  if not isinstance(\n    root_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep"\n    )\n\n  root_reference = (\n    extract_toda_group_proof_step_literature_reference(\n      root_step\n    )\n  )\n\n  if root_reference is None:\n    return (\n      entries,\n      statement_lines_by_reference_number,\n    )\n\n  root_boundary = (\n    classify_toda_literature_statement_step(\n      root_step\n    )\n  )\n\n  retained_entries = []\n\n  for entry in entries:\n    if not _same_toda_group_proof_literature_reference(\n      entry.reference,\n      root_reference,\n    ):\n      retained_entries.append(\n        entry\n      )\n      continue\n\n    if root_boundary is None:\n      continue\n\n    if (\n      root_boundary.classification\n      is TodaLiteratureStatementClassification.PROOF_INTERNAL\n    ):\n      fixed_steps = []\n\n      for proof_step in entry.proof_steps:\n        if proof_step is root_step:\n          continue\n\n        boundary = (\n          classify_toda_literature_statement_step(\n            proof_step\n          )\n        )\n\n        if (\n          boundary is None\n          or boundary.classification\n          is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n          or boundary.reference_locator\n          != root_boundary.reference_locator\n        ):\n          continue\n\n        fixed_steps.append(\n          proof_step\n        )\n\n      if fixed_steps:\n        retained_entries.append(\n          replace(\n            entry,\n            proof_steps=tuple(\n              fixed_steps\n            ),\n          )\n        )\n\n      continue\n\n    if (\n      root_boundary.classification\n      is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n      or root_boundary.component_key is None\n    ):\n      continue\n\n    eligible_steps = []\n\n    for proof_step in entry.proof_steps:\n      boundary = (\n        classify_toda_literature_statement_step(\n          proof_step\n        )\n      )\n\n      if (\n        boundary is None\n        or boundary.classification\n        is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n        or boundary.reference_locator\n        != root_boundary.reference_locator\n        or boundary.component_key is None\n      ):\n        continue\n\n      component = get_toda_fixed_statement_component(\n        boundary.reference_locator,\n        boundary.component_key,\n      )\n\n      if not (\n        is_toda_fixed_statement_component_reference_eligible(\n          component,\n          root_boundary.reference_locator,\n          root_boundary.component_key,\n        )\n      ):\n        continue\n\n      eligible_steps.append(\n        proof_step\n      )\n\n    if eligible_steps:\n      retained_entries.append(\n        replace(\n          entry,\n          proof_steps=tuple(\n            eligible_steps\n          ),\n        )\n      )\n\n  retained_entries = tuple(\n    retained_entries\n  )\n\n  number_map = {\n    entry.number: new_number\n    for new_number, entry in enumerate(\n      retained_entries,\n      start=1,\n    )\n  }\n\n  filtered_entries = tuple(\n    replace(\n      entry,\n      number=number_map[\n        entry.number\n      ],\n    )\n    for entry in retained_entries\n  )\n\n  filtered_statement_lines = {\n    number_map[\n      entry.number\n    ]: statement_lines_by_reference_number[\n      entry.number\n    ]\n    for entry in retained_entries\n    if entry.number\n    in statement_lines_by_reference_number\n  }\n\n  return (\n    filtered_entries,\n    filtered_statement_lines,\n  )\n'
PLAN_FUNCTION = 'def _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n):\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  root_step = presentation.root_step\n\n  if not isinstance(\n    root_step.conclusion,\n    Relation,\n  ):\n    return None\n\n  target_group = (\n    root_step.conclusion.lhs\n  )\n\n  if not isinstance(\n    target_group,\n    TodaPrimaryGroup,\n  ):\n    return None\n\n  target_dimension = (\n    target_group.group_dimension\n  )\n\n  if (\n    not isinstance(\n      target_dimension,\n      int,\n    )\n    or isinstance(\n      target_dimension,\n      bool,\n    )\n  ):\n    return None\n\n  matches = []\n\n  for entry in reference_entries:\n    for proof_step in entry.proof_steps:\n      boundary = (\n        classify_toda_literature_statement_step(\n          proof_step\n        )\n      )\n\n      if (\n        boundary is None\n        or boundary.classification\n        is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n        or boundary.component_key\n        != "eta2_composition_isomorphism"\n      ):\n        continue\n\n      statement = proof_step.conclusion\n      map_object = getattr(\n        statement,\n        "map",\n        None,\n      )\n\n      if map_object is None:\n        continue\n\n      source_group = getattr(\n        map_object,\n        "source_group",\n        None,\n      )\n      map_target_group = getattr(\n        map_object,\n        "target_group",\n        None,\n      )\n\n      if (\n        not isinstance(\n          source_group,\n          TodaPrimaryGroup,\n        )\n        or not isinstance(\n          map_target_group,\n          TodaPrimaryGroup,\n        )\n      ):\n        continue\n\n      symbol = (\n        map_target_group.group_dimension\n      )\n\n      if not isinstance(\n        symbol,\n        ScalarSymbol,\n      ):\n        continue\n\n      specialized_source = (\n        _phase159_r1_7c_r3_specialize_primary_group(\n          source_group,\n          symbol,\n          target_dimension,\n        )\n      )\n      specialized_target = (\n        _phase159_r1_7c_r3_specialize_primary_group(\n          map_target_group,\n          symbol,\n          target_dimension,\n        )\n      )\n\n      if specialized_target != target_group:\n        continue\n\n      source_steps = tuple(\n        premise_step\n        for premise_step in root_step.premises\n        if (\n          isinstance(\n            premise_step.conclusion,\n            Relation,\n          )\n          and premise_step.conclusion.lhs\n          == specialized_source\n        )\n      )\n\n      if len(\n        source_steps\n      ) != 1:\n        continue\n\n      source_step = source_steps[\n        0\n      ]\n      source_structure = (\n        source_step.conclusion.rhs\n      )\n      target_structure = (\n        root_step.conclusion.rhs\n      )\n      source_generator = getattr(\n        source_structure,\n        "generator",\n        None,\n      )\n      target_generator = getattr(\n        target_structure,\n        "generator",\n        None,\n      )\n      source_order = getattr(\n        source_structure,\n        "order",\n        None,\n      )\n      target_order = getattr(\n        target_structure,\n        "order",\n        None,\n      )\n\n      if (\n        source_generator is None\n        or target_generator is None\n        or source_order != target_order\n      ):\n        continue\n\n      matches.append(\n        (\n          entry,\n          proof_step,\n          source_step,\n          specialized_source,\n          specialized_target,\n          source_generator,\n          target_generator,\n          target_dimension,\n        )\n      )\n\n  if len(\n    matches\n  ) != 1:\n    return None\n\n  return matches[\n    0\n  ]\n'
SPECIALIZE_FUNCTION = 'def specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  plan = (\n    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  if plan is None:\n    return markdown\n\n  (\n    entry,\n    fixed_step,\n    source_step,\n    specialized_source,\n    specialized_target,\n    source_generator,\n    target_generator,\n    target_dimension,\n  ) = plan\n\n  marker = (\n    "[R"\n    + str(\n      entry.number\n    )\n    + "]"\n  )\n  specialized_map_paragraph = (\n    marker\n    + "を $i="\n    + str(\n      target_dimension\n    )\n    + "$ に適用すると, "\n    + r"$\\eta_{2}\\circ -: "\n    + render_toda_primary_group_latex(\n      specialized_source\n    )\n    + r" \\to "\n    + render_toda_primary_group_latex(\n      specialized_target\n    )\n    + "$ は同型である."\n  )\n  generator_paragraph = (\n    "この同型で, $"\n    + render_toda_expression_latex(\n      source_generator\n    )\n    + r" \\mapsto "\n    + render_toda_expression_latex(\n      target_generator\n    )\n    + "$."\n  )\n\n  if specialized_map_paragraph in markdown:\n    return markdown\n\n  fixed_rendered = (\n    _render_generic_narrative_step(\n      fixed_step\n    )\n  )\n  source_rendered = (\n    _render_generic_narrative_step(\n      source_step\n    )\n  )\n  root_rendered = (\n    _render_generic_narrative_step(\n      presentation.root_step\n    )\n  )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  retained = []\n\n  for paragraph in paragraphs:\n    if (\n      fixed_rendered\n      and fixed_rendered in paragraph\n    ):\n      continue\n\n    retained.append(\n      paragraph\n    )\n\n  insertion_index = None\n\n  if source_rendered:\n    matching_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        retained\n      )\n      if source_rendered in paragraph\n    )\n\n    if len(\n      matching_indices\n    ) == 1:\n      insertion_index = (\n        matching_indices[\n          0\n        ]\n        + 1\n      )\n\n  if (\n    insertion_index is None\n    and root_rendered\n  ):\n    matching_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        retained\n      )\n      if root_rendered in paragraph\n    )\n\n    if len(\n      matching_indices\n    ) == 1:\n      insertion_index = (\n        matching_indices[\n          0\n        ]\n      )\n\n  if insertion_index is None:\n    return markdown\n\n  retained[\n    insertion_index:\n    insertion_index\n  ] = [\n    specialized_map_paragraph,\n    generator_paragraph,\n  ]\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TEST_SOURCE = 'from homotopy_groups import (\n  TodaPrimaryGroup,\n)\nfrom proof import (\n  Relation,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase161_r4_pi4_2_presentations():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  semantic = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    semantic,\n  )\n\n\ndef _phase161_r4_frontier_entries():\n  _, presentation = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  entries = (\n    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(\n      entries,\n      presentation.root_step,\n    )\n  )\n  statement_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = (\n    exclude_toda_group_proof_narrative_root_reference(\n      entries,\n      statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  return (\n    presentation,\n    entries,\n  )\n\n\ndef test_phase161_r4_pi4_2_same_locator_fixed_statement_survives_root_exclusion():\n  presentation, entries = (\n    _phase161_r4_frontier_entries()\n  )\n\n  toda52_entries = tuple(\n    entry\n    for entry in entries\n    if entry.reference.locator == "(5.2)"\n  )\n\n  assert len(\n    toda52_entries\n  ) == 1\n\n  assert all(\n    proof_step is not presentation.root_step\n    for proof_step in toda52_entries[\n      0\n    ].proof_steps\n  )\n\n\ndef test_phase161_r4_pi4_2_specialization_plan_is_semantic():\n  presentation, entries = (\n    _phase161_r4_frontier_entries()\n  )\n  plan = (\n    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(\n      presentation,\n      entries,\n    )\n  )\n\n  assert plan is not None\n\n  (\n    _,\n    _,\n    source_step,\n    specialized_source,\n    specialized_target,\n    _,\n    _,\n    target_dimension,\n  ) = plan\n\n  assert target_dimension == 4\n\n  assert specialized_source == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=3,\n  )\n  assert specialized_target == TodaPrimaryGroup(\n    group_dimension=4,\n    sphere_dimension=2,\n  )\n\n  assert isinstance(\n    source_step.conclusion,\n    Relation,\n  )\n  assert (\n    source_step.conclusion.lhs\n    == specialized_source\n  )\n\n\ndef test_phase161_r4_pi4_2_public_reference_is_general_and_body_is_specialized():\n  raw, _ = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert (\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}$"\n    in reference\n  )\n\n  assert "Proposition 4.4" not in reference\n\n  assert (\n    r"[R1]を $i=4$ に適用すると, "\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{4}^{3} \\to \\pi_{4}^{2}$ "\n    r"は同型である."\n    in body\n  )\n\n  assert (\n    r"\\eta_{3} \\mapsto "\n    in body\n  )\n\n  assert (\n    r"\\pi_{i}^{3}"\n    not in body\n  )\n  assert (\n    r"\\pi_{i}^{2}"\n    not in body\n  )\n  assert (\n    r"\\pi_{i - 1}^{1}"\n    not in body\n  )\n  assert (\n    "分解写像の第二成分"\n    not in body\n  )\n  assert (\n    "Proposition 4.4"\n    not in body\n  )\n\n\ndef test_phase161_r4_pi4_2_keeps_target_and_qed():\n  raw, _ = (\n    _phase161_r4_pi4_2_presentations()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in rendered\n  )\n  assert "□" in rendered\n'
R3_TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi4_2_phase161_r3() -> str:\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase161_r3_pi4_2_reference_keeps_toda52_after_r4_frontier_refinement():\n  rendered = _render_pi4_2_phase161_r3()\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "**[R1] (5.2).**" in reference\n  assert (\n    r"$\\eta_{2}\\circ -: "\n    r"\\pi_{i}^{3} \\to \\pi_{i}^{2}$"\n    in reference\n  )\n  assert "[R1]" in body\n\n\ndef test_phase161_r3_pi4_2_keeps_group_result_and_qed():\n  rendered = _render_pi4_2_phase161_r3()\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in rendered\n  )\n  assert "□" in rendered\n'


RENDER_FUNCTION_NAME = (
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"
)

CALL_ANCHOR = """  rendered = (
    specialize_toda_group_proof_narrative_root_zero_direct_premises(
      presentation,
      rendered,
    )
  )
"""

CALL_REPLACEMENT = CALL_ANCHOR + """
  rendered = (
    specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application(
      presentation,
      rendered,
      reference_entries,
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
  references_source = REFERENCES.read_text(
    encoding="utf-8"
  )
  renderer_source = RENDERER.read_text(
    encoding="utf-8"
  )

  if (
    "Phase 161-R3 relink is already applied"
    in renderer_source
  ):
    raise RuntimeError(
      "Unexpected package text found in production renderer."
    )

  if (
    "link_toda_group_proof_narrative_unmarked_reference_consumers("
    not in renderer_source
  ):
    raise RuntimeError(
      "R3/recovered renderer does not contain the relink helper call."
    )

  updated_references = _replace_function(
    references_source,
    "exclude_toda_group_proof_narrative_root_reference",
    EXCLUDE_FUNCTION,
  )

  if (
    "_toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan"
    not in renderer_source
  ):
    renderer_source = _insert_before_function(
      renderer_source,
      RENDER_FUNCTION_NAME,
      PLAN_FUNCTION
      + "\n\n"
      + SPECIALIZE_FUNCTION,
    )

  if (
    "specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application("
    not in _extract_function(
      renderer_source,
      RENDER_FUNCTION_NAME,
    )
  ):
    count = renderer_source.count(
      CALL_ANCHOR
    )

    if count != 1:
      raise RuntimeError(
        "Expected exactly one root-zero specialization call anchor, "
        f"found {count}."
      )

    renderer_source = renderer_source.replace(
      CALL_ANCHOR,
      CALL_REPLACEMENT,
      1,
    )

  ast.parse(
    updated_references
  )
  ast.parse(
    renderer_source
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    REFERENCES,
    BACKUP_DIR / REFERENCES.name,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )

  REFERENCES.write_text(
    updated_references,
    encoding="utf-8",
    newline="\n",
  )
  RENDERER.write_text(
    renderer_source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  R3_TEST.write_text(
    R3_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "exclude_toda_group_proof_narrative_root_reference.py.txt"
  ).write_text(
    _extract_function(
      updated_references,
      "exclude_toda_group_proof_narrative_root_reference",
    ),
    encoding="utf-8",
    newline="\n",
  )

  for function_name in (
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
        renderer_source,
        function_name,
      ),
      encoding="utf-8",
      newline="\n",
    )

  (
    OUTPUT_DIR
    / "test_phase161_r4_pi4_2_specialization_frontier.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )
  (
    OUTPUT_DIR
    / "test_phase161_pi4_2_restored_reference_relink.py.txt"
  ).write_text(
    R3_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    REFERENCES,
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
    "Updated:",
    R3_TEST,
  )
  print(
    "Full changed/new functions and test files written to output/."
  )


if __name__ == "__main__":
  main()
