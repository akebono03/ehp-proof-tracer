from __future__ import annotations

import ast
import shutil
from pathlib import Path


TARGET_FUNCTION = "_infer_toda_group_proof_literature_reference_from_rule_name"
NEW_FUNCTION = 'def _infer_toda_group_proof_literature_reference_from_rule_name(\n  rule_name: str,\n) -> LiteratureReference | None:\n  if not isinstance(rule_name, str):\n    raise TypeError("rule_name must be a str")\n\n  normalized_rule_name = rule_name.lower()\n\n  if "bridge" in normalized_rule_name:\n    return None\n\n  named_match = re.match(\n    r"^Toda (Proposition|Lemma|Theorem|Equation) ([0-9]+(?:\\.[0-9]+)*)\\b",\n    rule_name,\n  )\n  if named_match is not None:\n    kind, number = named_match.groups()\n    locator = f"{kind} {number}"\n    return LiteratureReference(\n      label=f"Toda {locator}",\n      locator=locator,\n    )\n\n  parenthesized_match = re.match(\n    r"^Toda \\(([0-9]+(?:\\.[0-9]+)*)\\)\\b",\n    rule_name,\n  )\n  if parenthesized_match is not None:\n    number = parenthesized_match.group(1)\n    locator = f"({number})"\n    return LiteratureReference(\n      label=f"Toda {locator}",\n      locator=locator,\n    )\n\n  bare_equation_match = re.match(\n    r"^Toda ([0-9]+\\.[0-9]+)\\b",\n    rule_name,\n  )\n  if bare_equation_match is not None:\n    number = bare_equation_match.group(1)\n    locator = f"({number})"\n    return LiteratureReference(\n      label=f"Toda {locator}",\n      locator=locator,\n    )\n\n  return None\n'
TEST_SOURCE = 'from toda_group_proof_narrative_references import (\n  _infer_toda_group_proof_literature_reference_from_rule_name,\n)\nfrom toda_rules import (\n  toda_53_eta5_iterated_suspension_bridge_inference_rule,\n)\n\n\ndef test_phase156_r5_repair4_unreferenced_bridge_does_not_infer_reference():\n  reference = (\n    _infer_toda_group_proof_literature_reference_from_rule_name(\n      "Toda 5.3 eta_5 iterated suspension bridge"\n    )\n  )\n\n  assert reference is None\n\n\ndef test_phase156_r5_repair4_standard_equation_rule_still_infers_reference():\n  reference = (\n    _infer_toda_group_proof_literature_reference_from_rule_name(\n      "Toda 5.3 nu-prime specialization"\n    )\n  )\n\n  assert reference is not None\n  assert reference.label == "Toda (5.3)"\n  assert reference.locator == "(5.3)"\n\n\ndef test_phase156_r5_repair4_named_rule_still_infers_reference():\n  reference = (\n    _infer_toda_group_proof_literature_reference_from_rule_name(\n      "Toda Proposition 5.3 finite-dimensional result"\n    )\n  )\n\n  assert reference is not None\n  assert reference.label == "Toda Proposition 5.3"\n  assert reference.locator == "Proposition 5.3"\n\n\ndef test_phase156_r5_repair4_eta5_bridge_rule_has_no_fallback_reference():\n  rule = (\n    toda_53_eta5_iterated_suspension_bridge_inference_rule()\n  )\n\n  assert rule.literature_reference is None\n  assert (\n    _infer_toda_group_proof_literature_reference_from_rule_name(\n      rule.name\n    )\n    is None\n  )\n'


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


def patch_reference_inference(
  repo_root: Path,
  package_dir: Path,
) -> None:
  path = (
    repo_root
    / "toda_group_proof_narrative_references.py"
  )
  text = path.read_text(
    encoding="utf-8-sig"
  )
  tree = ast.parse(
    text
  )
  functions = [
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
  ]

  if len(
    functions
  ) != 1:
    raise RuntimeError(
      "target function count: "
      + str(
        len(
          functions
        )
      )
    )

  function = functions[
    0
  ]
  old_source = _function_source(
    text,
    function,
  )

  if old_source.strip() != NEW_FUNCTION.strip():
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
      / path.name,
    )

    updated = (
      text[
        :start
      ]
      + NEW_FUNCTION
      + text[
        end:
      ]
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )

  (
    package_dir
    / "changed_function_after.txt"
  ).write_text(
    NEW_FUNCTION,
    encoding="utf-8",
  )

  print(
    "Updated toda_group_proof_narrative_references.py"
  )
  print(
    "  unreferenced bridge rules no longer infer literature references"
  )


def write_test(
  repo_root: Path,
) -> None:
  path = (
    repo_root
    / "tests"
    / "test_phase156_r5_repair4_bridge_reference_inference.py"
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


def main() -> int:
  package_dir = Path(
    __file__
  ).resolve().parent
  repo_root = package_dir.parent

  patch_reference_inference(
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
