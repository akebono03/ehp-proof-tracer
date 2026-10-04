from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
PRODUCTION = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
PHASE156_TEST = (
  ROOT
  / "tests"
  / "test_phase156_r5_repair12_reference_frontier.py"
)
NEW_TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair31_reference_period_and_stale_frontier_tests.py"
)

NEW_FUNCTION = 'def normalize_toda_group_proof_narrative_display_math_periods(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  normalized_lines = []\n\n  for line in markdown.splitlines():\n    stripped = line.strip()\n\n    if (\n      stripped.endswith(\n        "$"\n      )\n      and "$" in stripped\n      and stripped != r"$\\square$"\n    ):\n      line = line.rstrip() + "."\n\n    normalized_lines.append(\n      line\n    )\n\n  return "\\n".join(\n    normalized_lines\n  )\n'
NEW_TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair31() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair31_reference_prefixed_math_lines_end_with_period():\n  rendered = _render_pi6_3_repair31()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  expected = (\n    "[R3]より, "\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n  )\n\n  assert expected in body\n\n\ndef test_phase157_r20_repair31_r2_hopf_reference_line_ends_with_period():\n  rendered = _render_pi6_3_repair31()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  expected = (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n  )\n\n  assert expected in body\n\n\ndef test_phase157_r20_repair31_all_math_terminated_lines_have_period():\n  rendered = _render_pi6_3_repair31()\n\n  for line in rendered.splitlines():\n    stripped = line.strip()\n\n    if (\n      stripped.endswith(\n        "$"\n      )\n      and "$" in stripped\n      and stripped != r"$\\square$"\n    ):\n      raise AssertionError(\n        "math-terminated line lacks ASCII period: "\n        + stripped\n      )\n'


def function_range(
  source: str,
  name: str,
) -> tuple[
  int,
  int,
]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )
      return (
        start,
        end,
      )

  raise RuntimeError(
    "function not found: "
    + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def update_phase156_stale_expectations(
  source: str,
) -> str:
  old_depth2 = """  assert headers == [
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.6",
  ]
"""

  new_depth2 = """  assert headers == [
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ]
"""

  if source.count(
    old_depth2
  ) != 1:
    raise RuntimeError(
      "stale Phase156 depth2 header expectation "
      "was not found exactly once"
    )

  source = source.replace(
    old_depth2,
    new_depth2,
    1,
  )

  old_depth3 = """  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Proposition 5.6" in headers
  assert "Lemma 5.4" not in headers
  assert "(5.2)" not in headers
"""

  new_depth3 = """  assert headers == [
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ]
  assert "Lemma 5.4" not in headers
  assert "(5.2)" not in headers
"""

  if source.count(
    old_depth3
  ) != 1:
    raise RuntimeError(
      "stale Phase156 depth3 header expectation "
      "was not found exactly once"
    )

  return source.replace(
    old_depth3,
    new_depth3,
    1,
  )


def main() -> int:
  for path in (
    PRODUCTION,
    PHASE156_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        "Run from repository root; missing: "
        + str(
          path
        )
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair31_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    PRODUCTION,
    backup / PRODUCTION.name,
  )
  shutil.copy2(
    PHASE156_TEST,
    backup / PHASE156_TEST.name,
  )

  production_source = PRODUCTION.read_text(
    encoding="utf-8"
  )
  phase156_test_source = PHASE156_TEST.read_text(
    encoding="utf-8"
  )

  production_source = replace_function(
    production_source,
    "normalize_toda_group_proof_narrative_display_math_periods",
    NEW_FUNCTION,
  )
  phase156_test_source = (
    update_phase156_stale_expectations(
      phase156_test_source
    )
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in production_source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    production_source,
    str(
      PRODUCTION
    ),
    "exec",
  )
  compile(
    phase156_test_source,
    str(
      PHASE156_TEST
    ),
    "exec",
  )
  compile(
    NEW_TEST_SOURCE,
    str(
      NEW_TEST
    ),
    "exec",
  )

  PRODUCTION.write_text(
    production_source,
    encoding="utf-8",
    newline="\n",
  )
  PHASE156_TEST.write_text(
    phase156_test_source,
    encoding="utf-8",
    newline="\n",
  )
  NEW_TEST.write_text(
    NEW_TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair31 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    PRODUCTION,
  )
  print(
    "Updated stale test:",
    PHASE156_TEST,
  )
  print(
    "Added test:",
    NEW_TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      production_source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
