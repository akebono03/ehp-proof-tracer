from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path


SUPPRESSION_FUNCTION = 'def suppress_toda_group_proof_narrative_reference_internal_body(\n  presentation: TodaGroupProofPresentation,\n  body_markdown: str,\n  reference_entries,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  internal_step_ids = (\n    _toda_group_proof_narrative_reference_internal_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  if not internal_step_ids:\n    return body_markdown\n\n  internal_statement_lines = {\n    rendered\n    for node in presentation.nodes\n    for proof_step in (\n      node.proof_step,\n    )\n    if id(\n      proof_step\n    )\n    in internal_step_ids\n    for rendered in (\n      _render_generic_narrative_step(\n        proof_step\n      ),\n    )\n    if rendered\n  }\n\n  internal_purpose_sentences = set()\n\n  for argument in arguments:\n    conclusion_step = (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n    )\n\n    if (\n      conclusion_step is None\n      or id(\n        conclusion_step\n      )\n      not in internal_step_ids\n    ):\n      continue\n\n    purpose = (\n      render_toda_group_proof_narrative_argument_purpose_sentence(\n        argument\n      )\n    )\n\n    if purpose is not None:\n      internal_purpose_sentences.add(\n        purpose\n      )\n\n  retained_lines = []\n\n  for line in body_markdown.splitlines():\n    stripped = line.strip()\n\n    if stripped in internal_statement_lines:\n      continue\n\n    if any(\n      stripped.endswith(\n        purpose\n      )\n      for purpose in internal_purpose_sentences\n    ):\n      continue\n\n    retained_lines.append(\n      line\n    )\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in retained_lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'
PHASE150_PARAM_TEST = 'def test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract(\n  _label,\n  n,\n  k,\n):\n  (\n    presentation,\n    semantic_sidecar,\n    reason_sidecar,\n    rendered,\n  ) = _render_case(\n    n,\n    k,\n  )\n\n  reference_entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  empty_statement_lines = {\n    entry.number: ()\n    for entry in reference_entries\n  }\n  (\n    reference_entries,\n    _,\n  ) = exclude_toda_group_proof_narrative_root_reference(\n    reference_entries,\n    empty_statement_lines,\n    presentation.root_step,\n  )\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  sentence_reasons = {}\n\n  for reason in reason_sidecar.reasons:\n    sentence = (\n      render_toda_group_proof_narrative_reason_sentence(\n        reason\n      )\n    )\n\n    if sentence is None:\n      continue\n\n    sentence_reasons.setdefault(\n      sentence,\n      [],\n    ).append(\n      reason\n    )\n\n  for sentence, reasons in sentence_reasons.items():\n    visible_reasons = tuple(\n      reason\n      for reason in reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in owned_step_ids\n    )\n\n    if any(\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .FINAL_RESULT_DERIVATION\n      for reason in visible_reasons\n    ):\n      assert rendered.count(\n        sentence\n      ) == 1\n      continue\n\n    assert rendered.count(\n      sentence\n    ) == len(\n      visible_reasons\n    )\n'
REPAIR9_DEPTH2 = 'def test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary():\n  rendered = _render_pi6_3(\n    2\n  )\n  body = _body(\n    rendered\n  )\n\n  assert rendered.startswith(\n    "使用する結果を先にまとめる."\n  )\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert body.startswith(\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n'
REPAIR9_DEPTH3 = 'def test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary():\n  rendered = _render_pi6_3(\n    3\n  )\n  body = _body(\n    rendered\n  )\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert body.startswith(\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3(\n  depth: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r5_repair10_depth2_removes_owned_unreferenced_bracket_line():\n  rendered = _render_pi6_3(\n    2\n  )\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n    in rendered\n  )\n\n\ndef test_phase156_r5_repair10_depth3_removes_owned_unreferenced_bracket_line():\n  rendered = _render_pi6_3(\n    3\n  )\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n    in rendered\n  )\n'


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
          (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
          ),
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

  decorator_lineno = min(
    (
      decorator.lineno
      for decorator in function.decorator_list
    ),
    default=function.lineno,
  )
  start_line = min(
    decorator_lineno,
    function.lineno,
  )

  start = sum(
    len(
      line
    )
    for line in lines[
      :start_line - 1
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
    "suppress_toda_group_proof_narrative_reference_internal_body",
    SUPPRESSION_FUNCTION,
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
    / "changed_suppression_function_after.txt"
  ).write_text(
    SUPPRESSION_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  internal statement suppression now scans presentation.nodes"
  )


def patch_phase150_test(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase150_rc4_5_visible_reasons.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )

  pattern = (
    r'(?:@pytest\.mark\.parametrize\("_label,n,k", CASES\)\s*)+'
    r'def test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract'
  )
  text = re.sub(
    pattern,
    'def test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract',
    text,
    count=1,
  )

  updated = _replace_function(
    text,
    "test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract",
    (
      '@pytest.mark.parametrize("_label,n,k", CASES)\n'
      + PHASE150_PARAM_TEST
    ),
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
    "Updated test_phase150_rc4_5_visible_reasons.py"
  )
  print(
    "  duplicate parametrization collapsed to one decorator"
  )


def patch_repair9_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  updated = _replace_function(
    text,
    "test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary",
    REPAIR9_DEPTH2,
  )
  updated = _replace_function(
    updated,
    "test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary",
    REPAIR9_DEPTH3,
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
    "Updated repair9 focused tests"
  )


def write_repair10_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair10_owned_step_line_suppression.py"
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
  patch_phase150_test(
    repo_root,
    package_dir,
  )
  patch_repair9_tests(
    repo_root,
    package_dir,
  )
  write_repair10_test(
    repo_root
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
