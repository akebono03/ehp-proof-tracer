from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = ROOT / "toda_upstream_bootstrap.py"
BOUNDARY_PATH = ROOT / "toda_literature_statement_boundary.py"
CONTRIBUTION_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_PATH = (
  ROOT
  / "tests"
  / "test_phase159_pi4_3_repair2g_reference_policy.py"
)


def function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
  marker = "def " + function_name + "("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"{function_name}: function not found"
    )

  match = re.search(
    r"\n(?=def [A-Za-z0-9_]+\()",
    source[start + 1:],
  )

  if match is None:
    return start, len(source)

  end = start + 1 + match.start() + 1
  return start, end


def replace_once(
  source: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = source.count(old)

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return source.replace(
    old,
    new,
    1,
  )


def rewire_phase50_metadata() -> None:
  source = BOOTSTRAP_PATH.read_text(
    encoding="utf-8"
  )
  start, end = function_span(
    source,
    "_build_phase50_result",
  )
  body = source[start:end]

  replacements = (
    (
      "'Toda (5.1) diagonal free cyclic'",
      "'Toda (5.1) diagonal identity group'",
      "pi_5^5 (5.1) component rule name",
    ),
    (
      "'Toda (5.1) below-diagonal zero'",
      "'Toda (5.1) sphere connectivity zero'",
      "pi_4^5 (5.1) component rule name",
    ),
  )

  for old, new, label in replacements:
    if new in body:
      continue

    if old not in body:
      raise RuntimeError(
        f"{label}: neither old nor new rule name found"
      )

    body = replace_once(
      body,
      old,
      new,
      label,
    )

  source = source[:start] + body + source[end:]

  BOOTSTRAP_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def remove_obsolete_boundary_mappings() -> None:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  obsolete_fragments = (
    '  "Toda (5.1) below-diagonal zero": '
    '"basic_sphere_group_relations",\n',
    '  "Toda (5.1) diagonal free cyclic": '
    '"basic_sphere_group_relations",\n',
    '  "Toda (5.1) below-diagonal zero": "(5.1)",\n',
    '  "Toda (5.1) diagonal free cyclic": "(5.1)",\n',
  )

  for fragment in obsolete_fragments:
    source = source.replace(
      fragment,
      "",
    )

  if "basic_sphere_group_relations" in source:
    remaining = tuple(
      line
      for line in source.splitlines()
      if "basic_sphere_group_relations" in line
    )
    raise RuntimeError(
      "obsolete basic_sphere_group_relations references "
      "remain in boundary catalog:\n"
      + "\n".join(remaining)
    )

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def remove_obsolete_aggregate_renderer_branch() -> None:
  source = CONTRIBUTION_PATH.read_text(
    encoding="utf-8"
  )
  start, end = function_span(
    source,
    "_phase157_r20_canonical_fixed_reference_line",
  )
  body = source[start:end]

  marker = '    and boundary.component_key\n    == "basic_sphere_group_relations"\n'
  if marker in body:
    block_start = body.rfind(
      "  if (\n",
      0,
      body.index(marker),
    )
    block_end = body.find(
      "\n  if (\n",
      body.index(marker),
    )
    if block_start < 0 or block_end < 0:
      raise RuntimeError(
        "obsolete aggregate renderer branch span not found"
      )
    body = body[:block_start] + body[block_end + 1:]

  if "basic_sphere_group_relations" in body:
    raise RuntimeError(
      "obsolete aggregate component remains in "
      "canonical reference renderer"
    )

  source = source[:start] + body + source[end:]

  CONTRIBUTION_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def patch_focused_tests() -> None:
  source = TEST_PATH.read_text(
    encoding="utf-8"
  )

  start, end = function_span(
    source,
    "test_phase159_repair2g_phase50_fixed_sources_have_expected_boundaries",
  )
  body = source[start:end]

  old = (
    "  for step in (\n"
    "    pi5_step,\n"
    "    pi4_zero_step,\n"
    "  ):\n"
  )
  new = (
    "  expected_51_components = (\n"
    "    (\n"
    "      pi5_step,\n"
    "      \"diagonal_identity_group\",\n"
    "    ),\n"
    "    (\n"
    "      pi4_zero_step,\n"
    "      \"sphere_connectivity_zero\",\n"
    "    ),\n"
    "  )\n"
    "\n"
    "  for step, expected_component_key in (\n"
    "    expected_51_components\n"
    "  ):\n"
  )
  if new not in body:
    body = replace_once(
      body,
      old,
      new,
      "phase50 existing (5.1) component loop",
    )

  old_key = (
    "    assert (\n"
    "      boundary.component_key\n"
    "      == \"basic_sphere_group_relations\"\n"
    "    )\n"
  )
  new_key = (
    "    assert (\n"
    "      boundary.component_key\n"
    "      == expected_component_key\n"
    "    )\n"
  )
  if new_key not in body:
    body = replace_once(
      body,
      old_key,
      new_key,
      "phase50 existing (5.1) component key",
    )

  source = source[:start] + body + source[end:]

  start, end = function_span(
    source,
    "test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51",
  )
  body = source[start:end]

  old_public = (
    '  assert (\n'
    '    r"\\pi_i^1=0"\n'
    '    in reference\n'
    '  )\n'
    '  assert (\n'
    '    r"\\pi_i^n=0"\n'
    '    in reference\n'
    '  )\n'
    '  assert (\n'
    '    r"\\pi_n^n="\n'
    '    in reference\n'
    '  )\n'
    '  assert (\n'
    '    r"\\mathbb{Z}\\{\\iota_n\\}"\n'
    '    in reference\n'
    '  )\n'
  )
  new_public = (
    '  assert (\n'
    '    r"\\pi_{5}^{5}"\n'
    '    in reference\n'
    '  )\n'
    '  assert (\n'
    '    r"\\mathbb{Z}\\{\\iota_{5}\\}"\n'
    '    in reference\n'
    '  )\n'
    '  assert (\n'
    '    r"\\pi_{4}^{5} = 0"\n'
    '    in reference\n'
    '  )\n'
  )
  if new_public not in body:
    body = replace_once(
      body,
      old_public,
      new_public,
      "pi4 public concrete (5.1) expectations",
    )

  source = source[:start] + body + source[end:]

  TEST_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def verify_no_obsolete_component() -> None:
  for path in (
    BOOTSTRAP_PATH,
    BOUNDARY_PATH,
    CONTRIBUTION_PATH,
    TEST_PATH,
  ):
    source = path.read_text(
      encoding="utf-8"
    )

    if "basic_sphere_group_relations" in source:
      raise RuntimeError(
        "obsolete aggregate component remains in "
        + str(path)
      )


def main() -> int:
  rewire_phase50_metadata()
  remove_obsolete_boundary_mappings()
  remove_obsolete_aggregate_renderer_branch()
  patch_focused_tests()
  verify_no_obsolete_component()

  print("Phase 159 pi_4^3 repair2g fix6 applied.")
  print("Changed: toda_upstream_bootstrap.py")
  print("Changed: toda_literature_statement_boundary.py")
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Changed: "
    "tests/test_phase159_pi4_3_repair2g_reference_policy.py"
  )
  print(
    "Removed obsolete component: "
    "basic_sphere_group_relations"
  )
  print(
    "Rewired pi_5^5 -> diagonal_identity_group"
  )
  print(
    "Rewired pi_4^5=0 -> sphere_connectivity_zero"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
