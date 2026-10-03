from __future__ import annotations

import ast
import shutil
from pathlib import Path


EXTERNAL_HELPER = 'def _toda_group_proof_narrative_reference_externally_used_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  internal_step_ids = (\n    _toda_group_proof_narrative_reference_internal_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n  internal_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if id(\n      node.proof_step\n    )\n    in internal_step_ids\n  )\n\n  externally_used_step_ids = set()\n\n  for entry in reference_entries:\n    for proof_step in entry.proof_steps:\n      if (\n        _phase153_r7_reaches_root_without_steps(\n          presentation,\n          proof_step,\n          internal_steps,\n        )\n      ):\n        externally_used_step_ids.add(\n          id(\n            proof_step\n          )\n        )\n\n  return frozenset(\n    externally_used_step_ids\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n\n  reference_owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n  boundary_filtered_reason_sidecar = type(\n    reason_sidecar\n  )(\n    presentation=reason_sidecar.presentation,\n    reasons=tuple(\n      reason\n      for reason in reason_sidecar.reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in reference_owned_step_ids\n    ),\n  )\n\n  rendered = (\n    insert_toda_group_proof_narrative_reason_prose(\n      contribution_markdown,\n      boundary_filtered_reason_sidecar,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_internal_body(\n      presentation,\n      rendered,\n      reference_entries,\n      arguments,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n  rendered = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      rendered,\n      statement_lines_by_reference_number,\n    )\n  )\n  rendered = (\n    link_toda_group_proof_narrative_reference_body_consumers(\n      presentation,\n      rendered,\n      reference_entries,\n    )\n  )\n\n  generic_used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n\n  if "[R" in rendered:\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        rendered,\n      )\n    )\n  else:\n    externally_used_reference_step_ids = (\n      _toda_group_proof_narrative_reference_externally_used_step_ids(\n        presentation,\n        reference_entries,\n      )\n    )\n    boundary_visible_used_step_ids = frozenset(\n      step_id\n      for step_id in generic_used_step_ids\n      if step_id in externally_used_reference_step_ids\n    )\n\n    (\n      reference_entries,\n      statement_lines_by_reference_number,\n    ) = (\n      filter_toda_group_proof_narrative_reference_entries_by_step_usage(\n        reference_entries,\n        statement_lines_by_reference_number,\n        boundary_visible_used_step_ids,\n        presentation.root_step,\n      )\n    )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  return (\n    reference_section\n    + "\\n\\n"\n    + rendered\n  )\n'
PHASE144_PUBLIC = 'def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():\n  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n\n  assert "使用する結果を先にまとめる." in rendered\n  assert "(5.3) / Lemma 5.2" not in rendered\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "(5.2)" in rendered\n  assert "Proposition 5.3" in rendered\n  assert "Lemma 5.4" in rendered\n  assert "Proposition 5.1" not in rendered\n  assert "Proposition 2.2" not in rendered\n'
REPAIR3_HEADER = 'def test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header():\n  rendered = _pi6_3_rendered()\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert headers.count(\n    "Lemma 5.2"\n  ) == 0\n  assert headers.count(\n    "Proposition 5.1"\n  ) == 0\n  assert "(5.3) / Lemma 5.2" not in rendered\n'
FOCUSED_TEST = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _data(\n  depth: int,\n):\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(\n    presentation\n  )\n  blocks = build_toda_group_proof_narrative_blocks(\n    presentation,\n    semantic_sidecar=semantic_sidecar,\n  )\n  arguments = build_toda_group_proof_narrative_arguments(\n    presentation,\n    blocks,\n    semantic_sidecar=semantic_sidecar,\n  )\n  return (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n  )\n\n\ndef test_phase156_r5_repair11_raw_graph_keeps_proposition51_reference():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n  ) = _data(\n    2\n  )\n  entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  locators = {\n    entry.reference.locator\n    for entry in entries\n  }\n\n  assert "Proposition 5.1" in locators\n\n\ndef test_phase156_r5_repair11_public_pi6_prunes_internal_only_proposition51_depth2():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n  ) = _data(\n    2\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert headers == [\n    "(5.3)",\n    "Proposition 5.3",\n    "Lemma 5.4",\n    "(5.2)",\n  ]\n  assert "Proposition 5.1" not in rendered\n\n\ndef test_phase156_r5_repair11_public_pi6_prunes_internal_only_proposition51_depth3():\n  raw = _data(\n    3\n  )[\n    0\n  ]\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert "Proposition 5.1" not in headers\n  assert "(5.3)" in headers\n  assert "(5.2)" in headers\n  assert "Lemma 5.2" not in rendered\n\n\ndef test_phase156_r5_repair11_reference_numbers_are_compact_after_pruning():\n  raw = _data(\n    2\n  )[\n    0\n  ]\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  numbers = [\n    int(\n      number\n    )\n    for number in re.findall(\n      r"\\*\\*\\[R(\\d+)\\] ",\n      rendered,\n    )\n  ]\n\n  assert numbers == list(\n    range(\n      1,\n      len(\n        numbers\n      )\n      + 1,\n    )\n  )\n'


def _function_source(
  text: str,
  function,
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
) -> str:
  if (
    "def _toda_group_proof_narrative_reference_externally_used_step_ids("
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


def _patch_function_file(
  path: Path,
  replacements: dict[
    str,
    str,
  ],
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
  updated = text

  for function_name, replacement in replacements.items():
    updated = _replace_function(
      updated,
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
    + path.name
  )


def patch_production(
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
    EXTERNAL_HELPER,
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
    / "changed_production_functions_after.txt"
  ).write_text(
    EXTERNAL_HELPER
    + "\n\n"
    + RENDER_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  added Reference dependency pruning at final step-usage selection"
  )


def patch_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  _patch_function_file(
    repo_root
    / "tests"
    / "test_phase144_6_r3_production_references.py",
    {
      "test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section": (
        PHASE144_PUBLIC
      ),
    },
    package_dir,
  )

  _patch_function_file(
    repo_root
    / "tests"
    / "test_phase156_r5_repair3_eta3_zero_attribution.py",
    {
      "test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header": (
        REPAIR3_HEADER
      ),
    },
    package_dir,
  )

  focused_path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair11_reference_dependency_pruning.py"
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

  patch_production(
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
