from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair53_display_closing_fragment_normalization.py"
)

HELPER = 'def _normalize_toda_group_proof_narrative_display_closing_fragments(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  lines = rendered.splitlines()\n  normalized = []\n  closing_fragments = {\n    "である.",\n    "を得る.",\n    "を用いる.",\n    "となる.",\n  }\n\n  for line in lines:\n    stripped = line.strip()\n\n    if (\n      stripped\n      in closing_fragments\n      and normalized\n    ):\n      previous_index = (\n        len(\n          normalized\n        )\n        - 1\n      )\n\n      while (\n        previous_index >= 0\n        and not normalized[\n          previous_index\n        ].strip()\n      ):\n        previous_index -= 1\n\n      if (\n        previous_index >= 0\n        and normalized[\n          previous_index\n        ].strip()\n        == r"\\]"\n      ):\n        del normalized[\n          previous_index + 1:\n        ]\n\n    normalized.append(\n      line\n    )\n\n  return "\\n".join(\n    normalized\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _normalize_toda_group_proof_narrative_display_closing_fragments,\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_group(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair53_helper_merges_only_display_closing_fragment_gap():\n  rendered = (\n    "前文.\\n"\n    "\\n"\n    "\\\\[\\n"\n    "x=y\\n"\n    "\\\\]\\n"\n    "\\n"\n    "を得る.\\n"\n    "\\n"\n    "後文.\\n"\n  )\n\n  normalized = (\n    _normalize_toda_group_proof_narrative_display_closing_fragments(\n      rendered\n    )\n  )\n\n  assert (\n    "\\\\]\\nを得る."\n    in normalized\n  )\n  assert (\n    "\\\\]\\n\\nを得る."\n    not in normalized\n  )\n  assert (\n    "前文.\\n\\n\\\\["\n    in normalized\n  )\n  assert (\n    "を得る.\\n\\n後文."\n    in normalized\n  )\n\n\ndef test_phase157_r20_repair53_pi8_5_has_no_isolated_closing_fragment():\n  rendered = _render_group(\n    5,\n    3,\n  )\n\n  paragraphs = tuple(\n    paragraph.strip()\n    for paragraph in rendered.split(\n      "\\n\\n"\n    )\n    if paragraph.strip()\n  )\n\n  assert "を得る." not in paragraphs\n  assert (\n    r"\\pi_{8}^{5} = "\n    r"\\mathbb{Z}/8\\{\\nu_{5}\\}"\n    in rendered\n  )\n\n\ndef test_phase157_r20_repair53_pi15_8_has_no_isolated_closing_fragments():\n  rendered = _render_group(\n    8,\n    7,\n  )\n\n  paragraphs = tuple(\n    paragraph.strip()\n    for paragraph in rendered.split(\n      "\\n\\n"\n    )\n    if paragraph.strip()\n  )\n\n  assert "である." not in paragraphs\n  assert "を得る." not in paragraphs\n  assert (\n    r"\\pi_{15}^{8} = "\n    r"\\mathbb{Z}\\{\\sigma_{8}\\} "\n    r"\\oplus "\n    r"\\mathbb{Z}/8\\{E\\sigma\'\\}"\n    in rendered\n  )\n\n\ndef test_phase157_r20_repair53_pi6_3_public_narrative_is_unchanged_by_fragment_rule():\n  rendered = _render_group(\n    3,\n    3,\n  )\n\n  assert (\n    r"$E(\\eta_{2}^{3})="\n    r"\\eta_{3}^{3}\\neq0$"\n    in rendered\n  )\n  assert (\n    r"$\\pi_{6}^{3} = "\n    r"\\mathbb{Z}/4\\{\\nu\'\\}$."\n    in rendered\n  )\n  assert rendered.rstrip().endswith(\n    r"$\\square$"\n  )\n'


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
      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def add_helper(
  source: str,
) -> str:
  if (
    "def _normalize_toda_group_proof_narrative_display_closing_fragments("
    in source
  ):
    raise RuntimeError(
      "repair53 helper already exists"
    )

  anchor = (
    "\ndef _finalize_toda_group_proof_narrative_markdown(\n"
  )

  if source.count(
    anchor
  ) != 1:
    raise RuntimeError(
      "repair53 helper anchor was not found exactly once"
    )

  return source.replace(
    anchor,
    "\n\n"
    + HELPER.rstrip()
    + "\n\n"
    + anchor.lstrip(
      "\n"
    ),
    1,
  )


def update_finalizer(
  source: str,
) -> str:
  name = (
    "_finalize_toda_group_proof_narrative_markdown"
  )
  start, end = function_range(
    source,
    name,
  )
  current = source[
    start:
    end
  ]

  old = """  rendered = (
    _phase157_r11_r17_normalize_public_numeric_equalities(
      rendered
    )
  )
  lines = rendered.rstrip().splitlines()
"""

  new = """  rendered = (
    _phase157_r11_r17_normalize_public_numeric_equalities(
      rendered
    )
  )
  rendered = (
    _normalize_toda_group_proof_narrative_display_closing_fragments(
      rendered
    )
  )
  lines = rendered.rstrip().splitlines()
"""

  if current.count(
    old
  ) != 1:
    raise RuntimeError(
      "repair53 finalizer anchor was not found exactly once"
    )

  replacement = current.replace(
    old,
    new,
    1,
  )

  return (
    source[
      :start
    ]
    + replacement
    + source[
      end:
    ]
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  updated = add_helper(
    source
  )
  updated = update_finalizer(
    updated
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in updated:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    updated,
    str(
      TARGET
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair53_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair53 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    TARGET,
  )
  print(
    "Added test:",
    TEST,
  )
  print("")
  print(
    "Import changes: none"
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
      updated.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
