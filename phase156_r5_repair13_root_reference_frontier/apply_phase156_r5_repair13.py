from __future__ import annotations

import ast
import shutil
from pathlib import Path


FRONTIER_FUNCTION = 'def _toda_group_proof_narrative_reference_frontier_step_ids(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n) -> frozenset[int]:\n  children_by_step_id = {}\n\n  for edge in presentation.edges:\n    children_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  root_step = presentation.root_step\n  root_reference = (\n    extract_toda_group_proof_step_literature_reference(\n      root_step\n    )\n  )\n  frontier_step_ids = set()\n\n  for entry in reference_entries:\n    for source_step in entry.proof_steps:\n      queue = deque(\n        [\n          source_step,\n        ]\n      )\n      visited = set()\n\n      while queue:\n        current_step = queue.popleft()\n        current_step_id = id(\n          current_step\n        )\n\n        if current_step_id in visited:\n          continue\n\n        visited.add(\n          current_step_id\n        )\n\n        if current_step is root_step:\n          frontier_step_ids.add(\n            id(\n              source_step\n            )\n          )\n          break\n\n        for child_step in children_by_step_id.get(\n          current_step_id,\n          (),\n        ):\n          if child_step is root_step:\n            frontier_step_ids.add(\n              id(\n                source_step\n              )\n            )\n            queue.clear()\n            break\n\n          child_reference = (\n            extract_toda_group_proof_step_literature_reference(\n              child_step\n            )\n          )\n\n          if (\n            child_reference is not None\n            and child_reference != entry.reference\n            and child_reference != root_reference\n          ):\n            continue\n\n          queue.append(\n            child_step\n          )\n\n  return frozenset(\n    frontier_step_ids\n  )\n'
REPAIR3_TEST = 'def test_phase156_r5_repair3_two_eta3_zero_is_not_under_53_header():\n  rendered = _pi6_3_rendered()\n  sections = re.split(\n    r"(?=\\*\\*\\[R\\d+\\] )",\n    rendered,\n  )\n  source_53 = next(\n    section\n    for section in sections\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] \\(5\\.3\\)\\.\\*\\*",\n      section,\n    )\n  )\n\n  assert "$2\\\\eta_{3} = 0$" not in source_53\n  assert "Proposition 5.1" not in rendered\n'
FOCUSED_TEST = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_frontier_step_ids,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _data(\n  depth: int,\n):\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(\n    presentation\n  )\n  blocks = build_toda_group_proof_narrative_blocks(\n    presentation,\n    semantic_sidecar=semantic_sidecar,\n  )\n  arguments = build_toda_group_proof_narrative_arguments(\n    presentation,\n    blocks,\n    semantic_sidecar=semantic_sidecar,\n  )\n  entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  empty_lines = {\n    entry.number: ()\n    for entry in entries\n  }\n  entries, _ = exclude_toda_group_proof_narrative_root_reference(\n    entries,\n    empty_lines,\n    presentation.root_step,\n  )\n  return (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    entries,\n  )\n\n\ndef test_phase156_r5_repair13_proposition51_is_not_on_root_reference_frontier():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    entries,\n  ) = _data(\n    2\n  )\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  prop51 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "Proposition 5.1"\n  )\n\n  assert all(\n    id(\n      proof_step\n    )\n    not in frontier_step_ids\n    for proof_step in prop51.proof_steps\n  )\n\n\ndef test_phase156_r5_repair13_toda52_is_on_root_reference_frontier():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    entries,\n  ) = _data(\n    2\n  )\n  frontier_step_ids = (\n    _toda_group_proof_narrative_reference_frontier_step_ids(\n      presentation,\n      entries,\n    )\n  )\n  toda52 = next(\n    entry\n    for entry in entries\n    if entry.reference.locator == "(5.2)"\n  )\n\n  assert any(\n    id(\n      proof_step\n    )\n    in frontier_step_ids\n    for proof_step in toda52.proof_steps\n  )\n\n\ndef test_phase156_r5_repair13_depth2_public_reference_headers():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    entries,\n  ) = _data(\n    2\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert headers == [\n    "(5.3)",\n    "Proposition 5.3",\n    "Lemma 5.4",\n    "(5.2)",\n  ]\n\n\ndef test_phase156_r5_repair13_depth3_keeps_52_and_prunes_51():\n  raw = _data(\n    3\n  )[\n    0\n  ]\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert "Proposition 5.1" not in headers\n  assert "(5.3)" in headers\n  assert "Proposition 5.3" in headers\n  assert "Lemma 5.4" in headers\n  assert "(5.2)" in headers\n'


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
  updated = _replace_function(
    text,
    "_toda_group_proof_narrative_reference_frontier_step_ids",
    FRONTIER_FUNCTION,
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
    / "changed_frontier_function_after.txt"
  ).write_text(
    FRONTIER_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  root Reference transitions are now allowed"
  )


def patch_repair3_test(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair3_eta3_zero_attribution.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "test_phase156_r5_repair3_two_eta3_zero_is_not_under_53_header",
    REPAIR3_TEST,
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
    "Updated test_phase156_r5_repair3_eta3_zero_attribution.py"
  )


def write_focused_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair13_root_reference_frontier.py"
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

  patch_production(
    repo_root,
    package_dir,
  )
  patch_repair3_test(
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
