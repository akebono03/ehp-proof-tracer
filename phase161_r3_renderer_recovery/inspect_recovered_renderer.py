from pathlib import Path
import ast
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

RESTORE_NAME = (
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage"
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


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )
  tree = ast.parse(
    source
  )
  lines = source.splitlines()

  print(
    "=" * 78
  )
  print(
    "Recovered renderer shape"
  )
  print(
    "=" * 78
  )
  print(
    "total lines:",
    len(
      lines
    ),
  )

  containing = []

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

    if any(
      _call_name(
        child
      ) == RESTORE_NAME
      for child in ast.walk(
        node
      )
      if isinstance(
        child,
        ast.Call,
      )
    ):
      containing.append(
        node
      )

  print(
    "functions containing restore helper:",
    len(
      containing
    ),
  )

  for function in containing:
    print(
      "  ",
      function.name,
      f"lines {function.lineno}-{function.end_lineno}",
    )

  print()
  print(
    "RECOVERY SHAPE AUDIT COMPLETE"
  )


if __name__ == "__main__":
  main()
