def link_toda_group_proof_narrative_reference_body_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  source_steps_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      reference_entries,
    )
  )
  lines = body_markdown.splitlines()

  # Connect already-derived, single-premise proof steps to their cited
  # literature premises. Do not repeat specialization or inspect rule names.
  from proof import ProofRule

  for reference_number, source_steps in source_steps_by_number.items():
    marker = "[R" + str(reference_number) + "]"
    source_ids = {
      id(step)
      for step in source_steps
      if step.rule is ProofRule.GIVEN
    }
    consumers = []
    for edge in presentation.edges:
      if id(edge.premise_step) not in source_ids:
        continue
      derived_step = edge.parent_step
      if derived_step.rule is not ProofRule.INFERENCE:
        continue
      if (
        len(derived_step.premises) != 1
        or derived_step.premises[0] is not edge.premise_step
      ):
        continue
      derived_line = _render_generic_narrative_step(derived_step)
      if not derived_line:
        continue
      candidates = tuple(
        i for i, line in enumerate(lines)
        if line.strip().rstrip(".。") in (
          derived_line.strip().rstrip(".。"),
          "これより, " + derived_line.strip().rstrip(".。"),
          "これより、" + derived_line.strip().rstrip(".。"),
        )
      )
      if len(candidates) == 1:
        consumers.append((candidates[0], derived_line.strip()))
    consumers = list(dict.fromkeys(consumers))
    if not consumers:
      continue
    source_formulas = {
      _render_generic_narrative_step(step).strip().rstrip(".。")
      for step in source_steps
      if _render_generic_narrative_step(step)
    }
    # One literature reference may have several independent specializations.
    # Remove a displayed general form, if present, without discarding any
    # of its concrete consequences.
    for old_index in range(len(lines) - 1, -1, -1):
      stripped = lines[old_index].strip().rstrip(".。")
      if any(
        stripped == marker + "より, " + formula
        or stripped == marker + "より、" + formula
        for formula in source_formulas
      ):
        del lines[old_index]
        consumers = [
          (index - (1 if old_index < index else 0), rendered)
          for index, rendered in consumers
          if index != old_index
        ]
    # Never attach two different source references to the same visible line.
    # Preserve already-cited lines and keep the complete concrete result.
    for index, derived_line in consumers:
      existing = lines[index].strip()
      if existing.startswith("[R"):
        continue
      lines[index] = marker + "より, " + derived_line.rstrip(".。") + "."
  for reference_number, source_steps in (
    source_steps_by_number.items()
  ):
    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    marker_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if marker in line
    )

    if len(
      marker_indices
    ) != 1:
      continue

    marker_index = marker_indices[
      0
    ]
    marker_line = lines[
      marker_index
    ]

    current_body = "\n".join(
      lines
    )
    consumer_line = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        source_steps,
        current_body,
      )
    )

    if consumer_line is None:
      continue

    consumer_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        index != marker_index
        and consumer_line in line
      )
    )

    if len(
      consumer_indices
    ) != 1:
      continue

    consumer_index = consumer_indices[
      0
    ]

    # A reference marker may be moved only onto an unadorned
    # conclusion.  The substring match above can find a conclusion
    # embedded in an independently derived explanation; replacing
    # that paragraph would discard its mathematical justification.
    if lines[consumer_index].strip() != consumer_line.strip():
      continue

    legacy_marker_only = (
      marker_line
      .rstrip()
      .endswith(
        marker
        + "を用いる。"
      )
    )

    rendered_source_lines = tuple(
      rendered
      for source_step in source_steps
      for rendered in (
        _render_generic_narrative_step(
          source_step
        ),
      )
      if rendered
    )

    self_reference_marker = (
      not legacy_marker_only
      and any(
        rendered_source in marker_line
        for rendered_source in rendered_source_lines
      )
      and consumer_line not in marker_line
    )

    if legacy_marker_only:
      if consumer_index <= marker_index:
        continue

      lines[
        marker_index
      ] = (
        marker
        + "より, "
        + consumer_line
      )
      del lines[
        consumer_index
      ]
      continue

    if not self_reference_marker:
      continue

    if consumer_index < marker_index:
      lines[
        consumer_index
      ] = (
        marker
        + "より, "
        + consumer_line
      )
      del lines[
        marker_index
      ]
      continue

    lines[
      marker_index
    ] = (
      marker
      + "より, "
      + consumer_line
    )
    del lines[
      consumer_index
    ]

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  # A cited exactness subwindow is redundant after the longer EHP
  # sequence has already been displayed in the same proof body.
  # Keep the reference marker by attaching it to the original
  # introduction rather than treating exactness as a new conclusion.
  for index in range(len(compacted_lines) - 1, -1, -1):
    line = compacted_lines[index].strip()
    match = re.match(
      r"^\[R([0-9]+)\]より,\s*\$(.+?)\$\s*は完全である[.。]?$",
      line,
    )
    if match is None:
      continue

    reference_number, subwindow = match.groups()
    normalized_subwindow = re.sub(
      r"\s+", "", subwindow.replace(r"\Delta", "Δ")
    )
    earlier_sequence_indices = []
    for earlier_index, earlier_line in enumerate(compacted_lines[:index]):
      if earlier_line.strip().startswith("[R"):
        continue
      earlier_math = re.search(r"\$(.+?)\$", earlier_line)
      if earlier_math is None:
        continue
      earlier_core = re.sub(
        r"\s+", "",
        earlier_math.group(1).replace(r"\Delta", "Δ"),
      )
      if (
        normalized_subwindow in earlier_core
        and normalized_subwindow != earlier_core
        and earlier_core.count(r"\xrightarrow{")
        > normalized_subwindow.count(r"\xrightarrow{")
      ):
        earlier_sequence_indices.append(earlier_index)

    if len(earlier_sequence_indices) != 1:
      continue

    introduction_indices = [
      previous_index
      for previous_index in range(earlier_sequence_indices[0])
      if "次の完全列を考える" in compacted_lines[previous_index]
    ]
    if len(introduction_indices) != 1:
      continue

    intro_index = introduction_indices[0]
    marker = "[R" + reference_number + "]"
    if marker not in compacted_lines[intro_index]:
      compacted_lines[intro_index] = (
        marker + "を用いて, " + compacted_lines[intro_index]
      )
    del compacted_lines[index]

  return "\n".join(
    compacted_lines
  ).strip()
