from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair39_map_type_name_fallback.py"
)

NEW_FUNCTION = 'def _toda_group_proof_narrative_map_name_latex(\n  group_map,\n) -> str | None:\n  name = getattr(\n    group_map,\n    "name",\n    None,\n  )\n\n  if name is not None:\n    if name in (\n      "Δ",\n      "Delta",\n    ):\n      return r"\\Delta"\n\n    return str(\n      name\n    )\n\n  map_type_name = type(\n    group_map\n  ).__name__\n\n  if map_type_name in (\n    "TodaSuspensionMap",\n    "TodaIteratedSuspensionMap",\n  ):\n    return "E"\n\n  if (\n    map_type_name\n    == "TodaHopfInvariantMap"\n  ):\n    return "H"\n\n  if (\n    map_type_name\n    == "TodaDeltaMap"\n  ):\n    return r"\\Delta"\n\n  return None\n'
TEST_SOURCE = 'from homotopy_groups import (\n  TodaDeltaMap,\n  TodaHopfInvariantMap,\n  TodaPrimaryGroup,\n  TodaSuspensionMap,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_map_name_latex,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef test_phase157_r20_repair39_map_type_name_fallback():\n  source = TodaPrimaryGroup(\n    group_dimension=5,\n    sphere_dimension=2,\n  )\n  middle = TodaPrimaryGroup(\n    group_dimension=6,\n    sphere_dimension=3,\n  )\n  target = TodaPrimaryGroup(\n    group_dimension=6,\n    sphere_dimension=5,\n  )\n\n  assert (\n    _toda_group_proof_narrative_map_name_latex(\n      TodaSuspensionMap(\n        source_group=source,\n        target_group=middle,\n      )\n    )\n    == "E"\n  )\n  assert (\n    _toda_group_proof_narrative_map_name_latex(\n      TodaHopfInvariantMap(\n        source_group=middle,\n        target_group=target,\n      )\n    )\n    == "H"\n  )\n  assert (\n    _toda_group_proof_narrative_map_name_latex(\n      TodaDeltaMap(\n        source_group=target,\n        target_group=source,\n      )\n    )\n    == r"\\Delta"\n  )\n\n\ndef test_phase157_r20_repair39_short_exact_follows_surjectivity():\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n  body = rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )[1]\n\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ "\n    "は全射である."\n  )\n  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n  short_exact = (\n    r"$0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0$."\n  )\n\n  assert body.index(\n    surjectivity\n  ) < body.index(\n    reason\n  )\n  assert body.index(\n    reason\n  ) < body.index(\n    short_exact\n  )\n'


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


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair39_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )
  source = replace_function(
    source,
    "_toda_group_proof_narrative_map_name_latex",
    NEW_FUNCTION,
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    source,
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

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair39 applied."
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
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
