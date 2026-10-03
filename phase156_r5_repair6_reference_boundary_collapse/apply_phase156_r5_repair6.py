from __future__ import annotations

import ast
import shutil
from pathlib import Path


HELPER = 'def _toda_group_proof_narrative_reference_boundary_step_ids(\n  reference_entries,\n) -> frozenset[int]:\n  return frozenset(\n    id(\n      proof_step\n    )\n    for entry in reference_entries\n    for proof_step in entry.proof_steps\n  )\n\n\ndef _toda_group_proof_narrative_reference_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  internal_step_ids = set()\n\n  for entry in reference_entries:\n    candidate_steps = []\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          proof_step,\n          rendered_statement,\n        )\n      ):\n        continue\n\n      if rendered_statement in seen_rendered_statements:\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n    selected_step_ids = {\n      id(\n        proof_step\n      )\n      for proof_step in selected_steps\n    }\n\n    internal_step_ids.update(\n      id(\n        proof_step\n      )\n      for proof_step in entry.proof_steps\n      if id(\n        proof_step\n      )\n      not in selected_step_ids\n    )\n\n  return frozenset(\n    internal_step_ids\n  )\n\n\ndef suppress_toda_group_proof_narrative_reference_internal_body(\n  presentation: TodaGroupProofPresentation,\n  body_markdown: str,\n  reference_entries,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  internal_step_ids = (\n    _toda_group_proof_narrative_reference_internal_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  if not internal_step_ids:\n    return body_markdown\n\n  internal_statement_lines = {\n    rendered\n    for entry in reference_entries\n    for proof_step in entry.proof_steps\n    if id(\n      proof_step\n    )\n    in internal_step_ids\n    for rendered in (\n      _render_generic_narrative_step(\n        proof_step\n      ),\n    )\n    if rendered\n  }\n\n  internal_purpose_sentences = set()\n\n  for argument in arguments:\n    conclusion_step = (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n    )\n\n    if (\n      conclusion_step is None\n      or id(\n        conclusion_step\n      )\n      not in internal_step_ids\n    ):\n      continue\n\n    purpose = (\n      render_toda_group_proof_narrative_argument_purpose_sentence(\n        argument\n      )\n    )\n\n    if purpose is not None:\n      internal_purpose_sentences.add(\n        purpose\n      )\n\n  retained_lines = []\n\n  for line in body_markdown.splitlines():\n    stripped = line.strip()\n\n    if stripped in internal_statement_lines:\n      continue\n\n    if any(\n      stripped.endswith(\n        purpose\n      )\n      for purpose in internal_purpose_sentences\n    ):\n      continue\n\n    retained_lines.append(\n      line\n    )\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in retained_lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  generic_used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  (\n    boundary_reference_entries,\n    boundary_statement_lines,\n  ) = (\n    filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n      reference_entries,\n      statement_lines_by_reference_number,\n      generic_used_step_ids,\n      presentation.root_step,\n    )\n  )\n\n  boundary_step_ids = (\n    _toda_group_proof_narrative_reference_boundary_step_ids(\n      boundary_reference_entries\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  boundary_filtered_reason_sidecar = type(\n    reason_sidecar\n  )(\n    presentation=reason_sidecar.presentation,\n    reasons=tuple(\n      reason\n      for reason in reason_sidecar.reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in boundary_step_ids\n    ),\n  )\n\n  rendered = (\n    insert_toda_group_proof_narrative_reason_prose(\n      contribution_markdown,\n      boundary_filtered_reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_internal_body(\n      presentation,\n      rendered,\n      boundary_reference_entries,\n      arguments,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      rendered,\n      statement_lines_by_reference_number,\n    )\n  )\n  rendered = (\n    link_toda_group_proof_narrative_reference_body_consumers(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n\n  if "[R" in rendered:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        rendered,\n      )\n    )\n  else:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        generic_used_step_ids,\n        presentation.root_step,\n      )\n    )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  return (\n    reference_section\n    + "\\n\\n"\n    + rendered\n  )\n'
BASELINE_REASON_SENTENCE = 'def render_toda_group_proof_narrative_reason_sentence(\n  reason: TodaGroupProofNarrativeReason,\n) -> str | None:\n  if not isinstance(\n    reason,\n    TodaGroupProofNarrativeReason,\n  ):\n    raise TypeError(\n      "reason must be a "\n      "TodaGroupProofNarrativeReason"\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .DEFINITION_APPLICABILITY\n  ):\n    application = reason.reference_application\n\n    if application is None or len(application.bindings) != 1:\n      return (\n        "この前提条件を満たすので, "\n        "次の定義を用いる."\n      )\n\n    binding = application.bindings[0]\n    reference_label = application.reference.label\n    formal_latex = render_toda_expression_latex(\n      binding.formal_variable\n    )\n    instantiated_latex = render_toda_expression_latex(\n      binding.instantiated_expression\n    )\n\n    return (\n      "この前提条件を満たすので, "\n      f"{reference_label} を適用できる.\\n"\n      f"{reference_label} の "\n      f"${formal_latex}$ を "\n      f"${instantiated_latex}$ と定めると, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_MAP_PROPERTY\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    exactness_statement = (\n      reason.premise_steps[1].conclusion\n    )\n    window = exactness_statement.window\n    first_map_name = window.first_map.name\n    second_map_name = window.second_map.name\n\n    return (\n      "この完全性と "\n      f"${first_map_name}=0$ より, "\n      f"$\\\\ker {second_map_name}"\n      f"=\\\\operatorname{{Im}}{first_map_name}=0$ "\n      "である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .MULTIPLE_RELATION_TO_ORDER\n  ):\n    if len(reason.premise_steps) != 2:\n      return None\n\n    order_statement = reason.premise_steps[0].conclusion\n    equality_statement = reason.premise_steps[1].conclusion\n    ordered_latex = render_toda_expression_latex(order_statement.lhs)\n    target_latex = render_toda_expression_latex(\n      equality_statement.lhs.expression\n    )\n\n    return (\n      f"$\\\\operatorname{{ord}}({ordered_latex})=2$ "\n      f"かつ $2{target_latex}={ordered_latex}$ より, "\n      f"$4{target_latex}=0$ かつ "\n      f"$2{target_latex}\\\\neq0$ である.\\n"\n      "したがって, "\n    )\n\n  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .FINAL_GROUP_STRUCTURE\n  ):\n    if len(reason.premise_steps) != 7:\n      return None\n\n    left_group_statement = reason.premise_steps[0].conclusion\n    right_group_statement = reason.premise_steps[4].conclusion\n    order_statement = reason.premise_steps[5].conclusion\n    membership_statement = reason.premise_steps[6].conclusion\n\n    left_order = left_group_statement.rhs.order\n    right_order = right_group_statement.rhs.order\n    middle_order = left_order * right_order\n    generator_latex = render_toda_expression_latex(\n      membership_statement.element\n    )\n\n    return (\n      "この短完全列と両端の群の位数より, "\n      f"中央の群の位数は ${left_order}\\\\cdot"\n      f"{right_order}={middle_order}$ である.\\n"\n      f"また, ${generator_latex}$ は中央の群に属し, "\n      f"$\\\\operatorname{{ord}}({generator_latex})"\n      f"={order_statement.rhs}={middle_order}$ であるから, "\n      f"${generator_latex}$ は中央の群を生成する.\\n"\n      "したがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:\n    return (\n      "この完全性, 既知の群構造, および写像の像に関する結果を合わせると, "\n      "対象となる写像の像と核が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:\n    return (\n      "この群構造と写像による移送の結果を合わせると, "\n      "対象の群の位数と写像の単射性が決まる.\\nしたがって, "\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:\n    return "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "\n\n  return None\n'
BASELINE_INSERTION = 'def _toda_group_proof_narrative_reason_insertion_index(\n  markdown: str,\n  reason: TodaGroupProofNarrativeReason,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> int | None:\n  conclusion_line = _render_generic_narrative_step(\n    reason.conclusion_step\n  )\n  if conclusion_line:\n    conclusion_index = markdown.find(conclusion_line)\n    if conclusion_index >= 0:\n      return conclusion_index\n\n  children_by_step_id = {}\n  for edge in reason_sidecar.presentation.edges:\n    children_by_step_id.setdefault(\n      id(edge.premise_step),\n      [],\n    ).append(edge.parent_step)\n\n  queue = list(\n    children_by_step_id.get(\n      id(reason.conclusion_step),\n      (),\n    )\n  )\n  visited_step_ids = {\n    id(reason.conclusion_step),\n  }\n\n  while queue:\n    next_queue = []\n    for proof_step in queue:\n      proof_step_id = id(proof_step)\n      if proof_step_id in visited_step_ids:\n        continue\n      visited_step_ids.add(proof_step_id)\n\n      rendered_line = _render_generic_narrative_step(\n        proof_step\n      )\n      if rendered_line:\n        rendered_index = markdown.find(rendered_line)\n        if rendered_index >= 0:\n          return rendered_index\n\n      next_queue.extend(\n        children_by_step_id.get(\n          proof_step_id,\n          (),\n        )\n      )\n    queue = next_queue\n\n  return None\n'
FOCUSED_TEST = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _pi6_3_rendered(\n  depth: int = 2,\n) -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r5_repair6_reference_53_is_public_boundary():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    reference_part,\n  )\n\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert "Lemma 5.2" not in headers\n\n\ndef test_phase156_r5_repair6_pi6_body_does_not_expand_53_internal_proof():\n  rendered = _pi6_3_rendered()\n  body = "まず" + rendered.split(\n    "まず",\n    1,\n  )[1]\n\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n\n\ndef test_phase156_r5_repair6_pi6_keeps_53_consequences_as_reference_results():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n\n  section = next(\n    part\n    for part in re.split(\n      r"(?=\\*\\*\\[R\\d+\\] )",\n      reference_part,\n    )\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] \\(5\\.3\\)\\.\\*\\*",\n      part,\n    )\n  )\n\n  assert "\\\\nu\' \\\\in \\\\pi_{6}^{3}" in section\n  assert "2\\\\nu\'" in section\n\n\ndef test_phase156_r5_repair6_depth3_keeps_same_public_boundary():\n  rendered = _pi6_3_rendered(\n    depth=3,\n  )\n  reference_part, body_tail = rendered.split(\n    "まず",\n    1,\n  )\n  body = "まず" + body_tail\n\n  assert reference_part.count(\n    "(5.3)"\n  ) >= 1\n  assert "Lemma 5.2.**" not in reference_part\n  assert "Lemma 5.2" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n'
PHASE150_RESTORE = 'def test_phase150_rc4_5b_3_renderer_uses_typed_reference_and_binding():\n  presentation, semantic_sidecar, reason_sidecar = _pi6_data()\n  sentence = render_toda_group_proof_narrative_reason_sentence(\n    reason_sidecar.reasons[0]\n  )\n  assert sentence == (\n    "この前提条件を満たすので, Lemma 5.2 を適用できる.\\n"\n    "Lemma 5.2 の $\\\\beta$ を $\\\\nu\'$ と定めると, "\n  )\n'
PHASE144_FIRST = 'def test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated():\n  presentation, _, _, _ = _phase144_6_r3_pi6_3_data()\n  entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  locators = tuple(entry.reference.locator for entry in entries)\n\n  assert "(5.3)" in locators\n  assert "Lemma 5.2" not in locators\n  assert "(5.3) / Lemma 5.2" not in locators\n  assert locators.count("(5.3)") == 1\n  assert "(5.2)" in locators\n  assert "Proposition 4.4" in locators\n  assert "Proposition 5.1" in locators\n  assert locators.count("Proposition 4.4") == 1\n  assert "Proposition 2.2" not in locators\n'
PHASE144_SECOND = 'def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():\n  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n  reference_section = rendered.split(\n    "まず",\n    1,\n  )[0]\n\n  assert "使用する結果を先にまとめる." in reference_section\n  assert "(5.3) / Lemma 5.2" not in reference_section\n  assert "(5.3)" in reference_section\n  assert "Lemma 5.2" not in reference_section\n  assert "(5.2)" in reference_section\n  assert "Proposition 4.4" in reference_section\n  assert "Proposition 5.1" in reference_section\n  assert "Proposition 2.2" not in reference_section\n'
REPAIR1_TEST = 'def test_phase156_r5_pi6_proof_still_records_lemma52_application():\n  rendered = _pi6_3_rendered()\n  reference_part, body_tail = rendered.split(\n    "まず",\n    1,\n  )\n  body = "まず" + body_tail\n\n  assert "Lemma 5.2" not in reference_part\n  assert "Lemma 5.2" not in body\n'
REPAIR3_TEST = 'def test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    reference_part,\n  )\n\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert headers.count(\n    "Lemma 5.2"\n  ) == 0\n  assert headers.count(\n    "Proposition 5.1"\n  ) == 1\n  assert "(5.3) / Lemma 5.2" not in reference_part\n'


def _function_source(
  text: str,
  function: ast.FunctionDef,
) -> str:
  lines = text.splitlines(
    keepends=True
  )
  return "".join(
    lines[
      function.lineno - 1:
      function.end_lineno
    ]
  )


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

  old_source = _function_source(
    text,
    function,
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
  end = start + len(
    old_source
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
  function_name: str,
  insertion: str,
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
      "missing insertion target: "
      + function_name
    )

  if (
    "def _toda_group_proof_narrative_reference_boundary_step_ids("
    in text
  ):
    return text

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
  backup_dir = (
    package_dir
    / "backup_before_apply"
    / path.parent.name
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    backup_dir
    / path.name,
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
    HELPER,
  )
  updated = _replace_function(
    updated,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    RENDER_FUNCTION,
  )

  _backup(
    path,
    package_dir,
  )
  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  (
    package_dir
    / "changed_contribution_renderer_after.txt"
  ).write_text(
    HELPER
    + "\n\n"
    + RENDER_FUNCTION,
    encoding="utf-8",
  )
  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )


def restore_reason_renderer(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_group_proof_narrative_reason_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "render_toda_group_proof_narrative_reason_sentence",
    BASELINE_REASON_SENTENCE,
  )
  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_reason_insertion_index",
    BASELINE_INSERTION,
  )

  _backup(
    path,
    package_dir,
  )
  ast.parse(
    updated
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )

  (
    package_dir
    / "restored_reason_renderer_functions.txt"
  ).write_text(
    BASELINE_REASON_SENTENCE
    + "\n\n"
    + BASELINE_INSERTION,
    encoding="utf-8",
  )
  print(
    "Restored repair5 reason-renderer changes to generic baseline"
  )


def patch_test_function(
  path: Path,
  function_name: str,
  replacement: str,
  package_dir: Path,
) -> None:
  if not path.exists():
    print(
      "Skipped missing "
      + str(
        path
      )
    )
    return

  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    function_name,
    replacement,
  )

  _backup(
    path,
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
    + str(
      path.name
    )
    + "::"
    + function_name
  )


def patch_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  phase144 = (
    repo_root
    / "tests"
    / "test_phase144_6_r3_production_references.py"
  )
  patch_test_function(
    phase144,
    "test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated",
    PHASE144_FIRST,
    package_dir,
  )
  patch_test_function(
    phase144,
    "test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section",
    PHASE144_SECOND,
    package_dir,
  )

  patch_test_function(
    repo_root
    / "tests"
    / "test_phase150_rc4_5b_3_reference_binding.py",
    "test_phase150_rc4_5b_3_renderer_uses_typed_reference_and_binding",
    PHASE150_RESTORE,
    package_dir,
  )

  patch_test_function(
    repo_root
    / "tests"
    / "test_phase156_r5_reference_attribution_separation.py",
    "test_phase156_r5_pi6_proof_still_records_lemma52_application",
    REPAIR1_TEST,
    package_dir,
  )

  patch_test_function(
    repo_root
    / "tests"
    / "test_phase156_r5_repair3_eta3_zero_attribution.py",
    "test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header",
    REPAIR3_TEST,
    package_dir,
  )

  repair2 = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair2_lemma52_specialization_attribution.py"
  )
  if repair2.exists():
    text = repair2.read_text(
      encoding="utf-8-sig"
    )
    text = text.replace(
      'assert reference.label == "Toda Lemma 5.2"',
      'assert reference.label == "Toda (5.3)"',
    )
    text = text.replace(
      'assert reference.locator == "Lemma 5.2"',
      'assert reference.locator == "(5.3)"',
    )
    text = text.replace(
      'assert headers.count("Lemma 5.2") == 1',
      'assert headers.count("Lemma 5.2") == 0',
    )
    text = text.replace(
      'assert "Lemma 5.2 を適用" in rendered',
      'assert "Lemma 5.2" not in rendered.split("まず", 1)[1]',
    )
    _backup(
      repair2,
      package_dir,
    )
    ast.parse(
      text
    )
    repair2.write_text(
      text,
      encoding="utf-8",
    )
    print(
      "Updated repair2 intermediate contract"
    )

  repair5 = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair5_53_source_lemma52_dependency.py"
  )
  if repair5.exists():
    _backup(
      repair5,
      package_dir,
    )
    repair5.unlink()
    print(
      "Removed superseded repair5 focused test"
    )

  focused_path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair6_reference_boundary_collapse.py"
  )
  focused_path.write_text(
    FOCUSED_TEST,
    encoding="utf-8",
  )
  print(
    "Wrote "
    + str(
      focused_path.relative_to(
        repo_root
      )
    )
  )


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = package_dir.parent

  patch_contribution_renderer(
    repo_root,
    package_dir,
  )
  restore_reason_renderer(
    repo_root,
    package_dir,
  )
  patch_tests(
    repo_root,
    package_dir,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
