from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = (
    REPO_ROOT
    / "tests"
    / "test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py"
)
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


IMPORT_OLD = '''from homotopy_groups import (
  TodaPrimaryGroup,
)
'''

IMPORT_NEW = '''from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
'''


INSERT_MARKER = '''def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
'''


HELPERS = 'def _phase159_r1_7c_r3_specialize_primary_group(\n  group: TodaPrimaryGroup,\n  symbol,\n  binding: int,\n) -> TodaPrimaryGroup | None:\n  group_dimension = (\n    _phase157_r20_reference_scalar_value(\n      group.group_dimension,\n      symbol,\n      binding,\n    )\n  )\n  sphere_dimension = (\n    _phase157_r20_reference_scalar_value(\n      group.sphere_dimension,\n      symbol,\n      binding,\n    )\n  )\n\n  if (\n    group_dimension is None\n    or sphere_dimension is None\n  ):\n    return None\n\n  return TodaPrimaryGroup(\n    group_dimension=group_dimension,\n    sphere_dimension=sphere_dimension,\n  )\n\n\ndef _phase159_r1_7c_r3_aggregate_zero_specializes_to(\n  statement,\n  target_group: TodaPrimaryGroup,\n) -> bool:\n  if not isinstance(\n    target_group,\n    TodaPrimaryGroup,\n  ):\n    raise TypeError(\n      "target_group must be a TodaPrimaryGroup"\n    )\n\n  if not is_dataclass(\n    statement\n  ):\n    return False\n\n  target_sphere_dimension = (\n    target_group.sphere_dimension\n  )\n\n  if (\n    not isinstance(\n      target_sphere_dimension,\n      int,\n    )\n    or isinstance(\n      target_sphere_dimension,\n      bool,\n    )\n  ):\n    return False\n\n  statement_values = tuple(\n    getattr(\n      statement,\n      field.name,\n    )\n    for field in fields(\n      statement\n    )\n  )\n  range_statements = tuple(\n    value\n    for value in statement_values\n    if isinstance(\n      value,\n      ScalarGreaterEqualStatement,\n    )\n  )\n\n  for value in statement_values:\n    if not isinstance(\n      value,\n      TodaPrimaryGroupZeroStatement,\n    ):\n      continue\n\n    template_group = value.group\n    symbol = (\n      template_group.sphere_dimension\n    )\n\n    if not isinstance(\n      symbol,\n      ScalarSymbol,\n    ):\n      continue\n\n    specialized_group = (\n      _phase159_r1_7c_r3_specialize_primary_group(\n        template_group,\n        symbol,\n        target_sphere_dimension,\n      )\n    )\n\n    if specialized_group != target_group:\n      continue\n\n    applicable_range_found = False\n\n    for range_statement in range_statements:\n      left = (\n        _phase157_r20_reference_scalar_value(\n          range_statement.left,\n          symbol,\n          target_sphere_dimension,\n        )\n      )\n      right = (\n        _phase157_r20_reference_scalar_value(\n          range_statement.right,\n          symbol,\n          target_sphere_dimension,\n        )\n      )\n\n      if (\n        left is not None\n        and right is not None\n        and left >= right\n      ):\n        applicable_range_found = True\n        break\n\n    if applicable_range_found:\n      return True\n\n  return False\n\n\ndef _phase159_r1_7c_r3_decomposition_specialization(\n  statement,\n  target_group: TodaPrimaryGroup,\n):\n  prop44_statement = getattr(\n    statement,\n    "prop44_isomorphism",\n    None,\n  )\n\n  if prop44_statement is not None:\n    decomposition_map = getattr(\n      prop44_statement,\n      "map",\n      None,\n    )\n  else:\n    decomposition_map = getattr(\n      statement,\n      "map",\n      None,\n    )\n\n  if decomposition_map is None:\n    return None\n\n  source_group = getattr(\n    decomposition_map,\n    "source_group",\n    None,\n  )\n  map_target_group = getattr(\n    decomposition_map,\n    "target_group",\n    None,\n  )\n  summands = getattr(\n    source_group,\n    "summands",\n    None,\n  )\n\n  if (\n    not isinstance(\n      map_target_group,\n      TodaPrimaryGroup,\n    )\n    or not isinstance(\n      summands,\n      tuple,\n    )\n    or len(\n      summands\n    ) != 2\n    or not all(\n      isinstance(\n        summand,\n        TodaPrimaryGroup,\n      )\n      for summand in summands\n    )\n  ):\n    return None\n\n  target_dimension = (\n    target_group.group_dimension\n  )\n\n  if (\n    not isinstance(\n      target_dimension,\n      int,\n    )\n    or isinstance(\n      target_dimension,\n      bool,\n    )\n  ):\n    return None\n\n  map_dimension = (\n    map_target_group.group_dimension\n  )\n\n  if isinstance(\n    map_dimension,\n    ScalarSymbol,\n  ):\n    symbol = map_dimension\n    binding = target_dimension\n  elif isinstance(\n    map_dimension,\n    int,\n  ) and not isinstance(\n    map_dimension,\n    bool,\n  ):\n    if map_target_group != target_group:\n      return None\n\n    symbol = ScalarSymbol(\n      name="_phase159_r1_7c_r3_unused",\n    )\n    binding = target_dimension\n  else:\n    return None\n\n  specialized_target = (\n    _phase159_r1_7c_r3_specialize_primary_group(\n      map_target_group,\n      symbol,\n      binding,\n    )\n  )\n\n  if specialized_target != target_group:\n    return None\n\n  specialized_summands = tuple(\n    _phase159_r1_7c_r3_specialize_primary_group(\n      summand,\n      symbol,\n      binding,\n    )\n    for summand in summands\n  )\n\n  if any(\n    summand is None\n    for summand in specialized_summands\n  ):\n    return None\n\n  return (\n    specialized_summands,\n    target_group,\n  )\n\n\ndef _phase159_r1_7c_r3_root_zero_direct_premise_plan(\n  presentation: TodaGroupProofPresentation,\n):\n  root_step = presentation.root_step\n\n  if not isinstance(\n    root_step.conclusion,\n    TodaPrimaryGroupZeroStatement,\n  ):\n    return None\n\n  target_group = (\n    root_step.conclusion.group\n  )\n  decomposition_matches = tuple(\n    (\n      premise_step,\n      specialization,\n    )\n    for premise_step in root_step.premises\n    for specialization in (\n      _phase159_r1_7c_r3_decomposition_specialization(\n        premise_step.conclusion,\n        target_group,\n      ),\n    )\n    if specialization is not None\n  )\n\n  if len(\n    decomposition_matches\n  ) != 1:\n    return None\n\n  (\n    decomposition_step,\n    decomposition_specialization,\n  ) = decomposition_matches[0]\n  (\n    specialized_summands,\n    specialized_target,\n  ) = decomposition_specialization\n  support_records = []\n\n  for summand in specialized_summands:\n    direct_zero_matches = tuple(\n      premise_step\n      for premise_step in root_step.premises\n      if (\n        isinstance(\n          premise_step.conclusion,\n          TodaPrimaryGroupZeroStatement,\n        )\n        and premise_step.conclusion.group\n        == summand\n      )\n    )\n\n    if len(\n      direct_zero_matches\n    ) == 1:\n      support_records.append(\n        (\n          summand,\n          direct_zero_matches[0],\n          "known_zero",\n        )\n      )\n      continue\n\n    aggregate_matches = tuple(\n      premise_step\n      for premise_step in root_step.premises\n      if (\n        premise_step is not decomposition_step\n        and _phase159_r1_7c_r3_aggregate_zero_specializes_to(\n          premise_step.conclusion,\n          summand,\n        )\n      )\n    )\n\n    if len(\n      aggregate_matches\n    ) != 1:\n      return None\n\n    support_records.append(\n      (\n        summand,\n        aggregate_matches[0],\n        "aggregate_zero",\n      )\n    )\n\n  support_kinds = {\n    support_kind\n    for _, _, support_kind in support_records\n  }\n\n  if support_kinds != {\n    "known_zero",\n    "aggregate_zero",\n  }:\n    return None\n\n  return (\n    tuple(\n      support_records\n    ),\n    decomposition_step,\n    specialized_summands,\n    specialized_target,\n  )\n\n\ndef _phase159_r1_7c_r3_reference_marker(\n  paragraph: str,\n) -> str | None:\n  stripped = paragraph.lstrip()\n\n  if not stripped.startswith(\n    "[R"\n  ):\n    return None\n\n  closing_index = stripped.find(\n    "]"\n  )\n\n  if closing_index < 0:\n    return None\n\n  number = stripped[\n    2:closing_index\n  ]\n\n  if not number.isdigit():\n    return None\n\n  return stripped[\n    :closing_index + 1\n  ]\n\n\ndef _phase159_r1_7c_r3_specialized_zero_paragraph(\n  paragraph: str,\n  group: TodaPrimaryGroup,\n) -> str:\n  marker = (\n    _phase159_r1_7c_r3_reference_marker(\n      paragraph\n    )\n  )\n  statement = (\n    "$"\n    + render_toda_primary_group_latex(\n      group\n    )\n    + " = 0$."\n  )\n\n  if marker is None:\n    return statement\n\n  return (\n    marker\n    + "より, "\n    + statement\n  )\n\n\ndef _phase159_r1_7c_r3_specialized_decomposition_paragraph(\n  paragraph: str,\n  summands: tuple[\n    TodaPrimaryGroup,\n    ...,\n  ],\n  target_group: TodaPrimaryGroup,\n) -> str:\n  marker = (\n    _phase159_r1_7c_r3_reference_marker(\n      paragraph\n    )\n  )\n  source_latex = r" \\oplus ".join(\n    render_toda_primary_group_latex(\n      summand\n    )\n    for summand in summands\n  )\n  statement = (\n    "$"\n    + source_latex\n    + r" \\xrightarrow{\\cong} "\n    + render_toda_primary_group_latex(\n      target_group\n    )\n    + "$."\n  )\n\n  if marker is None:\n    return statement\n\n  return (\n    marker\n    + "より, "\n    + statement\n  )\n\n\ndef specialize_toda_group_proof_narrative_root_zero_direct_premises(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  plan = (\n    _phase159_r1_7c_r3_root_zero_direct_premise_plan(\n      presentation\n    )\n  )\n\n  if plan is None:\n    return markdown\n\n  (\n    support_records,\n    decomposition_step,\n    specialized_summands,\n    specialized_target,\n  ) = plan\n  replacement_by_rendered_step = {}\n\n  for (\n    summand,\n    support_step,\n    support_kind,\n  ) in support_records:\n    if support_kind != "aggregate_zero":\n      continue\n\n    rendered_support = (\n      _render_generic_narrative_step(\n        support_step\n      )\n    )\n\n    if rendered_support:\n      replacement_by_rendered_step[\n        rendered_support\n      ] = (\n        "zero",\n        summand,\n      )\n\n  rendered_decomposition = (\n    _render_generic_narrative_step(\n      decomposition_step\n    )\n  )\n\n  if rendered_decomposition:\n    replacement_by_rendered_step[\n      rendered_decomposition\n    ] = (\n      "decomposition",\n      (\n        specialized_summands,\n        specialized_target,\n      ),\n    )\n\n  direct_premise_ids = {\n    id(\n      premise_step\n    )\n    for premise_step in (\n      presentation.root_step.premises\n    )\n  }\n  ancestor_steps = []\n  seen_ancestor_ids = set()\n  stack = [\n    ancestor_step\n    for premise_step in (\n      presentation.root_step.premises\n    )\n    for ancestor_step in (\n      premise_step.premises\n    )\n  ]\n\n  while stack:\n    proof_step = stack.pop()\n    proof_step_id = id(\n      proof_step\n    )\n\n    if (\n      proof_step_id\n      in seen_ancestor_ids\n      or proof_step_id\n      in direct_premise_ids\n    ):\n      continue\n\n    seen_ancestor_ids.add(\n      proof_step_id\n    )\n    ancestor_steps.append(\n      proof_step\n    )\n    stack.extend(\n      proof_step.premises\n    )\n\n  ancestor_fragments = tuple(\n    rendered\n    for rendered in (\n      _render_generic_narrative_step(\n        proof_step\n      )\n      for proof_step in ancestor_steps\n    )\n    if rendered\n  )\n  root_rendered = (\n    _render_generic_narrative_step(\n      presentation.root_step\n    )\n  )\n  retained_paragraphs = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    replacement = next(\n      (\n        replacement\n        for rendered_step, replacement\n        in replacement_by_rendered_step.items()\n        if rendered_step in paragraph\n      ),\n      None,\n    )\n\n    if replacement is not None:\n      replacement_kind, value = replacement\n\n      if replacement_kind == "zero":\n        retained_paragraphs.append(\n          _phase159_r1_7c_r3_specialized_zero_paragraph(\n            paragraph,\n            value,\n          )\n        )\n      else:\n        (\n          summands,\n          target_group,\n        ) = value\n        retained_paragraphs.append(\n          _phase159_r1_7c_r3_specialized_decomposition_paragraph(\n            paragraph,\n            summands,\n            target_group,\n          )\n        )\n\n      continue\n\n    if (\n      root_rendered\n      and root_rendered in paragraph\n    ):\n      retained_paragraphs.append(\n        paragraph\n      )\n      continue\n\n    if any(\n      fragment in paragraph\n      for fragment in ancestor_fragments\n    ):\n      continue\n\n    retained_paragraphs.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained_paragraphs\n  )\n'


CALL_OLD = '''  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  generic_used_step_ids = (
'''

CALL_NEW = '''  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
  rendered = (
    specialize_toda_group_proof_narrative_root_zero_direct_premises(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
'''


def replace_once(
  source: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = source.count(old)

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> None:
  if not TARGET.exists():
    raise FileNotFoundError(
      f"repository target not found: {TARGET}"
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  already_applied = (
    "def specialize_toda_group_proof_narrative_root_zero_direct_premises("
    in source
  )

  if not already_applied:
    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )
    backup = (
      BACKUP_DIR
      / TARGET.name
    )

    if not backup.exists():
      shutil.copy2(
        TARGET,
        backup,
      )

    source = replace_once(
      source,
      IMPORT_OLD,
      IMPORT_NEW,
      "homotopy_groups import",
    )

    if INSERT_MARKER not in source:
      raise RuntimeError(
        "render function insertion marker not found"
      )

    source = source.replace(
      INSERT_MARKER,
      HELPERS
      + "\n\n"
      + INSERT_MARKER,
      1,
    )

    source = replace_once(
      source,
      CALL_OLD,
      CALL_NEW,
      "R3 public narrative hook",
    )

    TARGET.write_text(
      source,
      encoding="utf-8",
    )

  TEST_TARGET.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    PACKAGE_DIR
    / "test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py",
    TEST_TARGET,
  )

  print(
    "Phase 159 R1-7c R3 applied."
  )
  print(
    "Production file:",
    TARGET,
  )
  print(
    "Focused test:",
    TEST_TARGET,
  )
  print(
    "Already applied:",
    already_applied,
  )


if __name__ == "__main__":
  main()
