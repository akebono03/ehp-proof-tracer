from __future__ import annotations

import ast
import shutil
from pathlib import Path


RENDER_FUNCTION = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  boundary_step_ids = (\n    _toda_group_proof_narrative_reference_boundary_step_ids(\n      reference_entries\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  boundary_filtered_reason_sidecar = type(\n    reason_sidecar\n  )(\n    presentation=reason_sidecar.presentation,\n    reasons=tuple(\n      reason\n      for reason in reason_sidecar.reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in boundary_step_ids\n    ),\n  )\n\n  rendered = (\n    insert_toda_group_proof_narrative_reason_prose(\n      contribution_markdown,\n      boundary_filtered_reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_internal_body(\n      presentation,\n      rendered,\n      reference_entries,\n      arguments,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      rendered,\n      statement_lines_by_reference_number,\n    )\n  )\n  rendered = (\n    link_toda_group_proof_narrative_reference_body_consumers(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n\n  generic_used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n\n  if "[R" in rendered:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        rendered,\n      )\n    )\n  else:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        generic_used_step_ids,\n        presentation.root_step,\n      )\n    )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  return (\n    reference_section\n    + "\\n\\n"\n    + rendered\n  )\n'
REPAIR2_HEADER_TEST = 'def test_phase156_r5_repair2_pi6_reference_headers_separate_53_and_lemma52():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    reference_part,\n  )\n\n  assert "(5.3) / Lemma 5.2" not in reference_part\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert headers.count(\n    "Lemma 5.2"\n  ) == 0\n'
FOCUSED_TEST = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3(\n  depth: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _parts(\n  rendered: str,\n) -> tuple[\n  str,\n  str,\n]:\n  reference_part, body_tail = rendered.split(\n    "まず",\n    1,\n  )\n  return (\n    reference_part,\n    "まず" + body_tail,\n  )\n\n\ndef test_phase156_r5_repair7_depth2_collapses_53_internal_proof():\n  reference_part, body = _parts(\n    _render_pi6_3(\n      2\n    )\n  )\n\n  assert "(5.3)" in reference_part\n  assert "Lemma 5.2.**" not in reference_part\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n\n\ndef test_phase156_r5_repair7_depth3_collapses_53_internal_proof():\n  reference_part, body = _parts(\n    _render_pi6_3(\n      3\n    )\n  )\n\n  assert "(5.3)" in reference_part\n  assert "Lemma 5.2.**" not in reference_part\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n\n\ndef test_phase156_r5_repair7_53_reference_keeps_public_consequences():\n  reference_part, body = _parts(\n    _render_pi6_3(\n      2\n    )\n  )\n  sections = re.split(\n    r"(?=\\*\\*\\[R\\d+\\] )",\n    reference_part,\n  )\n  section = next(\n    part\n    for part in sections\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] \\(5\\.3\\)\\.\\*\\*",\n      part,\n    )\n  )\n\n  assert "\\\\nu\' \\\\in \\\\pi_{6}^{3}" in section\n  assert "2\\\\nu\'" in section\n'


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
  updated = _replace_function(
    text,
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
    / "changed_render_function_after.txt"
  ).write_text(
    RENDER_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  Reference boundary now uses all non-root entries before final display filtering"
  )


def patch_repair2_test(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair2_lemma52_specialization_attribution.py"
  )

  if not path.exists():
    print(
      "Skipped missing repair2 test"
    )
    return

  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "test_phase156_r5_repair2_pi6_reference_headers_separate_53_and_lemma52",
    REPAIR2_HEADER_TEST,
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
    "Updated repair2 header expectation"
  )


def write_focused_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair7_reference_boundary_filter_order.py"
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
  patch_repair2_test(
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
