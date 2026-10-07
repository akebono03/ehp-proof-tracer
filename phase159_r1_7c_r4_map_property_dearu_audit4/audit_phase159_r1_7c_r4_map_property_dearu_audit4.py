from pathlib import Path
import ast
import inspect
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
  )


import toda_group_proof_aggregate_statement_renderer as aggregate_renderer
import toda_group_proof_narrative_contribution_renderer as contribution_renderer


TARGET_LITERALS = (
  "は単射である.",
  "は全射である.",
)


def _function_spans(
  source: str,
):
  tree = ast.parse(
    source
  )
  spans = []

  for node in ast.walk(
    tree
  ):
    if not isinstance(
      node,
      (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
      ),
    ):
      continue

    end_lineno = getattr(
      node,
      "end_lineno",
      None,
    )

    if end_lineno is None:
      continue

    spans.append(
      (
        node.lineno,
        end_lineno,
        node.name,
        node.col_offset,
      )
    )

  return tuple(
    spans
  )


def _enclosing_functions(
  spans,
  line_number: int,
):
  matches = [
    span
    for span in spans
    if (
      span[0]
      <= line_number
      <= span[1]
    )
  ]

  return tuple(
    sorted(
      matches,
      key=lambda span: (
        span[3],
        span[0],
      ),
    )
  )


def _audit_module(
  title: str,
  module,
) -> int:
  source = inspect.getsource(
    module
  )
  lines = source.splitlines()
  spans = _function_spans(
    source
  )
  count = 0

  print()
  print(
    "=" * 78
  )
  print(
    title
  )
  print(
    "=" * 78
  )

  for line_number, line in enumerate(
    lines,
    start=1,
  ):
    hits = tuple(
      literal
      for literal in TARGET_LITERALS
      if literal in line
    )

    if not hits:
      continue

    count += len(
      hits
    )
    enclosing = _enclosing_functions(
      spans,
      line_number,
    )

    print()
    print(
      "line:",
      line_number,
    )
    print(
      "source:",
      line.strip(),
    )
    print(
      "hits:",
      ", ".join(
        hits
      ),
    )

    if not enclosing:
      print(
        "enclosing functions: <none>"
      )
      continue

    print(
      "enclosing functions:"
    )

    for (
      start,
      end,
      name,
      indent,
    ) in enclosing:
      print(
        " ",
        name,
        f"lines={start}-{end}",
        f"indent={indent}",
      )

  return count


def main() -> None:
  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property 'である' function-owner audit4"
  )
  print(
    "=" * 78
  )

  contribution_count = _audit_module(
    "toda_group_proof_narrative_contribution_renderer.py",
    contribution_renderer,
  )
  aggregate_count = _audit_module(
    "toda_group_proof_aggregate_statement_renderer.py",
    aggregate_renderer,
  )

  print()
  print(
    "=" * 78
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 78
  )
  print(
    "contribution literal occurrences:",
    contribution_count,
  )
  print(
    "aggregate literal occurrences:",
    aggregate_count,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Test code changes: none"
  )
  print(
    "Full pytest: not run"
  )


if __name__ == "__main__":
  main()
