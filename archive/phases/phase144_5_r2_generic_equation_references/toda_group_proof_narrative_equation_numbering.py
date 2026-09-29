import re


_STANDALONE_MATH_PATTERN = re.compile(
  r"^\$(?P<latex>.+)\$(?P<suffix>.*)$"
)
_TAG_PATTERN = re.compile(
  r"\\tag\{(?P<number>\d+)\}"
)


def toda_group_proof_narrative_equation_reference(
  equation_number: int,
) -> str:
  if (
    not isinstance(
      equation_number,
      int,
    )
    or isinstance(
      equation_number,
      bool,
    )
    or equation_number <= 0
  ):
    raise ValueError(
      "equation_number must be a positive integer"
    )

  return (
    "("
    + str(
      equation_number
    )
    + ")"
  )


def _previous_calculation_source_line_indices(
  lines: list[str],
  connector_index: int,
) -> tuple[int, ...]:
  source_indices = []
  index = connector_index - 1

  while index >= 0:
    line = lines[
      index
    ]

    if not line:
      index -= 1
      continue

    if (
      _STANDALONE_MATH_PATTERN.match(
        line
      )
      is None
    ):
      break

    source_indices.append(
      index
    )
    index -= 1

  source_indices.reverse()

  return tuple(
    source_indices
  )


def _next_calculation_target_line_index(
  lines: list[str],
  connector_index: int,
) -> int | None:
  for index in range(
    connector_index + 1,
    len(
      lines
    ),
  ):
    line = lines[
      index
    ]

    if not line:
      continue

    if (
      _STANDALONE_MATH_PATTERN.match(
        line
      )
      is not None
    ):
      return index

    return None

  return None


def number_toda_group_proof_narrative_equations(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a string"
    )

  lines = markdown.splitlines()
  reference_groups = []
  numbered_line_indices = set()

  for connector_index, line in enumerate(
    lines
  ):
    if line != "これらより、":
      continue

    source_indices = (
      _previous_calculation_source_line_indices(
        lines,
        connector_index,
      )
    )
    target_index = (
      _next_calculation_target_line_index(
        lines,
        connector_index,
      )
    )

    if (
      not source_indices
      or target_index is None
    ):
      continue

    reference_groups.append(
      (
        connector_index,
        source_indices,
      )
    )
    numbered_line_indices.update(
      source_indices
    )
    numbered_line_indices.add(
      target_index
    )

  equation_number_by_line_index = {}
  next_equation_number = 1

  for line_index in sorted(
    numbered_line_indices
  ):
    line = lines[
      line_index
    ]
    match = _STANDALONE_MATH_PATTERN.match(
      line
    )

    if match is None:
      continue

    existing_tag = _TAG_PATTERN.search(
      match.group(
        "latex"
      )
    )

    if existing_tag is not None:
      equation_number_by_line_index[
        line_index
      ] = int(
        existing_tag.group(
          "number"
        )
      )
      continue

    equation_number_by_line_index[
      line_index
    ] = next_equation_number
    next_equation_number += 1

    lines[
      line_index
    ] = (
      "$"
      + match.group(
        "latex"
      )
      + r"\tag{"
      + str(
        equation_number_by_line_index[
          line_index
        ]
      )
      + "}$"
      + match.group(
        "suffix"
      )
    )

  for (
    connector_index,
    source_indices,
  ) in reference_groups:
    references = tuple(
      toda_group_proof_narrative_equation_reference(
        equation_number_by_line_index[
          source_index
        ]
      )
      for source_index in source_indices
      if (
        source_index
        in equation_number_by_line_index
      )
    )

    if not references:
      continue

    if len(
      references
    ) == 1:
      reference_text = references[
        0
      ]
    else:
      reference_text = (
        ", ".join(
          references[
            :-1
          ]
        )
        + " と "
        + references[
          -1
        ]
      )

    lines[
      connector_index
    ] = (
      reference_text
      + " より、"
    )

  return "\n".join(
    lines
  )
