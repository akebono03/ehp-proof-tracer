from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path


RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)
LOCALITY_TEST = Path(
  "tests/test_phase159_pi3_2_public_definition_premise_locality.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_repair18_numbered_locality_repair23_backup"
)


NEW_ORDERING_HELPER = r"""def _phase159_order_public_unique_preimage_definition_premises(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

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
  had_trailing_newline = rendered.endswith(
    "\n"
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if (
      stripped.startswith(
        r"\["
      )
      and stripped.endswith(
        r"\]"
      )
    ):
      display_lines = tuple(
        line.strip()
        for line in stripped.splitlines()
        if line.strip()
      )

      if len(
        display_lines
      ) == 3:
        display_body = display_lines[
          1
        ]
        display_match = re.fullmatch(
          (
            r"(?P<map>.+?)"
            r"\\quad\\text\{"
            r"(?P<property>は単射|は全射)"
            r"\}\.\s*"
            r"\\qquad\s*"
            r"\((?P<number>\d+)\)"
          ),
          display_body,
        )

        if display_match is not None:
          stripped = (
            "$"
            + display_match.group(
              "map"
            )
            + "$ "
            + display_match.group(
              "property"
            )
            + "."
          )

    numbered_connector = re.compile(
      (
        r"^(?:\(\d+\)"
        r"(?:,\s*|\s+と\s+)?)"
        r"+\s*より,\s*"
      )
    )
    stripped = numbered_connector.sub(
      "",
      stripped,
    )

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ].lstrip()

        for reference_prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            reference_prefix
          ):
            stripped = suffix[
              len(
                reference_prefix
              ):
            ]
            break

    for prose_prefix in (
      "完全性より, ",
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
    ):
      if stripped.startswith(
        prose_prefix
      ):
        stripped = stripped[
          len(
            prose_prefix
          ):
        ]
        break

    for verbose, concise in (
      (
        " は単射である.",
        " は単射.",
      ),
      (
        " は全射である.",
        " は全射.",
      ),
      (
        " は零写像である.",
        " は零写像.",
      ),
      (
        " は同型写像である.",
        " は同型.",
      ),
    ):
      if stripped.endswith(
        verbose
      ):
        stripped = (
          stripped[
            :-len(
              verbose
            )
          ]
          + concise
        )
        break

    return stripped.rstrip(
      ".,"
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    line = _render_generic_narrative_step(
      proof_step
    )

    if not line:
      return None

    target_key = match_key(
      line
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  for node in presentation.nodes:
    proof_step = node.proof_step
    definition_line = (
      _phase159_unique_preimage_definition_line(
        proof_step
      )
    )

    if definition_line is None:
      continue

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    visible_premise_records = tuple(
      (
        premise_step,
        paragraph_index_for_step(
          premise_step
        ),
      )
      for premise_step in proof_step.premises
    )

    if any(
      premise_index is None
      for (
        _,
        premise_index,
      ) in visible_premise_records
    ):
      continue

    premise_indices = tuple(
      premise_index
      for (
        _,
        premise_index,
      ) in visible_premise_records
      if premise_index is not None
    )

    if len(
      premise_indices
    ) != len(
      proof_step.premises
    ):
      continue

    definition_index = definition_matches[
      0
    ]
    expected_indices = tuple(
      range(
        definition_index
        - len(
          premise_indices
        ),
        definition_index,
      )
    )

    if premise_indices == expected_indices:
      continue

    premise_paragraphs = tuple(
      paragraphs[
        premise_index
      ]
      for premise_index in premise_indices
    )

    for premise_index in sorted(
      premise_indices,
      reverse=True,
    ):
      paragraphs.pop(
        premise_index
      )

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    definition_index = definition_matches[
      0
    ]
    paragraphs[
      definition_index:
      definition_index
    ] = premise_paragraphs

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result
"""


TEST_CONSTANTS = {
  "H_INJECTIVE": (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
  ),
  "E_ISOMORPHISM": (
    r"$E(\iota_{1}) = \iota_{2}$ であるから, "
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型."
  ),
  "H_SURJECTIVE": (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
  ),
  "H_ISOMORPHISM": (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  ),
}


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


def replace_module_constant(
  source: str,
  name: str,
  value: str,
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
          ast.Assign,
        )
        and len(
          node.targets
        ) == 1
        and isinstance(
          node.targets[
            0
          ],
          ast.Name,
        )
        and node.targets[
          0
        ].id
        == name
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      "test constant not found: "
      + name
    )

  lines = source.splitlines(
    keepends=True
  )
  newline = (
    "\r\n"
    if "\r\n" in source
    else "\n"
  )
  literal = (
    name
    + " = "
    + repr(
      value
    )
    + newline
  )

  return (
    "".join(
      lines[
        :target.lineno - 1
      ]
    )
    + literal
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
    LOCALITY_TEST,
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
    LOCALITY_TEST,
  ):
    backup(
      path
    )

  renderer_source = RENDERER.read_text(
    encoding="utf-8"
  )
  test_source = LOCALITY_TEST.read_text(
    encoding="utf-8"
  )

  renderer_updated = (
    replace_top_level_function(
      renderer_source,
      "_phase159_order_public_unique_preimage_definition_premises",
      NEW_ORDERING_HELPER,
    )
  )

  test_updated = test_source

  for name, value in TEST_CONSTANTS.items():
    test_updated = (
      replace_module_constant(
        test_updated,
        name,
        value,
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
  LOCALITY_TEST.write_text(
    test_updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 repair18 numbered-locality repair23."
  )
  print(
    "repair18 ordering now recognizes centered numbered "
    "map-property paragraphs and numbered conclusions."
  )
  print(
    "repair18 locality constants updated to the current "
    "Phase 159 display contract."
  )


if __name__ == "__main__":
  main()
