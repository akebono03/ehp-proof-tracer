from __future__ import annotations

import ast
import shutil
from pathlib import Path


RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)
NUMBERED_TEST = Path(
  "tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_numbered_exactness_prefix_repair22_backup"
)


NEW_HELPER = r"""def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
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
    r"^\[R\d+\]\s*より,\s*"
  )
  exactness_prefix = re.compile(
    r"^完全性より,\s*"
  )
  connector_prefix = re.compile(
    r"^\((\d+)\),\s*\((\d+)\)\s+より,\s*"
  )
  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
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
    stripped = exactness_prefix.sub(
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
        r"\[",
        (
          map_text
          + r"\quad\text{"
          + property_text
          + r"}. \qquad ("
          + str(
            number
          )
          + ")"
        ),
        r"\]",
      )
    )

  return (
    prefix
    + "\n".join(
      output_lines
    )
    + (
      "\n"
      if rendered.endswith(
        "\n"
      )
      else ""
    )
  )
"""


NEW_PI11_TEST = r"""def test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )
  assert (
    r"(1), (2) より, "
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型写像である."
    not in rendered
  )
"""


NEW_PI3_TEST = r"""def test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning():
  rendered = _public_narrative(
    2,
    1,
  )

  assert (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )
  assert (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    in rendered
  )
"""


NEW_GENERAL_TEST = r"""def test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded():
  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  )

  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "---\n\n"
    "## 証明\n\n"
    "完全性より, $F: A \\to B$ は単射.\n"
    "完全性より, $F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型写像である.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert (
    "\\[\n"
    r"F: A \to B"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in normalized
  )
  assert (
    "\\[\n"
    r"F: A \to B"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in normalized
  )
  assert (
    r"(1), (2) より, $F: A \to B$ は同型."
    in normalized
  )
"""


def replace_top_level_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  target = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  lines = source.splitlines(
    keepends=True
  )
  newline = (
    "\r\n"
    if "\r\n" in source
    else "\n"
  )

  return (
    "".join(
      lines[
        :target.lineno - 1
      ]
    )
    + replacement.strip(
      "\n"
    ).replace(
      "\n",
      newline,
    )
    + newline
    + "".join(
      lines[
        target.end_lineno:
      ]
    )
  )


def backup(
  path: Path,
) -> None:
  destination = (
    BACKUP_DIR
    / path
  )
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


def main() -> None:
  for path in (
    RENDERER,
    NUMBERED_TEST,
  ):
    if not path.exists():
      raise FileNotFoundError(
        "Run from repository root; missing: "
        + str(
          path
        )
      )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for path in (
    RENDERER,
    NUMBERED_TEST,
  ):
    backup(
      path
    )

  renderer_source = RENDERER.read_text(
    encoding="utf-8"
  )
  test_source = NUMBERED_TEST.read_text(
    encoding="utf-8"
  )

  renderer_updated = (
    replace_top_level_function(
      renderer_source,
      "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
      NEW_HELPER,
    )
  )

  test_updated = (
    replace_top_level_function(
      test_source,
      "test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning",
      NEW_PI11_TEST,
    )
  )
  test_updated = (
    replace_top_level_function(
      test_updated,
      "test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning",
      NEW_PI3_TEST,
    )
  )
  test_updated = (
    replace_top_level_function(
      test_updated,
      "test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded",
      NEW_GENERAL_TEST,
    )
  )

  ast.parse(
    renderer_updated
  )
  ast.parse(
    test_updated
  )

  RENDERER.write_text(
    renderer_updated,
    encoding="utf-8",
  )
  NUMBERED_TEST.write_text(
    test_updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 numbered exactness-prefix repair22."
  )
  print(
    "Numbered reasoning now normalizes exactness-prefixed "
    "injective/surjective statements."
  )
  print(
    "Stale inline-tag expectations updated to current centered contract."
  )


if __name__ == "__main__":
  main()
