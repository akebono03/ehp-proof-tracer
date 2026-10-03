from __future__ import annotations

import ast
import shutil
from pathlib import Path


PHASE150_IMPORTS = 'import inspect\n\nimport pytest\n\nfrom tests.test_phase143_19_method_evidence import (\n  _method_evidence_data,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_owned_step_ids,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_reason_renderer import (\n  render_toda_group_proof_narrative_reason_sentence,\n)\nfrom toda_group_proof_narrative_reasons import (\n  TodaGroupProofNarrativeReasonKind,\n  build_toda_group_proof_narrative_reason_sidecar,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n)\n'
PHASE150_FIRST = 'def test_phase150_rc4_5_pi6_reason_is_visible_before_definition():\n  (\n    presentation,\n    semantic_sidecar,\n    reason_sidecar,\n    rendered,\n  ) = _render_case(\n    3,\n    3,\n  )\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .DEFINITION_APPLICABILITY\n    )\n  )\n  sentence = render_toda_group_proof_narrative_reason_sentence(\n    reason\n  )\n\n  reference_entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  empty_statement_lines = {\n    entry.number: ()\n    for entry in reference_entries\n  }\n  (\n    reference_entries,\n    _,\n  ) = exclude_toda_group_proof_narrative_root_reference(\n    reference_entries,\n    empty_statement_lines,\n    presentation.root_step,\n  )\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  assert sentence is not None\n  assert id(\n    reason.conclusion_step\n  ) in owned_step_ids\n  assert sentence not in rendered\n'
PHASE150_SECOND = '@pytest.mark.parametrize("_label,n,k", CASES)\ndef test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract(\n  _label,\n  n,\n  k,\n):\n  (\n    presentation,\n    semantic_sidecar,\n    reason_sidecar,\n    rendered,\n  ) = _render_case(\n    n,\n    k,\n  )\n\n  reference_entries = build_toda_group_proof_narrative_reference_entries(\n    presentation\n  )\n  empty_statement_lines = {\n    entry.number: ()\n    for entry in reference_entries\n  }\n  (\n    reference_entries,\n    _,\n  ) = exclude_toda_group_proof_narrative_root_reference(\n    reference_entries,\n    empty_statement_lines,\n    presentation.root_step,\n  )\n  owned_step_ids = (\n    _toda_group_proof_narrative_reference_owned_step_ids(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  sentence_reasons = {}\n\n  for reason in reason_sidecar.reasons:\n    sentence = (\n      render_toda_group_proof_narrative_reason_sentence(\n        reason\n      )\n    )\n\n    if sentence is None:\n      continue\n\n    sentence_reasons.setdefault(\n      sentence,\n      [],\n    ).append(\n      reason\n    )\n\n  for sentence, reasons in sentence_reasons.items():\n    visible_reasons = tuple(\n      reason\n      for reason in reasons\n      if id(\n        reason.conclusion_step\n      )\n      not in owned_step_ids\n    )\n\n    if any(\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .FINAL_RESULT_DERIVATION\n      for reason in visible_reasons\n    ):\n      assert rendered.count(\n        sentence\n      ) == 1\n      continue\n\n    assert rendered.count(\n      sentence\n    ) == len(\n      visible_reasons\n    )\n'
REPAIR1_TEST = 'def test_phase156_r5_pi6_proof_still_records_lemma52_application():\n  rendered = _pi6_3_rendered()\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n'
REPAIR2_BODY = 'def test_phase156_r5_repair2_pi6_body_still_records_lemma52_application():\n  rendered = _pi6_3_rendered()\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n'
REPAIR6_BODY = 'def test_phase156_r5_repair6_pi6_body_does_not_expand_53_internal_proof():\n  rendered = _pi6_3_rendered()\n\n  assert "Lemma 5.2" not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert "$\\\\nu\'$ を定める." not in rendered\n'
REPAIR6_DEPTH3 = 'def test_phase156_r5_repair6_depth3_keeps_same_public_boundary():\n  rendered = _pi6_3_rendered(\n    depth=3,\n  )\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2.**" not in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n'
REPAIR7_PARTS = 'def _parts(\n  rendered: str,\n) -> tuple[\n  str,\n  str,\n]:\n  body_marker = (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n  body_index = rendered.find(\n    body_marker\n  )\n\n  if body_index < 0:\n    raise AssertionError(\n      "pi_6^3 public body start marker is missing"\n    )\n\n  return (\n    rendered[\n      :body_index\n    ].rstrip(),\n    rendered[\n      body_index:\n    ],\n  )\n'
REPAIR8_DEPTH2 = 'def test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth2():\n  rendered = _data(\n    2\n  )[\n    -1\n  ]\n\n  body_marker = (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n  body_index = rendered.find(\n    body_marker\n  )\n\n  assert body_index >= 0\n  body = rendered[\n    body_index:\n  ]\n\n  assert "(5.3)" in rendered[\n    :body_index\n  ]\n  assert "Lemma 5.2.**" not in rendered[\n    :body_index\n  ]\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n'
REPAIR8_DEPTH3 = 'def test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth3():\n  rendered = _data(\n    3\n  )[\n    -1\n  ]\n\n  body_marker = (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n  body_index = rendered.find(\n    body_marker\n  )\n\n  assert body_index >= 0\n  body = rendered[\n    body_index:\n  ]\n\n  assert "(5.3)" in rendered[\n    :body_index\n  ]\n  assert "Lemma 5.2.**" not in rendered[\n    :body_index\n  ]\n  assert "Lemma 5.2" not in body\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in body\n  )\n  assert "$2\\\\eta_{3} = 0$" not in body\n  assert "$\\\\nu\'$ を定める." not in body\n'
FOCUSED_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3(\n  depth: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _body(\n  rendered: str,\n) -> str:\n  marker = (\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n  index = rendered.find(\n    marker\n  )\n  assert index >= 0\n  return rendered[\n    index:\n  ]\n\n\ndef test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary():\n  rendered = _render_pi6_3(\n    2\n  )\n  body = _body(\n    rendered\n  )\n\n  assert rendered.startswith(\n    "使用する結果を先にまとめる."\n  )\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert body.startswith(\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n\n\ndef test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary():\n  rendered = _render_pi6_3(\n    3\n  )\n  body = _body(\n    rendered\n  )\n\n  assert "(5.3)" in rendered\n  assert "Lemma 5.2" not in rendered\n  assert "$\\\\nu\'$ を定める." not in rendered\n  assert (\n    "\\\\nu\' \\\\in "\n    "\\\\{\\\\eta_{3}, 2\\\\iota_{4}, \\\\eta_{4}\\\\}_{1}"\n    not in rendered\n  )\n  assert body.startswith(\n    "次に, $\\\\nu\'$ の位数を決定するために"\n  )\n'


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


def _replace_import_prefix(
  text: str,
  new_imports: str,
) -> str:
  tree = ast.parse(
    text
  )
  body_nodes = tree.body

  import_nodes = []
  for node in body_nodes:
    if isinstance(
      node,
      (
        ast.Import,
        ast.ImportFrom,
      ),
    ):
      import_nodes.append(
        node
      )
      continue

    if (
      isinstance(
        node,
        ast.Assign,
      )
      and import_nodes
    ):
      break

    if import_nodes:
      break

  if not import_nodes:
    raise RuntimeError(
      "no import block found"
    )

  lines = text.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :import_nodes[0].lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :import_nodes[-1].end_lineno
    ]
  )

  suffix = text[
    end:
  ]
  suffix = suffix.lstrip(
    "\n"
  )

  return (
    text[
      :start
    ]
    + new_imports.rstrip()
    + "\n\n\n"
    + suffix
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


def _patch_functions(
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


def patch_phase150(
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
  updated = _replace_import_prefix(
    text,
    PHASE150_IMPORTS,
  )
  updated = _replace_function(
    updated,
    "test_phase150_rc4_5_pi6_reason_is_visible_before_definition",
    PHASE150_FIRST,
  )
  updated = _replace_function(
    updated,
    "test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract",
    PHASE150_SECOND,
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
    / "changed_phase150_imports_and_functions_after.txt"
  ).write_text(
    PHASE150_IMPORTS
    + "\n\n"
    + PHASE150_FIRST
    + "\n\n"
    + PHASE150_SECOND,
    encoding="utf-8",
  )

  print(
    "Updated test_phase150_rc4_5_visible_reasons.py"
  )


def patch_phase156_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  _patch_functions(
    repo_root
    / "tests"
    / "test_phase156_r5_reference_attribution_separation.py",
    {
      "test_phase156_r5_pi6_proof_still_records_lemma52_application": (
        REPAIR1_TEST
      ),
    },
    package_dir,
  )

  _patch_functions(
    repo_root
    / "tests"
    / "test_phase156_r5_repair2_lemma52_specialization_attribution.py",
    {
      "test_phase156_r5_repair2_pi6_body_still_records_lemma52_application": (
        REPAIR2_BODY
      ),
    },
    package_dir,
  )

  _patch_functions(
    repo_root
    / "tests"
    / "test_phase156_r5_repair6_reference_boundary_collapse.py",
    {
      "test_phase156_r5_repair6_pi6_body_does_not_expand_53_internal_proof": (
        REPAIR6_BODY
      ),
      "test_phase156_r5_repair6_depth3_keeps_same_public_boundary": (
        REPAIR6_DEPTH3
      ),
    },
    package_dir,
  )

  _patch_functions(
    repo_root
    / "tests"
    / "test_phase156_r5_repair7_reference_boundary_filter_order.py",
    {
      "_parts": REPAIR7_PARTS,
    },
    package_dir,
  )

  _patch_functions(
    repo_root
    / "tests"
    / "test_phase156_r5_repair8_reference_owned_ancestor_closure.py",
    {
      "test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth2": (
        REPAIR8_DEPTH2
      ),
      "test_phase156_r5_repair8_public_pi6_collapses_53_internal_proof_depth3": (
        REPAIR8_DEPTH3
      ),
    },
    package_dir,
  )

  focused_path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
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

  patch_phase150(
    repo_root,
    package_dir,
  )
  patch_phase156_tests(
    repo_root,
    package_dir,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
