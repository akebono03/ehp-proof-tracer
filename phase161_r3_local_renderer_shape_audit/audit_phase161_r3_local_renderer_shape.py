from pathlib import Path
import ast
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
OUTPUT_DIR = PACKAGE_DIR / "output"
OUTPUT = OUTPUT_DIR / "phase161_r3_local_renderer_shape.txt"

RESTORE_NAME = (
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage"
)

BODY_FILTER_NAME = (
  "filter_toda_group_proof_narrative_reference_entries_by_body_usage"
)

RELINK_NAME = (
  "link_toda_group_proof_narrative_unmarked_reference_consumers"
)


def _call_name(
  node,
):
  if not isinstance(
    node,
    ast.Call,
  ):
    return None

  function = node.func

  if isinstance(
    function,
    ast.Name,
  ):
    return function.id

  if isinstance(
    function,
    ast.Attribute,
  ):
    return function.attr

  return None


def _node_call_names(
  node,
) -> tuple[str, ...]:
  return tuple(
    name
    for child in ast.walk(
      node
    )
    if isinstance(
      child,
      ast.Call,
    )
    for name in (
      _call_name(
        child
      ),
    )
    if name is not None
  )


def _containing_functions(
  tree,
  call_name: str,
):
  matches = []

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

    if call_name in _node_call_names(
      node
    ):
      matches.append(
        node
      )

  return tuple(
    matches
  )


def _line_slice(
  lines,
  start_line: int,
  end_line: int,
) -> str:
  start = max(
    1,
    start_line,
  )
  end = min(
    len(
      lines
    ),
    end_line,
  )

  return "\n".join(
    f"{number:5d}: {lines[number - 1]}"
    for number in range(
      start,
      end + 1,
    )
  )


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  lines = source.splitlines()
  tree = ast.parse(
    source
  )

  restore_functions = _containing_functions(
    tree,
    RESTORE_NAME,
  )
  body_filter_functions = _containing_functions(
    tree,
    BODY_FILTER_NAME,
  )
  relink_functions = _containing_functions(
    tree,
    RELINK_NAME,
  )

  report_lines = [
    "=" * 78,
    "Phase 161-R3 local renderer shape audit",
    "=" * 78,
    f"target: {TARGET}",
    f"total lines: {len(lines)}",
    "",
    "Functions containing restore helper:",
  ]

  if not restore_functions:
    report_lines.append(
      "  NONE"
    )
  else:
    for function in restore_functions:
      report_lines.extend(
        (
          (
            "  "
            + function.name
            + f"  lines {function.lineno}-{function.end_lineno}"
          ),
          (
            "    calls: "
            + ", ".join(
              _node_call_names(
                function
              )
            )
          ),
        )
      )

  report_lines.extend(
    (
      "",
      "Functions containing body-usage filter:",
    )
  )

  if not body_filter_functions:
    report_lines.append(
      "  NONE"
    )
  else:
    for function in body_filter_functions:
      report_lines.append(
        (
          "  "
          + function.name
          + f"  lines {function.lineno}-{function.end_lineno}"
        )
      )

  report_lines.extend(
    (
      "",
      "Functions containing unmarked-reference relink:",
    )
  )

  if not relink_functions:
    report_lines.append(
      "  NONE"
    )
  else:
    for function in relink_functions:
      report_lines.append(
        (
          "  "
          + function.name
          + f"  lines {function.lineno}-{function.end_lineno}"
        )
      )

  report_lines.extend(
    (
      "",
      "=" * 78,
      "Restore call sites and local context",
      "=" * 78,
    )
  )

  restore_calls = []

  for node in ast.walk(
    tree
  ):
    if (
      isinstance(
        node,
        ast.Call,
      )
      and _call_name(
        node
      ) == RESTORE_NAME
    ):
      restore_calls.append(
        node
      )

  if not restore_calls:
    report_lines.append(
      "NO restore call found."
    )
  else:
    for index, call in enumerate(
      restore_calls,
      start=1,
    ):
      report_lines.extend(
        (
          "",
          f"[restore call {index}] line {call.lineno}",
          _line_slice(
            lines,
            call.lineno - 35,
            call.end_lineno + 45,
          ),
        )
      )

  report_lines.extend(
    (
      "",
      "=" * 78,
      "Candidate render/public functions",
      "=" * 78,
    )
  )

  candidate_functions = tuple(
    node
    for node in ast.walk(
      tree
    )
    if (
      isinstance(
        node,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and (
        "render" in node.name.lower()
        or "public" in node.name.lower()
        or "narrative" in node.name.lower()
      )
      and (
        BODY_FILTER_NAME
        in _node_call_names(
          node
        )
        or RESTORE_NAME
        in _node_call_names(
          node
        )
      )
    )
  )

  for function in candidate_functions:
    report_lines.append(
      (
        function.name
        + f"  lines {function.lineno}-{function.end_lineno}"
      )
    )

  text = "\n".join(
    report_lines
  ) + "\n"

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  OUTPUT.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    text
  )
  print(
    "AUDIT COMPLETE"
  )
  print(
    "Production code changes: none"
  )


if __name__ == "__main__":
  main()
