from pathlib import Path
import ast

paths = (
  Path(
    "toda_group_proof_narrative_argument_multi_renderer.py"
  ),
  Path(
    "toda_group_proof_narrative_argument_body_renderer.py"
  ),
)

for path in paths:
  raw = path.read_bytes()
  text = raw.decode(
    "utf-8-sig"
  )

  print(
    "=" * 78
  )
  print(
    path
  )
  print(
    "BOM:",
    raw.startswith(
      b"\xef\xbb\xbf"
    ),
  )
  print(
    "-" * 78
  )

  tree = ast.parse(
    text
  )

  for node in tree.body:
    if isinstance(
      node,
      (
        ast.Import,
        ast.ImportFrom,
      ),
    ):
      source = ast.get_source_segment(
        text,
        node,
      )
      print(
        source
      )

  print(
    "-" * 78
  )

  for function_name in (
    "render_toda_group_proof_narrative_multi_argument_markdown",
    "render_toda_group_proof_narrative_argument_body_markdown",
  ):
    matches = [
      node
      for node in tree.body
      if isinstance(
        node,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and node.name == function_name
    ]

    if len(
      matches
    ) != 1:
      continue

    node = matches[
      0
    ]
    source = ast.get_source_segment(
      text,
      node,
    )

    if source is None:
      continue

    print(
      "FUNCTION",
      function_name,
    )
    print(
      source[
        :5000
      ]
    )
