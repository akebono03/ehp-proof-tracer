# Phase 155 Closure-R2C-R5 changed code

## Changed repository files

- `tests/test_phase153_r2_public_reference_semantic_fact.py`
- `tests/test_phase153_r3_10_public_reference_connection_repair.py`
- `tests/test_phase153_r3_5_reference_body_duplicate_suppression.py`
- `tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py`
- `tests/test_phase96_actual_pi9_5_end_to_end_presentation.py`
- `tests/test_phase96_representative_targets_end_to_end_presentation.py`
- `tests/test_phase97_actual_representative_targets_top_level_api.py`
- `tests/test_phase98_representative_convenience_validation.py`
- `tests/phase155_audit_only_nodeids.txt`
- `tests/test_phase155_audit_boundary.py`

## Top-level import changes

No top-level import changes.

## New merged Phase153 audit

```python
def test_phase153_r3_10_all_group_reference_population_invariants():
  missing_statements = []
  missing_markers = []
  entries_without_selected_statement = []

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _phase153_r3_10_presentations():
    entries = (
      build_toda_group_proof_narrative_reference_entries(
        presentation
      )
    )

    if not entries:
      continue

    selected_by_number = (
      _toda_group_proof_narrative_reference_statement_lines_by_number(
        presentation,
        entries,
      )
    )
    canonical_reference_section = (
      render_toda_group_proof_narrative_reference_entries_markdown(
        entries,
        selected_by_number,
      )
    )
    rendered = (
      render_toda_group_proof_narrative_markdown(
        raw_presentation
      )
    )
    public_reference_section = (
      _phase153_r3_10_public_reference_section(
        rendered,
        canonical_reference_section,
      )
    )

    assert public_reference_section, (
      n,
      k,
      rendered,
    )

    for entry in entries:
      statement_lines = (
        selected_by_number.get(
          entry.number,
          (),
        )
      )

      if not statement_lines:
        entries_without_selected_statement.append(
          (
            n,
            k,
            entry.number,
            entry.reference.locator
            or entry.reference.label,
          )
        )

      marker = (
        "[R"
        + str(
          entry.number
        )
        + "]"
      )

      if marker not in public_reference_section:
        missing_markers.append(
          (
            n,
            k,
            entry.number,
            entry.reference.locator
            or entry.reference.label,
          )
        )

      for statement_line in statement_lines:
        if statement_line in public_reference_section:
          continue

        missing_statements.append(
          (
            n,
            k,
            entry.number,
            entry.reference.locator
            or entry.reference.label,
            statement_line,
          )
        )

  assert entries_without_selected_statement == []
  assert missing_markers == []
  assert missing_statements == []
```

## New merged Phase97 cross-layer audit

```python
def test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api():
  actual = build_phase97_5_data()

  expected = {
    "pi7_4": (
      "65",
      "Toda Proposition 5.6",
      "pi7_4_group_relation",
    ),
    "pi9_5": (
      "68",
      "Toda Proposition 5.8",
      "pi9_5_group_relation",
    ),
    "pi10_4": (
      "73",
      "Toda Proposition 5.11",
      "pi10_4_group_relation",
    ),
    "pi11_5": (
      "73",
      "Toda Proposition 5.11",
      (
        "nu_squared_finite_dimensional."
        "pi11_5_group_relation"
      ),
    ),
    "pi9_2": (
      "75",
      "Toda Proposition 5.15",
      "pi9_2_zero",
    ),
    "pi12_5": (
      "75",
      "Toda Proposition 5.15",
      "pi12_5_group_relation",
    ),
  }

  for (
    key,
    (
      expected_phase,
      expected_theorem,
      expected_branch,
    ),
  ) in expected.items():
    report_candidate = (
      get_phase97_5_single_report_candidate(
        actual[
          "results"
        ][
          key
        ]
      )
    )
    source_candidate = (
      report_candidate.source_candidate
    )
    goal_source = (
      source_candidate.goal_source
    )
    presented_source = (
      report_candidate
      .presentation
      .source
      .goal_source
    )

    assert goal_source is not None
    assert presented_source is not None
    assert (
      presented_source
      .source_goal_source
      is goal_source
    )
    assert (
      presented_source
      .repository_source
      .source_entry
      is goal_source.source_entry
    )
    assert (
      presented_source
      .repository_source
      .phase
      == expected_phase
    )
    assert (
      presented_source
      .repository_source
      .theorem
      == expected_theorem
    )
    assert (
      presented_source.branch_name
      == expected_branch
    )
```

## Deleted functions

Exactly six R2C-R4 DELETE_CANDIDATE functions and three superseded merge-source functions are removed. The two replaced merge-source functions are replaced in place by the merged functions above.
