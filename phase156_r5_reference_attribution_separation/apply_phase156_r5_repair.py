from __future__ import annotations

import ast
import shutil
from pathlib import Path


TARGET_FUNCTION = (
  "toda_53_nu_prime_bracket_specialization_inference_rule"
)
OLD_LABEL = "Toda (5.3) / Lemma 5.2"
NEW_LABEL = "Toda (5.3)"
OLD_LOCATOR = "(5.3) / Lemma 5.2"
NEW_LOCATOR = "(5.3)"


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


def _replace_exact_string_literal(
  source: str,
  old: str,
  new: str,
) -> str:
  double_old = (
    '"'
    + old
    + '"'
  )
  single_old = (
    "'"
    + old
    + "'"
  )

  count = (
    source.count(
      double_old
    )
    + source.count(
      single_old
    )
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one literal "
      + repr(
        old
      )
      + " in target function, found "
      + str(
        count
      )
    )

  if double_old in source:
    return source.replace(
      double_old,
      '"'
      + new
      + '"',
      1,
    )

  return source.replace(
    single_old,
    "'"
    + new
    + "'",
    1,
  )


def patch_toda_rules(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_rules.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  tree = ast.parse(
    text
  )
  functions = tuple(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name
      == TARGET_FUNCTION
    )
  )

  if len(
    functions
  ) != 1:
    raise RuntimeError(
      "expected exactly one target function, found "
      + str(
        len(
          functions
        )
      )
    )

  function = functions[
    0
  ]
  source = _function_source(
    text,
    function,
  )

  if (
    OLD_LABEL not in source
    and OLD_LOCATOR not in source
    and 'label="Toda (5.3)"' in source
    and 'locator="(5.3)"' in source
  ):
    print(
      "toda_rules.py already has separated attribution."
    )
    (
      package_dir
      / "changed_function_after.txt"
    ).write_text(
      source,
      encoding="utf-8",
    )
    return

  updated_source = (
    _replace_exact_string_literal(
      source,
      OLD_LABEL,
      NEW_LABEL,
    )
  )
  updated_source = (
    _replace_exact_string_literal(
      updated_source,
      OLD_LOCATOR,
      NEW_LOCATOR,
    )
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
    source
  )
  updated_text = (
    text[
      :start
    ]
    + updated_source
    + text[
      end:
    ]
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

  path.write_text(
    updated_text,
    encoding="utf-8",
  )

  (
    package_dir
    / "changed_function_after.txt"
  ).write_text(
    updated_source,
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
    "  literature reference: "
    + OLD_LOCATOR
    + " -> "
    + NEW_LOCATOR
  )


def write_test(
  repo_root: Path,
) -> None:
  test_path = (
    repo_root
    / "tests"
    / "test_phase156_r5_reference_attribution_separation.py"
  )
  test_path.write_text(
    TEST_SOURCE,
    encoding="utf-8",
  )
  print(
    "Wrote "
    + str(
      test_path.relative_to(
        repo_root
      )
    )
  )


TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  toda_53_nu_prime_bracket_specialization_inference_rule,\n)\n\n\ndef _pi6_3_rendered() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = (\n    build_toda_group_proof_presentation(\n      replay\n    )\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase156_r5_bracket_specialization_is_attributed_to_53_only():\n  rule = (\n    toda_53_nu_prime_bracket_specialization_inference_rule()\n  )\n  reference = (\n    rule.literature_reference\n  )\n\n  assert reference is not None\n  assert reference.label == "Toda (5.3)"\n  assert reference.locator == "(5.3)"\n\n\ndef test_phase156_r5_pi6_reference_section_has_no_composite_53_lemma52_header():\n  rendered = _pi6_3_rendered()\n  reference_part = rendered.split(\n    "まず",\n    1,\n  )[0]\n\n  assert "(5.3) / Lemma 5.2" not in reference_part\n  assert "(5.3)" in reference_part\n\n\ndef test_phase156_r5_pi6_proof_still_records_lemma52_application():\n  rendered = _pi6_3_rendered()\n\n  assert "Lemma 5.2" in rendered\n  assert "Lemma 5.2 を適用" in rendered\n'


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
  write_test(
    repo_root
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
