from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_PATH = ROOT / "toda_group_proof_narrative_renderer.py"
SNAPSHOT_PATH = (
  Path(__file__).resolve().parent
  / "patched_functions_after_apply.py.txt"
)


PROSE_FUNCTION = '''def _phase159_r1_7c_r4_normalize_public_map_property_prose(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  replacements = (
    (
      "は単射である.",
      "は単射.",
    ),
    (
      "は全射である.",
      "は全射.",
    ),
    (
      "は同型写像である.",
      "は同型.",
    ),
    (
      "は同型である.",
      "は同型.",
    ),
    (
      "は零写像である.",
      "は零写像.",
    ),
  )

  normalized = rendered

  for old, new in replacements:
    normalized = normalized.replace(
      old,
      new,
    )

  return normalized


'''


NUMBERED_FUNCTION = '''def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\\n\\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  lines = proof_body.splitlines()

  reference_prefix = re.compile(
    r"^\\[R\\d+\\]より,\\s*"
  )
  connector_prefix = re.compile(
    r"^\\((\\d+)\\),\\s*\\((\\d+)\\)\\s+より,\\s*"
  )
  tag_pattern = re.compile(
    r"\\\\tag\\{(\\d+)\\}"
  )

  def map_property(
    line: str,
    suffix: str,
  ) -> tuple[
    str,
    int | None,
  ] | None:
    stripped = line.strip()
    stripped = reference_prefix.sub(
      "",
      stripped,
    )

    if not stripped.endswith(
      suffix
    ):
      return None

    map_text = stripped[
      :-len(
        suffix
      )
    ].strip()

    tag_match = tag_pattern.search(
      map_text
    )
    tag_number = (
      int(
        tag_match.group(
          1
        )
      )
      if tag_match is not None
      else None
    )
    map_text = tag_pattern.sub(
      "",
      map_text,
    ).strip()

    return (
      map_text,
      tag_number,
    )

  def isomorphism_map(
    line: str,
  ) -> tuple[
    str,
    bool,
  ] | None:
    stripped = line.strip()

    if reference_prefix.match(
      stripped
    ):
      return None

    had_connector = (
      connector_prefix.match(
        stripped
      )
      is not None
    )
    stripped = connector_prefix.sub(
      "",
      stripped,
    )

    for suffix in (
      " は同型.",
      " は同型写像.",
      " は同型である.",
      " は同型写像である.",
    ):
      if stripped.endswith(
        suffix
      ):
        return (
          tag_pattern.sub(
            "",
            stripped[
              :-len(
                suffix
              )
            ].strip(),
          ),
          had_connector,
        )

    return None

  injective_by_map = {}
  surjective_by_map = {}
  isomorphism_by_map = {}

  for index, line in enumerate(
    lines
  ):
    injective = map_property(
      line,
      " は単射.",
    )

    if injective is not None:
      injective_by_map.setdefault(
        injective[0],
        [],
      ).append(
        (
          index,
          injective[1],
        )
      )

    surjective = map_property(
      line,
      " は全射.",
    )

    if surjective is not None:
      surjective_by_map.setdefault(
        surjective[0],
        [],
      ).append(
        (
          index,
          surjective[1],
        )
      )

    isomorphism = isomorphism_map(
      line
    )

    if isomorphism is not None:
      isomorphism_by_map.setdefault(
        isomorphism[0],
        [],
      ).append(
        (
          index,
          isomorphism[1],
        )
      )

  existing_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for line in lines
    for match in tag_pattern.finditer(
      line
    )
  )
  next_number = (
    max(
      existing_numbers,
      default=0,
    )
    + 1
  )

  numbered_map_properties = {}

  for map_text in tuple(
    isomorphism_by_map
  ):
    injective_rows = injective_by_map.get(
      map_text,
      (),
    )
    surjective_rows = surjective_by_map.get(
      map_text,
      (),
    )

    if (
      not injective_rows
      or not surjective_rows
    ):
      continue

    injective_index, injective_number = (
      injective_rows[
        0
      ]
    )
    surjective_index, surjective_number = (
      surjective_rows[
        0
      ]
    )

    if injective_number is None:
      injective_number = next_number
      next_number += 1

    if surjective_number is None:
      surjective_number = next_number
      next_number += 1

    numbered_map_properties[
      injective_index
    ] = (
      map_text,
      "は単射",
      injective_number,
    )
    numbered_map_properties[
      surjective_index
    ] = (
      map_text,
      "は全射",
      surjective_number,
    )

    isomorphism_index, _had_connector = (
      isomorphism_by_map[
        map_text
      ][
        0
      ]
    )
    lines[
      isomorphism_index
    ] = (
      "("
      + str(
        injective_number
      )
      + "), ("
      + str(
        surjective_number
      )
      + ") より, "
      + map_text
      + " は同型."
    )

  output_lines = []

  for index, line in enumerate(
    lines
  ):
    numbered = numbered_map_properties.get(
      index
    )

    if numbered is None:
      output_lines.append(
        line
      )
      continue

    map_text, property_text, number = numbered

    if (
      map_text.startswith(
        "$"
      )
      and map_text.endswith(
        "$"
      )
    ):
      map_text = map_text[
        1:-1
      ]

    output_lines.extend(
      (
        r"\\[",
        (
          map_text
          + r"\\quad\\text{"
          + property_text
          + r"}. \\qquad ("
          + str(
            number
          )
          + ")"
        ),
        r"\\]",
      )
    )

  return (
    prefix
    + "\\n".join(
      output_lines
    )
    + (
      "\\n"
      if rendered.endswith(
        "\\n"
      )
      else ""
    )
  )


'''


def function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )
  matches = tuple(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == function_name
    )
  )

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      f"{function_name}: expected exactly one top-level function, "
      f"found {len(matches)}"
    )

  node = matches[
    0
  ]
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


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  start, end = function_span(
    source,
    function_name,
  )

  return (
    source[:start]
    + replacement
    + source[end:]
  )


def main() -> int:
  source = TARGET_PATH.read_text(
    encoding="utf-8"
  )

  source = replace_function(
    source,
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
    PROSE_FUNCTION,
  )
  source = replace_function(
    source,
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    NUMBERED_FUNCTION,
  )

  TARGET_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  prose_start, prose_end = function_span(
    source,
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
  )
  numbered_start, numbered_end = function_span(
    source,
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
  )

  SNAPSHOT_PATH.write_text(
    source[
      prose_start:prose_end
    ]
    + "\n\n"
    + source[
      numbered_start:numbered_end
    ],
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 repair2g fix10i applied."
  )
  print(
    "Changed file: toda_group_proof_narrative_renderer.py"
  )
  print(
    "Changed function: "
    "_phase159_r1_7c_r4_normalize_public_map_property_prose"
  )
  print(
    "Changed function: "
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning"
  )
  print(
    "Full changed functions written to:"
  )
  print(
    SNAPSHOT_PATH
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
