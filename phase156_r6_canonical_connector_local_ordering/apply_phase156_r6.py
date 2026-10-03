from __future__ import annotations

import ast
import shutil
from pathlib import Path


GENERIC_IMPORT_OLD = 'from expression import (\n  Composition,\n  HomotopyElement,\n)\n'
GENERIC_IMPORT_NEW = 'from expression import (\n  Composition,\n  HomotopyElement,\n  Suspension,\n)\n'
GENERIC_EXPR_FUNCTION = 'def _render_generic_narrative_expression_latex(\n  expression,\n) -> str:\n  compact = _render_generic_eta_composition_latex(\n    expression\n  )\n  if compact is not None:\n    return compact\n\n  if isinstance(\n    expression,\n    Suspension,\n  ):\n    suspended = expression.expression\n\n    if isinstance(\n      suspended,\n      HomotopyElement,\n    ):\n      generator = suspended.generator\n\n      if (\n        generator is not None\n        and generator.family == "η"\n        and isinstance(\n          generator.index,\n          int,\n        )\n        and not isinstance(\n          generator.index,\n          bool,\n        )\n        and generator.decoration is None\n      ):\n        return (\n          r"\\eta_{"\n          + str(\n            generator.index + 1\n          )\n          + "}"\n        )\n\n  if isinstance(\n    expression,\n    Composition,\n  ):\n    return (\n      _render_generic_narrative_expression_latex(\n        expression.left\n      )\n      + _render_generic_narrative_expression_latex(\n        expression.right\n      )\n    )\n\n  return render_toda_expression_latex(\n    expression\n  )\n'
CONNECTOR_HELPER = 'def normalize_toda_group_proof_narrative_connectors(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  retained = []\n\n  for index, paragraph in enumerate(\n    paragraphs\n  ):\n    stripped = paragraph.strip()\n\n    if (\n      stripped == "以上より,"\n      and index + 1 < len(\n        paragraphs\n      )\n      and paragraphs[\n        index + 1\n      ].strip().startswith(\n        "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"\n      )\n    ):\n      continue\n\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
TAG_HELPER = 'def _toda_group_proof_narrative_equation_tag_number(\n  paragraph: str,\n) -> int | None:\n  marker = r"\\tag{"\n  marker_index = paragraph.find(\n    marker\n  )\n\n  if marker_index < 0:\n    return None\n\n  number_start = (\n    marker_index\n    + len(\n      marker\n    )\n  )\n  number_end = paragraph.find(\n    "}",\n    number_start,\n  )\n\n  if number_end < 0:\n    return None\n\n  number_text = paragraph[\n    number_start:\n    number_end\n  ]\n\n  if not number_text.isdigit():\n    return None\n\n  return int(\n    number_text\n  )\n'
REF_HELPER = 'def _toda_group_proof_narrative_two_equation_reference_numbers(\n  paragraph: str,\n) -> tuple[\n  int,\n  int,\n] | None:\n  stripped = paragraph.strip()\n\n  if not stripped.startswith(\n    "("\n  ):\n    return None\n\n  first_close = stripped.find(\n    ")"\n  )\n\n  if first_close <= 1:\n    return None\n\n  first_text = stripped[\n    1:\n    first_close\n  ]\n\n  separator = ") と ("\n  separator_index = stripped.find(\n    separator\n  )\n\n  if separator_index != first_close:\n    return None\n\n  second_start = (\n    separator_index\n    + len(\n      separator\n    )\n  )\n  second_close = stripped.find(\n    ")",\n    second_start,\n  )\n\n  if second_close <= second_start:\n    return None\n\n  second_text = stripped[\n    second_start:\n    second_close\n  ]\n  suffix = stripped[\n    second_close + 1:\n  ].strip()\n\n  if not suffix.startswith(\n    "より,"\n  ):\n    return None\n\n  if (\n    not first_text.isdigit()\n    or not second_text.isdigit()\n  ):\n    return None\n\n  return (\n    int(\n      first_text\n    ),\n    int(\n      second_text\n    ),\n  )\n'
ORDER_HELPER = 'def order_toda_group_proof_narrative_local_equation_derivations(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  while True:\n    tag_index_by_number = {\n      tag_number: index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      for tag_number in (\n        _toda_group_proof_narrative_equation_tag_number(\n          paragraph\n        ),\n      )\n      if tag_number is not None\n    }\n    moved = False\n\n    for connector_index in range(\n      len(\n        paragraphs\n      ) - 1\n    ):\n      reference_numbers = (\n        _toda_group_proof_narrative_two_equation_reference_numbers(\n          paragraphs[\n            connector_index\n          ]\n        )\n      )\n\n      if reference_numbers is None:\n        continue\n\n      if any(\n        number not in tag_index_by_number\n        for number in reference_numbers\n      ):\n        continue\n\n      derived_tag = (\n        _toda_group_proof_narrative_equation_tag_number(\n          paragraphs[\n            connector_index + 1\n          ]\n        )\n      )\n\n      if derived_tag is None:\n        continue\n\n      source_anchor_index = max(\n        tag_index_by_number[\n          number\n        ]\n        for number in reference_numbers\n      )\n      desired_connector_index = (\n        source_anchor_index + 1\n      )\n\n      if (\n        connector_index\n        == desired_connector_index\n      ):\n        continue\n\n      derivation_paragraphs = paragraphs[\n        connector_index:\n        connector_index + 2\n      ]\n      del paragraphs[\n        connector_index:\n        connector_index + 2\n      ]\n\n      if connector_index < desired_connector_index:\n        desired_connector_index -= 2\n\n      paragraphs[\n        desired_connector_index:\n        desired_connector_index\n      ] = derivation_paragraphs\n      moved = True\n      break\n\n    if not moved:\n      break\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  reference_owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  boundary_filtered_reason_sidecar = type(\n    reason_sidecar\n  )(\n    presentation=reason_sidecar.presentation,\n    reasons=tuple(\n      reason\n      for reason in reason_sidecar.reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in reference_owned_step_ids\n    ),\n  )\n\n  rendered = (\n    insert_toda_group_proof_narrative_reason_prose(\n      contribution_markdown,\n      boundary_filtered_reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_internal_body(\n      presentation,\n      rendered,\n      reference_entries,\n      arguments,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      rendered,\n      statement_lines_by_reference_number,\n    )\n  )\n  rendered = (\n    link_toda_group_proof_narrative_reference_body_consumers(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    normalize_toda_group_proof_narrative_connectors(\n      rendered\n    )\n  )\n  rendered = (\n    order_toda_group_proof_narrative_local_equation_derivations(\n      rendered\n    )\n  )\n\n  generic_used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n\n  if "[R" in rendered:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        rendered,\n      )\n    )\n  else:\n    frontier_step_ids = (\n      _toda_group_proof_narrative_reference_frontier_step_ids(\n        presentation,\n        reference_entries,\n      )\n    )\n    boundary_visible_used_step_ids = frozenset(\n      step_id\n      for step_id in generic_used_step_ids\n      if step_id in frontier_step_ids\n    )\n\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        boundary_visible_used_step_ids,\n        presentation.root_step,\n      )\n    )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  return (\n    reference_section\n    + "\\n\\n"\n    + rendered\n  )\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  normalize_toda_group_proof_narrative_connectors,\n  order_toda_group_proof_narrative_local_equation_derivations,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3(\n  depth: int = 2,\n) -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r6_pi6_53_uses_canonical_suspended_eta_expression():\n  rendered = _render_pi6_3()\n\n  assert (\n    r"$2\\nu\' = \\eta_{3}\\eta_{4}\\eta_{5}$"\n    in rendered\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}E\\eta_{3}\\eta_{5}$"\n    not in rendered\n  )\n\n\ndef test_phase156_r6_pi6_local_calculation_uses_canonical_eta_expression():\n  rendered = _render_pi6_3()\n\n  equation_one = (\n    r"$2\\nu\' = "\n    r"\\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$"\n  )\n  equation_two = (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n  )\n\n  assert equation_one in rendered\n  assert equation_two in rendered\n\n\ndef test_phase156_r6_connector_normalization_removes_only_redundant_generic_connector():\n  markdown = (\n    "$a=b$\\n\\n"\n    "以上より,\\n\\n"\n    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,\\n\\n"\n    "$G=H$"\n  )\n\n  rendered = normalize_toda_group_proof_narrative_connectors(\n    markdown\n  )\n\n  assert "以上より," not in rendered\n  assert (\n    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"\n    in rendered\n  )\n\n\ndef test_phase156_r6_local_ordering_moves_derived_equation_next_to_sources():\n  markdown = (\n    "$a=b\\\\tag{1}$\\n\\n"\n    "$b=c\\\\tag{2}$\\n\\n"\n    "$x=y$\\n\\n"\n    "(1) と (2) より, \\n\\n"\n    "$a=c\\\\tag{3}$"\n  )\n\n  rendered = order_toda_group_proof_narrative_local_equation_derivations(\n    markdown\n  )\n\n  assert (\n    rendered.index(\n      r"$a=b\\tag{1}$"\n    )\n    < rendered.index(\n      r"$b=c\\tag{2}$"\n    )\n    < rendered.index(\n      "(1) と (2) より,"\n    )\n    < rendered.index(\n      r"$a=c\\tag{3}$"\n    )\n    < rendered.index(\n      "$x=y$"\n    )\n  )\n\n\ndef test_phase156_r6_pi6_places_equation3_before_order_and_group_transport():\n  rendered = _render_pi6_3()\n\n  equation_two = (\n    r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n  )\n  connector = "(1) と (2) より,"\n  equation_three = (\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$"\n  )\n  eta_cube_order = (\n    r"$\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2$"\n  )\n  transported_group = (\n    r"$\\pi_{5}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\eta_{4}\\}$"\n  )\n\n  assert (\n    rendered.index(\n      equation_two\n    )\n    < rendered.index(\n      connector\n    )\n    < rendered.index(\n      equation_three\n    )\n    < rendered.index(\n      eta_cube_order\n    )\n    < rendered.index(\n      transported_group\n    )\n  )\n\n\ndef test_phase156_r6_pi6_has_no_redundant_consecutive_result_connectors():\n  rendered = _render_pi6_3()\n\n  assert (\n    "以上より,\\n\\n"\n    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"\n    not in rendered\n  )\n'
TEST_PATHS = ['tests/test_phase143_57c_step_derivation_connector.py', 'tests/test_phase143_61b_direct_premise_narrative.py', 'tests/test_phase144_5_generic_definition_order_equations.py', 'tests/test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py', 'tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py', 'tests/test_phase148_rc2_5_semantic_closure_scope.py']


def _replace_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    text
  )
  function = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if function is None:
    raise RuntimeError(
      "missing function: "
      + function_name
    )

  lines = text.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :function.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :function.end_lineno
    ]
  )

  return (
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ]
  )


def _insert_before_function(
  text: str,
  target_name: str,
  insertion: str,
  sentinel: str,
) -> str:
  if sentinel in text:
    return text

  tree = ast.parse(
    text
  )
  target = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == target_name
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      "missing insertion target: "
      + target_name
    )

  lines = text.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :target.lineno - 1
    ]
  )

  return (
    text[
      :start
    ]
    + insertion
    + "\n\n"
    + text[
      start:
    ]
  )


def _backup(
  path: Path,
  package_dir: Path,
) -> None:
  backup_path = (
    package_dir
    / "backup_before_apply"
    / path
  )
  backup_path.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_path,
  )


def patch_generic_renderer(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_group_proof_generic_narrative_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )

  if GENERIC_IMPORT_OLD not in text:
    if GENERIC_IMPORT_NEW not in text:
      raise RuntimeError(
        "expression import block not found"
      )
    updated = text
  else:
    updated = text.replace(
      GENERIC_IMPORT_OLD,
      GENERIC_IMPORT_NEW,
      1,
    )

  updated = _replace_function(
    updated,
    "_render_generic_narrative_expression_latex",
    GENERIC_EXPR_FUNCTION,
  )

  _backup(
    path.relative_to(
      repo_root
    ),
    package_dir,
  )
  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_generic_narrative_renderer.py"
  )
  print(
    "  Suspension(eta_n) now renders canonically as eta_(n+1)"
  )


def patch_contribution_renderer(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )

  updated = _insert_before_function(
    text,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    (
      CONNECTOR_HELPER
      + "\n\n"
      + TAG_HELPER
      + "\n\n"
      + REF_HELPER
      + "\n\n"
      + ORDER_HELPER
    ),
    "def normalize_toda_group_proof_narrative_connectors(",
  )
  updated = _replace_function(
    updated,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    RENDER_FUNCTION,
  )

  _backup(
    path.relative_to(
      repo_root
    ),
    package_dir,
  )
  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  redundant connector suppression + local equation ordering"
  )


def patch_display_contract_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  old_one = (
    r"2\nu' = \eta_{3}E\eta_{3}\eta_{5}"
  )
  new_one = (
    r"2\nu' = \eta_{3}\eta_{4}\eta_{5}"
  )
  old_two = (
    r"\eta_{3}E\eta_{3}\eta_{5} = "
  )
  new_two = (
    r"\eta_{3}\eta_{4}\eta_{5} = "
  )

  for relative in TEST_PATHS:
    path = (
      repo_root
      / relative
    )

    if not path.exists():
      print(
        "Skipped missing "
        + relative
      )
      continue

    text = path.read_text(
      encoding="utf-8-sig"
    )
    updated = text.replace(
      old_one,
      new_one,
    ).replace(
      old_two,
      new_two,
    )

    if updated == text:
      print(
        "No canonical-expression expectation in "
        + relative
      )
      continue

    _backup(
      path.relative_to(
        repo_root
      ),
      package_dir,
    )
    ast.parse(
      updated
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )

    print(
      "Updated "
      + relative
    )


def write_focused_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r6_canonical_connector_local_ordering.py"
  )
  path.write_text(
    FOCUSED_TEST,
    encoding="utf-8",
  )

  print(
    "Wrote "
    + str(
      path.relative_to(
        repo_root
      )
    )
  )


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = package_dir.parent

  patch_generic_renderer(
    repo_root,
    package_dir,
  )
  patch_contribution_renderer(
    repo_root,
    package_dir,
  )
  patch_display_contract_tests(
    repo_root,
    package_dir,
  )
  write_focused_test(
    repo_root
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
