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

    # Normalize cited fixed-statement components to their registered general
    # form rather than printing selected specialized proof conclusions.
    # This is shared logic: no branch on the literature locator or target group.
    general_formula_by_component = {
      "circle_higher_homotopy_zero": r"\pi_{i}^{1} = 0",
      "sphere_connectivity_zero": r"\pi_{i}^{n} = 0",
      "diagonal_identity_group": r"\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}",
    }
    registered_components = {
      component.component_key: component
      for component in get_toda_fixed_statement_components(
        entry.reference.locator
      )
    }
    identified_components = set()
    for proof_step in entry.proof_steps:
      boundary = classify_toda_literature_statement_step(proof_step)
      if (
        boundary is not None
        and boundary.classification
        == TodaLiteratureStatementClassification.FIXED_STATEMENT
        and boundary.reference_locator == entry.reference.locator
        and boundary.component_key in registered_components
      ):
        identified_components.add(boundary.component_key)
      conclusion = proof_step.conclusion
      if type(conclusion).__name__ == "Toda51BelowDiagonalZeroStatement":
        identified_components.add("sphere_connectivity_zero")
      elif type(conclusion).__name__ == "TodaPrimaryGroupZeroStatement":
        group = getattr(conclusion, "group", None)
        if group is None:
          group = getattr(conclusion, "target_group", None)
        if (
          getattr(group, "sphere_dimension", None) == 1
          and isinstance(getattr(group, "group_dimension", None), int)
          and group.group_dimension > 1
        ):
          identified_components.add("circle_higher_homotopy_zero")
      elif type(conclusion).__name__ == "Relation":
        lhs = getattr(conclusion, "lhs", None)
        rhs = getattr(conclusion, "rhs", None)
        dimension = getattr(lhs, "group_dimension", None)
        if (
          dimension is not None
          and dimension == getattr(lhs, "sphere_dimension", None)
          and type(rhs).__name__ == "FreeCyclicGroup"
        ):
          identified_components.add("diagonal_identity_group")

    general_keys = (
      identified_components
      & registered_components.keys()
      & general_formula_by_component.keys()
    )
    if general_keys:
      normalized_lines = []
      for component_key in registered_components:
        if component_key not in general_keys:
          continue
        component = registered_components[component_key]
        formula = general_formula_by_component[component_key]
        range_text = component.range_text
        if range_text and component.range_is_explicit_in_current_aggregate:
          range_latex = (
            range_text.replace(">=", r"\ge")
            .replace("<=", r"\le")
            .replace(">", ">")
            .replace("<", "<")
          )
          formula += r"\quad(" + range_latex + ")"
        normalized_lines.append("$" + formula + "$.")
      # Fixed components must be shown in general form, not as an arbitrary
      # subset of specialized equations from the current proof.
      statement_lines = tuple(normalized_lines)

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
        # An already embedded condition, e.g. \\quad(n \\ge 1),
        # must not be appended a second time as separate inline math.
        existing_condition = "(" + applicable_ranges[0].strip() + ")"
        if (
          range_suffix not in statement_line
          and existing_condition not in statement_line
        ):
          if statement_line.endswith("."):
            statement_line = statement_line[:-1] + " " + range_suffix + "."
          else:
            statement_line += " " + range_suffix
      lines.append(statement_line)

  return "\n".join(lines)
