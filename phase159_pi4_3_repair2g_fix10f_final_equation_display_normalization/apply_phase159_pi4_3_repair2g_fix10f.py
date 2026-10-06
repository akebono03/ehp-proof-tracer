from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTION_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
RENDERER_PATH = (
  ROOT
  / "toda_group_proof_narrative_renderer.py"
)
SNAPSHOT_PATH = (
  Path(__file__).resolve().parent
  / "patched_functions_after_apply.py.txt"
)


FINAL_NORMALIZER = '''def _phase158_normalize_public_equation_numbers(
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  connector_numbers_by_index = {}
  referenced_numbers = set()

  for index, line in enumerate(
    proof_body
  ):
    numbers = (
      _phase158_public_equation_connector_numbers(
        line
      )
    )

    if numbers is None:
      continue

    connector_numbers_by_index[
      index
    ] = numbers
    referenced_numbers.update(
      numbers
    )

  derivation_target_numbers = set()

  for connector_index in connector_numbers_by_index:
    target_index = next(
      (
        index
        for index in range(
          connector_index + 1,
          len(
            proof_body
          ),
        )
        if proof_body[
          index
        ].strip()
      ),
      None,
    )

    if target_index is None:
      continue

    target_number = (
      _phase158_public_equation_tag_number(
        proof_body[
          target_index
        ]
      )
    )

    if target_number is not None:
      derivation_target_numbers.add(
        target_number
      )

  retained_numbers = (
    referenced_numbers
    | derivation_target_numbers
  )
  retained_old_numbers = []
  seen_old_numbers = set()

  for line in proof_body:
    number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if (
      number is None
      or number not in retained_numbers
      or number in seen_old_numbers
    ):
      continue

    retained_old_numbers.append(
      number
    )
    seen_old_numbers.add(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      retained_old_numbers,
      start=1,
    )
  }

  result = []
  emitted_old_numbers = set()

  for index, source_line in enumerate(
    proof_body
  ):
    line = source_line
    tag_number = (
      _phase158_public_equation_tag_number(
        line
      )
    )
    public_number = None

    if tag_number is not None:
      old_marker = (
        r"\tag{"
        + str(
          tag_number
        )
        + "}"
      )

      if (
        tag_number not in number_map
        or tag_number in emitted_old_numbers
      ):
        line = line.replace(
          old_marker,
          "",
          1,
        )
      else:
        public_number = number_map[
          tag_number
        ]
        line = line.replace(
          old_marker,
          "",
          1,
        )
        emitted_old_numbers.add(
          tag_number
        )

    connector_numbers = (
      connector_numbers_by_index.get(
        index
      )
    )

    if connector_numbers is not None:
      if all(
        number in number_map
        for number in connector_numbers
      ):
        line = (
          _phase158_render_public_equation_connector(
            tuple(
              number_map[
                number
              ]
              for number in connector_numbers
            )
          )
        )
      else:
        line = (
          "これより,"
          if len(
            connector_numbers
          ) == 1
          else "これらより,"
        )

    line = line.replace(
      "は零写像である.",
      "は零写像.",
    )

    numbered_map_properties = (
      (
        " は単射.",
        "は単射",
      ),
      (
        " は全射.",
        "は全射",
      ),
      (
        " は同型.",
        "は同型",
      ),
    )

    normalized_map_property = False

    if public_number is not None:
      stripped = line.strip()

      for suffix, property_text in numbered_map_properties:
        if (
          not stripped.startswith(
            "$"
          )
          or not stripped.endswith(
            suffix
          )
        ):
          continue

        math_and_suffix = stripped[
          : -len(
            suffix
          )
        ]

        if not math_and_suffix.endswith(
          "$"
        ):
          continue

        math_content = math_and_suffix[
          1:-1
        ].rstrip()

        result.extend(
          (
            r"\[",
            (
              math_content
              + r"\quad\text{"
              + property_text
              + r"}. \qquad ("
              + str(
                public_number
              )
              + ")"
            ),
            r"\]",
          )
        )
        normalized_map_property = True
        break

    if normalized_map_property:
      continue

    result.append(
      line
    )

  return result


'''


def function_span_from_ast(
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


def remove_fix10e_contribution_normalizer(
) -> str:
  source = CONTRIBUTION_PATH.read_text(
    encoding="utf-8"
  )
  helper_name = (
    "normalize_toda_group_proof_narrative_"
    "numbered_map_property_display"
  )

  if (
    "def "
    + helper_name
    + "("
    in source
  ):
    start, end = function_span_from_ast(
      source,
      helper_name,
    )
    source = (
      source[:start]
      + source[end:]
    )

  renderer_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  start, end = function_span_from_ast(
    source,
    renderer_name,
  )
  renderer_source = source[
    start:end
  ]

  call_block = (
    "  rendered = (\n"
    "    normalize_toda_group_proof_narrative_"
    "numbered_map_property_display(\n"
    "      rendered\n"
    "    )\n"
    "  )\n"
    "\n"
  )

  renderer_source = renderer_source.replace(
    call_block,
    "",
  )

  if helper_name in renderer_source:
    raise RuntimeError(
      "fix10e helper reference remains in contribution renderer"
    )

  source = (
    source[:start]
    + renderer_source
    + source[end:]
  )

  CONTRIBUTION_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  return renderer_source


def replace_final_normalizer(
) -> str:
  source = RENDERER_PATH.read_text(
    encoding="utf-8"
  )
  function_name = (
    "_phase158_normalize_public_equation_numbers"
  )
  start, end = function_span_from_ast(
    source,
    function_name,
  )

  source = (
    source[:start]
    + FINAL_NORMALIZER
    + source[end:]
  )

  RENDERER_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  return FINAL_NORMALIZER


def main() -> int:
  contribution_renderer = (
    remove_fix10e_contribution_normalizer()
  )
  final_normalizer = replace_final_normalizer()

  SNAPSHOT_PATH.write_text(
    (
      "# toda_group_proof_narrative_renderer.py\n\n"
      + final_normalizer
      + "\n"
      + "# toda_group_proof_narrative_contribution_renderer.py\n\n"
      + contribution_renderer
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 repair2g fix10f applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_renderer.py"
  )
  print(
    "Changed function: "
    "_phase158_normalize_public_equation_numbers"
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Removed ineffective fix10e helper and call."
  )
  print(
    "Numbered map-property formatting now occurs "
    "after final equation-number selection."
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
