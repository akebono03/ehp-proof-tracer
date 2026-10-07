
from __future__ import annotations

from pathlib import Path
import ast
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )


def extract_function_source(
  source: str,
  function_name: str,
) -> str:
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
    return source[
      start:
    ]

  end = (
    start
    + 1
    + match.start()
    + 1
  )

  return source[
    start:end
  ]


def assignment_targets(
  node: ast.AST,
) -> tuple[str, ...]:
  names = []

  for child in ast.walk(
    node
  ):
    if isinstance(
      child,
      ast.Name,
    ):
      names.append(
        child.id
      )

  return tuple(
    names
  )


def main() -> int:
  print(
    "=== Phase159 pi_4^3 repair2g fix9 "
    "local post-usage source audit ==="
  )
  print(
    "Production code changes: NONE"
  )
  print(
    "Source:",
    SOURCE_PATH,
  )

  source = SOURCE_PATH.read_text(
    encoding="utf-8"
  )
  function_source = extract_function_source(
    source,
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
  )

  step_usage_marker = (
    "filter_toda_group_proof_narrative_reference_entries_by_step_usage("
  )
  final_render_marker = (
    "render_toda_group_proof_narrative_reference_entries_markdown("
  )

  step_usage_index = function_source.find(
    step_usage_marker
  )
  final_render_index = function_source.find(
    final_render_marker
  )

  if step_usage_index < 0:
    raise RuntimeError(
      "step-usage filter call not found"
    )

  if final_render_index < 0:
    raise RuntimeError(
      "final reference renderer call not found"
    )

  if final_render_index <= step_usage_index:
    raise RuntimeError(
      "final renderer occurs before step-usage filter"
    )

  line_start = function_source.rfind(
    "\n",
    0,
    step_usage_index,
  )
  if line_start < 0:
    line_start = 0

  line_end = function_source.find(
    "\n",
    final_render_index,
  )
  if line_end < 0:
    line_end = len(
      function_source
    )

  segment = function_source[
    line_start:
    line_end
  ]

  print()
  print(
    "=== LOCAL SOURCE SEGMENT ==="
  )
  print(
    segment
  )

  tree = ast.parse(
    function_source
  )

  print()
  print(
    "=== ASSIGNMENTS TOUCHING REFERENCE STATE ==="
  )

  assignment_count = 0

  for node in ast.walk(
    tree
  ):
    targets = ()

    if isinstance(
      node,
      ast.Assign,
    ):
      targets = tuple(
        name
        for target in node.targets
        for name in assignment_targets(
          target
        )
      )
    elif isinstance(
      node,
      ast.AnnAssign,
    ):
      targets = assignment_targets(
        node.target
      )

    if not targets:
      continue

    relevant = tuple(
      name
      for name in targets
      if name in {
        "reference_entries",
        "statement_lines_by_reference_number",
      }
    )

    if not relevant:
      continue

    lineno = getattr(
      node,
      "lineno",
      None,
    )
    end_lineno = getattr(
      node,
      "end_lineno",
      lineno,
    )

    lines = function_source.splitlines()

    snippet = "\n".join(
      lines[
        lineno - 1:
        end_lineno
      ]
    )

    print()
    print(
      "targets=",
      relevant,
      "lines=",
      (
        lineno,
        end_lineno,
      ),
    )
    print(
      snippet
    )

    assignment_count += 1

  print()
  print(
    "reference-state assignment count:",
    assignment_count,
  )

  print()
  print(
    "=== CALLS IN POST-USAGE SEGMENT ==="
  )

  segment_tree = ast.parse(
    "def _segment_wrapper():\n"
    + "\n".join(
      "  " + line
      for line in segment.splitlines()
    )
  )

  call_names = []

  for node in ast.walk(
    segment_tree
  ):
    if not isinstance(
      node,
      ast.Call,
    ):
      continue

    func = node.func

    if isinstance(
      func,
      ast.Name,
    ):
      call_names.append(
        func.id
      )
    elif isinstance(
      func,
      ast.Attribute,
    ):
      call_names.append(
        func.attr
      )

  for name in dict.fromkeys(
    call_names
  ):
    print(
      name
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
