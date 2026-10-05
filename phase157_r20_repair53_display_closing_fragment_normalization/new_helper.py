def _normalize_toda_group_proof_narrative_display_closing_fragments(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.splitlines()
  normalized = []
  closing_fragments = {
    "である.",
    "を得る.",
    "を用いる.",
    "となる.",
  }

  for line in lines:
    stripped = line.strip()

    if (
      stripped
      in closing_fragments
      and normalized
    ):
      previous_index = (
        len(
          normalized
        )
        - 1
      )

      while (
        previous_index >= 0
        and not normalized[
          previous_index
        ].strip()
      ):
        previous_index -= 1

      if (
        previous_index >= 0
        and normalized[
          previous_index
        ].strip()
        == r"\]"
      ):
        del normalized[
          previous_index + 1:
        ]

    normalized.append(
      line
    )

  return "\n".join(
    normalized
  )
