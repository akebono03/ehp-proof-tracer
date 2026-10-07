from pathlib import Path
import ast

TEST_FILE = Path(
  "tests/test_phase159_pi4_3_repair2g_reference_policy.py"
)

FUNCTION_NAME = (
  "test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51"
)

NEW_FUNCTION = 'def test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51():\n  _, _, rendered = _group_data(\n    3,\n    1,\n  )\n  reference = _reference_section(\n    rendered\n  )\n\n  assert "**[R1] (5.1).**" in reference\n  assert (\n    "**[R2] Proposition 5.1.**"\n    in reference\n  )\n\n  assert (\n    r"\\pi_{i}^{n} = 0\\ (i < n)"\n    in reference\n  )\n  assert (\n    r"\\pi_{n}^{n} = "\n    r"\\mathbb{Z}\\{\\iota_{n}\\}"\n    in reference\n  )\n\n  assert (\n    r"\\pi_{5}^{5}"\n    not in reference\n  )\n  assert (\n    r"\\pi_{4}^{5} = 0"\n    not in reference\n  )\n\n  assert (\n    r"\\pi_{3}^{2}"\n    in reference\n  )\n  assert (\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    in reference\n  )\n  assert (\n    r"\\Delta"\n    in reference\n  )\n  assert (\n    r"\\iota_{5}"\n    in reference\n  )\n  assert (\n    r"2\\eta_{2}"\n    in reference\n  )\n\n  assert "Proposition 4.2" not in reference\n  assert r"\\xrightarrow" not in reference\n'


def function_span(
  source: str,
  name: str,
) -> tuple[int, int]:
  tree = ast.parse(
    source
  )
  node = next(
    (
      item
      for item in tree.body
      if isinstance(
        item,
        ast.FunctionDef,
      )
      and item.name == name
    ),
    None,
  )

  if node is None:
    raise RuntimeError(
      f"function not found: {name}"
    )

  lines = source.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :node.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :node.end_lineno
    ]
  )

  return (
    start,
    end,
  )


if not TEST_FILE.exists():
  raise RuntimeError(
    "Target test file was not found. "
    "No file was changed."
  )

source = TEST_FILE.read_text(
  encoding="utf-8"
)

start, end = function_span(
  source,
  FUNCTION_NAME,
)

updated = (
  source[:start]
  + NEW_FUNCTION
  + source[end:]
)

ast.parse(
  updated
)

TEST_FILE.write_text(
  updated,
  encoding="utf-8",
  newline="\n",
)

print(
  "Updated only the stale pi4^3 reference-policy test."
)
