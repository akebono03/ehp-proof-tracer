from __future__ import annotations

import ast
import shutil
from pathlib import Path


TARGET_FUNCTIONS = (
  "toda_53_nu_prime_lemma52_hopf_inference_rule",
  "toda_53_nu_prime_lemma52_double_inference_rule",
  "toda_53_nu_prime_lemma52_membership_inference_rule",
)

REFERENCE_BLOCK_LINES = (
  'literature_reference=LiteratureReference(\n',
  '  label="Toda Lemma 5.2",\n',
  '  author="H. Toda",\n',
  '  title="Composition Methods in Homotopy Groups of Spheres",\n',
  '  year=1962,\n',
  '  locator="Lemma 5.2",\n',
  '),\n',
)


def _line_indent(
  line: str,
) -> str:
  return line[
    :len(
      line
    )
    - len(
      line.lstrip()
    )
  ]


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


def _reference_block(
  indent: str,
) -> str:
  return "".join(
    indent + line
    for line in REFERENCE_BLOCK_LINES
  )


def patch_toda_rules(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = repo_root / "toda_rules.py"
  text = path.read_text(
    encoding="utf-8-sig"
  )

  if "LiteratureReference" not in text:
    raise RuntimeError(
      "LiteratureReference is not available in toda_rules.py; "
      "repair2 intentionally does not change imports."
    )

  tree = ast.parse(
    text
  )
  functions = {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }
  lines = text.splitlines(
    keepends=True
  )
  insertions = []

  for function_name in TARGET_FUNCTIONS:
    function = functions.get(
      function_name
    )
    if function is None:
      raise RuntimeError(
        "missing function: "
        + function_name
      )

    calls = tuple(
      node
      for node in ast.walk(
        function
      )
      if (
        isinstance(
          node,
          ast.Call,
        )
        and isinstance(
          node.func,
          ast.Name,
        )
        and node.func.id
        == "InferenceRule"
      )
    )

    if len(
      calls
    ) != 1:
      raise RuntimeError(
        function_name
        + ": expected exactly one InferenceRule call, found "
        + str(
          len(
            calls
          )
        )
      )

    call = calls[
      0
    ]
    literature_keywords = tuple(
      keyword
      for keyword in call.keywords
      if keyword.arg
      == "literature_reference"
    )

    if literature_keywords:
      segment = ast.get_source_segment(
        text,
        literature_keywords[
          0
        ].value,
      )
      if (
        segment is not None
        and 'locator="Lemma 5.2"' in segment
      ):
        continue

      raise RuntimeError(
        function_name
        + " already has a non-Lemma-5.2 literature_reference."
      )

    closing_index = (
      call.end_lineno
      - 1
    )
    indent = (
      _line_indent(
        lines[
          closing_index
        ]
      )
      + "  "
    )
    insertions.append(
      (
        closing_index,
        _reference_block(
          indent
        ),
      )
    )

  if insertions:
    backup_dir = (
      package_dir
      / "backup_before_apply"
    )
    backup_dir.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      path,
      backup_dir
      / "toda_rules.py",
    )

    for index, insertion in sorted(
      insertions,
      reverse=True,
    ):
      lines.insert(
        index,
        insertion,
      )

    path.write_text(
      "".join(
        lines
      ),
      encoding="utf-8",
    )

  updated_text = path.read_text(
    encoding="utf-8"
  )
  updated_tree = ast.parse(
    updated_text
  )
  updated_functions = {
    node.name: node
    for node in updated_tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }

  parts = []
  for function_name in TARGET_FUNCTIONS:
    parts.append(
      "# "
      + function_name
      + "\n"
    )
    parts.append(
      _function_source(
        updated_text,
        updated_functions[
          function_name
        ],
      )
    )
    parts.append(
      "\n\n"
    )

  (
    package_dir
    / "changed_functions_after.txt"
  ).write_text(
    "".join(
      parts
    ),
    encoding="utf-8",
  )

  print(
    "Updated toda_rules.py:"
  )
  for function_name in TARGET_FUNCTIONS:
    print(
      "  "
      + function_name
      + " -> Lemma 5.2"
    )


def patch_phase144_reference_tests(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase144_6_r3_production_references.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )

  old_first = '''def test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated():
  presentation, _, _, _ = _phase144_6_r3_pi6_3_data()
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  locators = tuple(entry.reference.locator for entry in entries)

  assert "(5.3) / Lemma 5.2" in locators
  assert "(5.2)" in locators
  assert "Proposition 4.4" in locators
  assert "Proposition 5.1" in locators
  assert locators.count("Proposition 4.4") == 1
  assert "Proposition 2.2" not in locators
'''

  new_first = '''def test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated():
  presentation, _, _, _ = _phase144_6_r3_pi6_3_data()
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  locators = tuple(entry.reference.locator for entry in entries)

  assert "(5.3)" in locators
  assert "Lemma 5.2" in locators
  assert "(5.3) / Lemma 5.2" not in locators
  assert locators.count("(5.3)") == 1
  assert locators.count("Lemma 5.2") == 1
  assert "(5.2)" in locators
  assert "Proposition 4.4" in locators
  assert "Proposition 5.1" in locators
  assert locators.count("Proposition 4.4") == 1
  assert "Proposition 2.2" not in locators
'''

  old_second = '''def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert "使用する結果を先にまとめる." in rendered
  assert "(5.3) / Lemma 5.2" in rendered
  assert "(5.2)" in rendered
  assert "Proposition 4.4" in rendered
  assert "Proposition 5.1" in rendered
  assert "Proposition 2.2" not in rendered
'''

  new_second = '''def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  reference_section = rendered.split(
    "まず",
    1,
  )[0]

  assert "使用する結果を先にまとめる." in reference_section
  assert "(5.3) / Lemma 5.2" not in reference_section
  assert "(5.3)" in reference_section
  assert "Lemma 5.2" in reference_section
  assert "(5.2)" in reference_section
  assert "Proposition 4.4" in reference_section
  assert "Proposition 5.1" in reference_section
  assert "Proposition 2.2" not in reference_section
'''

  updated = text
  for old, new in (
    (
      old_first,
      new_first,
    ),
    (
      old_second,
      new_second,
    ),
  ):
    if new in updated:
      continue
    if updated.count(
      old
    ) != 1:
      raise RuntimeError(
        "Phase144 reference test replacement anchor mismatch."
      )
    updated = updated.replace(
      old,
      new,
      1,
    )

  if updated != text:
    backup_dir = (
      package_dir
      / "backup_before_apply"
    )
    backup_dir.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      path,
      backup_dir
      / "test_phase144_6_r3_production_references.py",
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )

  (
    package_dir
    / "changed_phase144_test_functions_after.txt"
  ).write_text(
    new_first
    + "\n\n"
    + new_second,
    encoding="utf-8",
  )

  print(
    "Updated tests/test_phase144_6_r3_production_references.py"
  )


def write_repair2_tests(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair2_lemma52_specialization_attribution.py"
  )
  path.write_text(
    TEST_SOURCE,
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


TEST_SOURCE = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  toda_53_nu_prime_bracket_specialization_inference_rule,\n  toda_53_nu_prime_lemma52_double_inference_rule,\n  toda_53_nu_prime_lemma52_hopf_inference_rule,\n  toda_53_nu_prime_lemma52_membership_inference_rule,\n)\n\n\ndef _pi6_3_rendered() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = (\n    build_toda_group_proof_presentation(\n      replay\n    )\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r5_repair2_lemma52_rules_have_explicit_lemma52_attribution():\n  rules = (\n    toda_53_nu_prime_lemma52_hopf_inference_rule(),\n    toda_53_nu_prime_lemma52_double_inference_rule(),\n    toda_53_nu_prime_lemma52_membership_inference_rule(),\n  )\n\n  for rule in rules:\n    reference = rule.literature_reference\n    assert reference is not None\n    assert reference.label == "Toda Lemma 5.2"\n    assert reference.locator == "Lemma 5.2"\n\n\ndef test_phase156_r5_repair2_bracket_specialization_remains_53_only():\n  rule = (\n    toda_53_nu_prime_bracket_specialization_inference_rule()\n  )\n  reference = rule.literature_reference\n\n  assert reference is not None\n  assert reference.label == "Toda (5.3)"\n  assert reference.locator == "(5.3)"\n\n\ndef test_phase156_r5_repair2_pi6_reference_headers_separate_53_and_lemma52():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    reference_part,\n  )\n\n  assert "(5.3) / Lemma 5.2" not in reference_part\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert headers.count(\n    "Lemma 5.2"\n  ) == 1\n\n\ndef test_phase156_r5_repair2_pi6_body_still_records_lemma52_application():\n  rendered = _pi6_3_rendered()\n\n  assert "Lemma 5.2 を適用" in rendered\n'


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = (
    package_dir.parent
  )

  patch_toda_rules(
    repo_root,
    package_dir,
  )
  patch_phase144_reference_tests(
    repo_root,
    package_dir,
  )
  write_repair2_tests(
    repo_root
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
