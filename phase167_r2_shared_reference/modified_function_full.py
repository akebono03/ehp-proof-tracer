def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
  statement_lines_by_reference_number: (
    dict[
      int,
      tuple[
        str,
        ...,
      ],
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if (
    statement_lines_by_reference_number is not None
    and not isinstance(
      statement_lines_by_reference_number,
      dict,
    )
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be "
      "a dict or None"
    )

  if statement_lines_by_reference_number is not None:
    for reference_number, statement_lines in (
      statement_lines_by_reference_number.items()
    ):
      if (
        isinstance(
          reference_number,
          bool,
        )
        or not isinstance(
          reference_number,
          int,
        )
      ):
        raise TypeError(
          "statement_lines_by_reference_number keys "
          "must be integers"
        )

      if not isinstance(
        statement_lines,
        tuple,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must be tuples"
        )

      if not all(
        isinstance(
          line,
          str,
        )
        for line in statement_lines
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

  if not entries:
    return ""

  lines = []

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )

    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

    if entry.reference.locator == "Proposition 4.2":
      lines.append(
        r"$\cdots \to \pi_{i-1}^{n} \xrightarrow{E} "
        r"\pi_{i}^{n+1} \xrightarrow{H} "
        r"\pi_{i}^{2n+1} \xrightarrow{\Delta} "
        r"\pi_{i-2}^{n} \xrightarrow{E} "
        r"\pi_{i-1}^{n+1} \to \cdots$ は完全である."
      )
      continue

    statement_lines = (
      ()
      if statement_lines_by_reference_number is None
      else statement_lines_by_reference_number.get(
        entry.number,
        (),
      )
    )

    # Typed universal connectivity assertion: render its general mathematical
    # statement through the same statement_lines pipeline as every reference.
    # The decision is based on the proven GIVEN statement, never on locator text.
    additional_lines = []
    for proof_step in entry.proof_steps:
      if (
        type(proof_step.conclusion).__name__ == "Toda51BelowDiagonalZeroStatement"
        and not proof_step.premises
        and getattr(proof_step.rule, "name", None) == "GIVEN"
      ):
        additional_lines.append(r"$\pi_{i}^{n} = 0\ (i < n)$")
    statement_lines = tuple(dict.fromkeys(
      (*statement_lines, *additional_lines)
    ))

    for statement_line in statement_lines:
      # A catalog range belongs to its general formula, not to an
      # unrelated specialization or another component of the same theorem.
      applicable_ranges = []
      fixed_keys = set()
      for proof_step in entry.proof_steps:
        boundary = classify_toda_literature_statement_step(proof_step)
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator == entry.reference.locator
          and boundary.component_key is not None
        ):
          fixed_keys.add(boundary.component_key)

      for component in get_toda_fixed_statement_components(
        entry.reference.locator
      ):
        if component.range_text is None:
          continue
        range_variable = component.range_text.split()[0]
        # Symbolic indices are required in the displayed formula.
        if re.search(
          r"(?<![A-Za-z])" + re.escape(range_variable) + r"(?![A-Za-z])",
          statement_line,
        ) is None:
          continue
        # Explicit component matches are preferred; aggregate carriers
        # can use the unique matching symbolic statement component.
        if fixed_keys and component.component_key not in fixed_keys:
          continue
        rendered_range = (
          component.range_text.replace(">=", r"\ge")
          .replace("<=", r"\le")
        )
        if rendered_range not in applicable_ranges:
          applicable_ranges.append(rendered_range)

      if len(applicable_ranges) == 1 and statement_line.startswith("$"):
        range_suffix = r"$\;(" + applicable_ranges[0].strip() + ")$"
        if range_suffix not in statement_line:
          if statement_line.endswith("."):
            statement_line = statement_line[:-1] + " " + range_suffix + "."
          else:
            statement_line += " " + range_suffix
      lines.append(statement_line)

  return "\n".join(lines)
