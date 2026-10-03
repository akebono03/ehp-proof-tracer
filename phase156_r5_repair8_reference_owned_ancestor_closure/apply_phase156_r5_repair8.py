from __future__ import annotations

import ast
import shutil
from pathlib import Path


OWNED_HELPER = 'def _toda_group_proof_narrative_reference_owned_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  consumers_by_step_id = {}\n\n  for edge in presentation.edges:\n    consumers_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  all_owned_step_ids = set()\n\n  for entry in reference_entries:\n    entry_step_ids = {\n      id(\n        proof_step\n      )\n      for proof_step in entry.proof_steps\n    }\n    owned_step_ids = set(\n      entry_step_ids\n    )\n\n    changed = True\n\n    while changed:\n      changed = False\n\n      for edge in presentation.edges:\n        if (\n          id(\n            edge.parent_step\n          )\n          not in owned_step_ids\n        ):\n          continue\n\n        premise_step = edge.premise_step\n        premise_step_id = id(\n          premise_step\n        )\n\n        if (\n          premise_step\n          is presentation.root_step\n          or premise_step_id\n          in owned_step_ids\n        ):\n          continue\n\n        premise_reference = (\n          extract_toda_group_proof_step_literature_reference(\n            premise_step\n          )\n        )\n\n        if premise_reference is not None:\n          continue\n\n        consumers = tuple(\n          consumers_by_step_id.get(\n            premise_step_id,\n            (),\n          )\n        )\n\n        if not consumers:\n          continue\n\n        if not all(\n          id(\n            consumer\n          )\n          in owned_step_ids\n          for consumer in consumers\n        ):\n          continue\n\n        owned_step_ids.add(\n          premise_step_id\n        )\n        changed = True\n\n    all_owned_step_ids.update(\n      owned_step_ids\n    )\n\n  return frozenset(\n    all_owned_step_ids\n  )\n'
INTERNAL_HELPER = 'def _toda_group_proof_narrative_reference_internal_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  selected_step_ids = set()\n\n  for entry in reference_entries:\n    candidate_steps = []\n    seen_rendered_statements = set()\n\n    for proof_step in entry.proof_steps:\n      rendered_statement = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          proof_step,\n          rendered_statement,\n        )\n      ):\n        continue\n\n      if rendered_statement in seen_rendered_statements:\n        continue\n\n      seen_rendered_statements.add(\n        rendered_statement\n      )\n      candidate_steps.append(\n        proof_step\n      )\n\n    selected_steps = (\n      select_toda_group_proof_narrative_reference_statement_steps(\n        entry,\n        tuple(\n          candidate_steps\n        ),\n        presentation.edges,\n        root_step=presentation.root_step,\n      )\n    )\n\n    selected_step_ids.update(\n      id(\n        proof_step\n      )\n      for proof_step in selected_steps\n    )\n\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  return frozenset(\n    step_id\n    for step_id in owned_step_ids\n    if step_id not in selected_step_ids\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  reference_owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  boundary_filtered_reason_sidecar = type(\n    reason_sidecar\n  )(\n    presentation=reason_sidecar.presentation,\n    reasons=tuple(\n      reason\n      for reason in reason_sidecar.reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in reference_owned_step_ids\n    ),\n  )\n\n  rendered = (\n    insert_toda_group_proof_narrative_reason_prose(\n      contribution_markdown,\n      boundary_filtered_reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_internal_body(\n      presentation,\n      rendered,\n      reference_entries,\n      arguments,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      rendered,\n      statement_lines_by_reference_number,\n    )\n  )\n  rendered = (\n    link_toda_group_proof_narrative_reference_body_consumers(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n\n  generic_used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n\n  if "[R" in rendered:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        rendered,\n      )\n    )\n  else:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        generic_used_step_ids,\n        presentation.root_step,\n      )\n    )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  return (\n    reference_section\n    + "\\n\\n"\n    + rendered\n  )\n'
FOCUSED_TEST = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n  extract_toda_group_proof_narrative_argument_conclusion_step,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_owned_step_ids,\n)\nfrom toda_group_proof_narrative_reasons import (\n  TodaGroupProofNarrativeReasonKind,\n  build_toda_group_proof_narrative_reason_sidecar,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _data(\n  depth: int,\n):\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(\n    presentation\n  )\n  blocks = build_toda_group_proof_narrative_blocks(\n    presentation,\n    semantic_sidecar=semantic_sidecar,\n  )\n  arguments = build_toda_group_proof_narrative_arguments(\n    presentation,\n    blocks,\n    semantic_sidecar=semantic_sidecar,\n  )\n  reasons = build_toda_group_proof_narrative_reason_sidecar(\n    presentation,\n    semantic_sidecar,\n  )\n  entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  empty_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = exclude_toda_group_proof_narrative_root_reference(\n    entries,\n    empty_lines,\n    presentation.root_step,\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  return (\n    presentation,\n    arguments,\n    reasons,\n    entries,\n    rendered,\n  )\n\n\ndef test_phase156_r5_repair8_unreferenced_definition_step_is_reference_owned():\n  (\n    presentation,\n    arguments,\n    reasons,\n    entries,\n    rendered,\n  ) = _data(\n    2\n  )\n\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      entries,\n    )\n  )\n\n  definition_reason = next(\n    reason\n    for reason in reasons.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .DEFINITION_APPLICABILITY\n    )\n  )\n\n  assert id(\n    definition_reason.conclusion_step\n  ) in owned_step_ids\n  assert (\n    definition_reason.conclusion_step.inference_rule\n    is None\n  )\n\n  definition_argument = next(\n    argument\n    for argument in arguments\n    if (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n      is definition_reason.conclusion_step\n    )\n  )\n\n  assert id(\n    extract_toda_group_proof_narrative_argument_conclusion_step(\n      definition_argument\n    )\n  ) in owned_step_ids\n\n\ndef test_phase156_r5_repair8_different_explicit_reference_is_not_absorbed_into_53():\n  (\n    presentation,\n    arguments,\n    reasons,\n    entries,\n    rendered,\n  ) = _data(\n    2\n  )\n\n  definition_reason = next(\n    reason\n    for reason in reasons.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .DEFINITION_APPLICABILITY\n    )\n  )\n  precondition = definition_reason.premise_steps[\n    0\n  ]\n  reference = (\n    precondition\n    .inference_rule\n    .literature_reference\n  )\n\n  assert reference is not None\n  assert reference.locator == "Proposition 5.1"\n\n\ndef test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth2():\n  rendered = _data(\n    2\n  )[\n    -1\n  ]\n  reference_part, body_tail = rendered.split(\n    "まず",\n    1,\n  )\n  body = "まず" + body_tail\n\n  assert "(5.3)" in reference_part\n  assert "Lemma 5.2.**" not in reference_part\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n\n\ndef test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth3():\n  rendered = _data(\n    3\n  )[\n    -1\n  ]\n  reference_part, body_tail = rendered.split(\n    "まず",\n    1,\n  )\n  body = "まず" + body_tail\n\n  assert "(5.3)" in reference_part\n  assert "Lemma 5.2.**" not in reference_part\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n\n\ndef test_phase156_r5_repair8_53_reference_keeps_public_consequences():\n  rendered = _data(\n    2\n  )[\n    -1\n  ]\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  section = next(\n    part\n    for part in re.split(\n      r"(?=\\*\\*\\[R\\d+\\] )",\n      reference_part,\n    )\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] \\(5\\.3\\)\\.\\*\\*",\n      part,\n    )\n  )\n\n  assert "\\\\nu\' \\\\in \\\\pi_{6}^{3}" in section\n  assert "2\\\\nu\'" in section\n'


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
  target_name: str,
  insertion: str,
) -> str:
  if (
    "def _toda_group_proof_narrative_reference_owned_step_ids("
    in text
  ):
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
    "_toda_group_proof_narrative_reference_internal_step_ids",
    OWNED_HELPER,
  )
  updated = _replace_function(
    updated,
    "_toda_group_proof_narrative_reference_internal_step_ids",
    INTERNAL_HELPER,
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
    / "changed_contribution_renderer_functions_after.txt"
  ).write_text(
    OWNED_HELPER
    + "\n\n"
    + INTERNAL_HELPER
    + "\n\n"
    + RENDER_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  added exclusive unreferenced ancestor ownership"
  )
  print(
    "  reason suppression now uses Reference-owned closure"
  )


def write_focused_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair8_reference_owned_ancestor_closure.py"
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

  patch_contribution_renderer(
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
