def suppress_toda_group_proof_narrative_dangling_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  def numbered_connector_numbers(
    line: str,
  ) -> tuple[
    int,
    ...,
  ] | None:
    stripped = line.strip()

    if (
      not stripped.startswith(
        "("
      )
      or not stripped.endswith(
        "より,"
      )
      or "$" in stripped
      or "[R" in stripped
    ):
      return None

    relation_text = stripped[
      : -len(
        "より,"
      )
    ].strip()
    parts = tuple(
      part.strip()
      for part in relation_text.split(
        " と "
      )
    )

    if not parts:
      return None

    numbers = []

    for part in parts:
      if (
        len(
          part
        ) < 3
        or not part.startswith(
          "("
        )
        or not part.endswith(
          ")"
        )
      ):
        return None

      number_text = part[
        1:-1
      ]

      if not number_text.isdigit():
        return None

      numbers.append(
        int(
          number_text
        )
      )

    return tuple(
      numbers
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  retained_paragraphs = []

  for paragraph_index, paragraph in enumerate(
    paragraphs
  ):
    lines = paragraph.splitlines()

    while lines:
      stripped = lines[
        -1
      ].strip()

      if stripped in standalone_connectors:
        lines.pop()
        continue

      connector_numbers = (
        numbered_connector_numbers(
          stripped
        )
      )

      if connector_numbers is None:
        break

      previous_text = "\n\n".join(
        paragraphs[
          :paragraph_index
        ]
      )
      referenced_tags_exist = all(
        (
          r"\tag{"
          + str(
            number
          )
          + "}"
        )
        in previous_text
        for number in connector_numbers
      )

      next_paragraph = next(
        (
          candidate.strip()
          for candidate in paragraphs[
            paragraph_index + 1:
          ]
          if candidate.strip()
        ),
        "",
      )
      has_following_derivation = (
        "$" in next_paragraph
      )

      if (
        referenced_tags_exist
        and has_following_derivation
      ):
        break

      lines.pop()

    if not lines:
      continue

    normalized = "\n".join(
      lines
    )
    stripped = normalized.lstrip()

    for connector in standalone_connectors:
      prefix = (
        connector
        + " "
      )

      if (
        stripped.startswith(
          prefix
          + "[R"
        )
      ):
        leading = len(
          normalized
        ) - len(
          stripped
        )
        normalized = (
          normalized[
            :leading
          ]
          + stripped[
            len(
              prefix
            ):
          ]
        )
        break

    if normalized.strip():
      retained_paragraphs.append(
        normalized
      )

  # An exactness introduction must introduce a displayed EHP sequence,
  # not a repeated introduction or a calculation on another subject.
  # Keep the mathematical proof steps; remove only orphaned prose.
  cleaned_paragraphs = []
  for index, paragraph in enumerate(
    retained_paragraphs
  ):
    if paragraph.strip() == "次の完全列を考える.":
      following = next(
        (
          candidate.strip()
          for candidate in retained_paragraphs[
            index + 1:
          ]
          if candidate.strip()
        ),
        "",
      )
      is_exactness_display = (
        (
          following.startswith(r"\[")
          or following.startswith("$")
        )
        and (
          r"\xrightarrow{" in following
          or r"\longrightarrow" in following
        )
      )
      if not is_exactness_display:
        continue
    cleaned_paragraphs.append(paragraph)

  return "\n\n".join(cleaned_paragraphs)
