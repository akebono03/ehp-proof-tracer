def test_phase161_r4_r5_repair13_reference_selection_binds_prop51_component_source():
  _, presentation = (
    _phase161_r4_r5_repair13_data()
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )

  normalized_entries, statement_lines = (
    _select_toda_group_proof_narrative_reference_entries_and_statement_lines(
      presentation,
      entries,
    )
  )

  prop51_entries = tuple(
    entry
    for entry in normalized_entries
    if entry.reference.locator
    == "Proposition 5.1"
  )

  assert len(
    prop51_entries
  ) == 1

  prop51_entry = prop51_entries[
    0
  ]

  rule_names = tuple(
    step.inference_rule.name
    for step in prop51_entry.proof_steps
    if step.inference_rule is not None
  )

  assert (
    "Toda Proposition 5.1 higher eta group relation"
    in rule_names
  )
  assert (
    "Toda Proposition 5.1 finite-dimensional integration"
    in rule_names
  )

  assert any(
    (
      r"\pi_{n + 1}^{n} = "
      r"\mathbb{Z}/2\{\eta_{n}\}"
    )
    in line
    for line in statement_lines[
      prop51_entry.number
    ]
  )
