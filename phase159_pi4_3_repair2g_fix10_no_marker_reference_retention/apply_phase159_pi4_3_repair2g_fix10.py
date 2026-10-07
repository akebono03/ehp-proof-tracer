
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
SNAPSHOT_PATH = (
  Path(__file__).resolve().parent
  / "patched_render_function_after_apply.py.txt"
)


def extract_function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      f"{function_name}: function not found"
    )

  match = re.search(
    r"\n(?=def [A-Za-z0-9_]+\()",
    source[start + 1:],
  )

  if match is None:
    return (
      start,
      len(
        source
      ),
    )

  end = (
    start
    + 1
    + match.start()
    + 1
  )

  return (
    start,
    end,
  )


def main() -> int:
  source = TARGET_PATH.read_text(
    encoding="utf-8"
  )

  function_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  start, end = extract_function_span(
    source,
    function_name,
  )
  function_source = source[
    start:end
  ]

  obsolete_block = (
    '  if "[R" not in rendered:\n'
    '    reference_entries = ()\n'
    '    statement_lines_by_reference_number = {}\n'
    '\n'
  )

  if obsolete_block in function_source:
    function_source = (
      function_source.replace(
        obsolete_block,
        "",
        1,
      )
    )
    changed = True
  else:
    changed = False

  if (
    'if "[R" not in rendered:'
    in function_source
  ):
    raise RuntimeError(
      "unexpected no-marker Reference clearing "
      "still remains in target function"
    )

  prune_call = (
    "prune_toda_group_proof_narrative_"
    "root_zero_direct_premise_references("
  )

  if prune_call not in function_source:
    raise RuntimeError(
      "required root-zero direct-premise Reference pruning "
      "is missing from local target function"
    )

  if (
    "filter_toda_group_proof_narrative_"
    "reference_entries_by_step_usage("
    not in function_source
  ):
    raise RuntimeError(
      "required no-marker step-usage filter is missing"
    )

  patched_source = (
    source[:start]
    + function_source
    + source[end:]
  )

  TARGET_PATH.write_text(
    patched_source,
    encoding="utf-8",
    newline="\n",
  )

  SNAPSHOT_PATH.write_text(
    function_source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair2g fix10 applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Function: "
    + function_name
  )
  print(
    "Removed no-marker unconditional Reference clearing:",
    changed,
  )
  print(
    "Preserved: "
    "prune_toda_group_proof_narrative_"
    "root_zero_direct_premise_references"
  )
  print(
    "Full patched function written to:"
  )
  print(
    SNAPSHOT_PATH
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
