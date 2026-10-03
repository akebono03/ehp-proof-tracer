from __future__ import annotations

import ast
import shutil
from pathlib import Path


TARGET_FUNCTION = (
  "toda_53_eta3_twice_zero_inference_rule"
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
      "LiteratureReference is not available in toda_rules.py."
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
  function = functions.get(
    TARGET_FUNCTION
  )

  if function is None:
    raise RuntimeError(
      "missing function: "
      + TARGET_FUNCTION
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
      "expected exactly one InferenceRule call, found "
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
      and 'label="Toda Proposition 5.1"' in segment
      and 'locator="Proposition 5.1"' in segment
    ):
      updated_text = text
    else:
      raise RuntimeError(
        TARGET_FUNCTION
        + " already has a different explicit literature_reference."
      )
  else:
    lines = text.splitlines(
      keepends=True
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
    insertion = (
      indent
      + "literature_reference=LiteratureReference(\n"
      + indent
      + '  label="Toda Proposition 5.1",\n'
      + indent
      + '  author="H. Toda",\n'
      + indent
      + '  title="Composition Methods in Homotopy Groups of Spheres",\n'
      + indent
      + "  year=1962,\n"
      + indent
      + '  locator="Proposition 5.1",\n'
      + indent
      + "),\n"
    )

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

    lines.insert(
      closing_index,
      insertion,
    )
    updated_text = "".join(
      lines
    )
    path.write_text(
      updated_text,
      encoding="utf-8",
    )

  updated_tree = ast.parse(
    updated_text
  )
  updated_function = next(
    node
    for node in updated_tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name
      == TARGET_FUNCTION
    )
  )

  (
    package_dir
    / "changed_function_after.txt"
  ).write_text(
    _function_source(
      updated_text,
      updated_function,
    ),
    encoding="utf-8",
  )

  print(
    "Updated toda_rules.py:"
  )
  print(
    "  "
    + TARGET_FUNCTION
  )
  print(
    "  literature reference -> Proposition 5.1"
  )


def write_tests(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair3_eta3_zero_attribution.py"
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


TEST_SOURCE = 'import re\n\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  toda_53_eta3_twice_zero_inference_rule,\n)\n\n\ndef _pi6_3_rendered() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = (\n    build_toda_group_proof_presentation(\n      replay\n    )\n  )\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r5_repair3_eta3_twice_zero_is_attributed_to_proposition51():\n  rule = (\n    toda_53_eta3_twice_zero_inference_rule()\n  )\n  reference = rule.literature_reference\n\n  assert reference is not None\n  assert reference.label == "Toda Proposition 5.1"\n  assert reference.locator == "Proposition 5.1"\n\n\ndef test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    reference_part,\n  )\n\n  assert headers.count(\n    "(5.3)"\n  ) == 1\n  assert headers.count(\n    "Lemma 5.2"\n  ) == 1\n  assert headers.count(\n    "Proposition 5.1"\n  ) == 1\n  assert "(5.3) / Lemma 5.2" not in reference_part\n\n\ndef test_phase156_r5_repair3_two_eta3_zero_is_not_under_53_header():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n\n  sections = re.split(\n    r"(?=\\*\\*\\[R\\d+\\] )",\n    reference_part,\n  )\n  source_53 = next(\n    section\n    for section in sections\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] \\(5\\.3\\)\\.\\*\\*",\n      section,\n    )\n  )\n  proposition51 = next(\n    section\n    for section in sections\n    if re.search(\n      r"\\*\\*\\[R\\d+\\] Proposition 5\\.1\\.\\*\\*",\n      section,\n    )\n  )\n\n  assert "2\\\\eta_{3} = 0" not in source_53\n  assert "2\\\\eta_{3} = 0" in proposition51\n'


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = package_dir.parent

  patch_toda_rules(
    repo_root,
    package_dir,
  )
  write_tests(
    repo_root
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
