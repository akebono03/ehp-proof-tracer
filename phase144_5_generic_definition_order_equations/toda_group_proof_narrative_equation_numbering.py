import re


_STANDALONE_MATH_PATTERN = re.compile(
  r"^\$(?P<latex>.+)\$(?P<suffix>.*)$"
)


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
  numbered_lines = []
  equation_number = 0

  for line in lines:
    match = _STANDALONE_MATH_PATTERN.match(
      line
    )

    if match is None:
      numbered_lines.append(
        line
      )
      continue

    latex = match.group(
      "latex"
    )
    suffix = match.group(
      "suffix"
    )

    if r"\tag{" in latex:
      numbered_lines.append(
        line
      )
      continue

    equation_number += 1
    numbered_lines.append(
      "$"
      + latex
      + r"\tag{"
      + str(
        equation_number
      )
      + "}$"
      + suffix
    )

  return "\n".join(
    numbered_lines
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
