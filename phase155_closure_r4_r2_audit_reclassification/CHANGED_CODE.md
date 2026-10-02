# Phase 155 Closure-R4-R2 changed code

## Repository files

- `tests/test_phase144_6_r5_43_11d_final_completion_audit.py`
- `tests/test_phase153_r3_10_public_reference_connection_repair.py`
- `tests/test_phase153_r3_11_reference_body_ownership_repair.py`
- `tests/test_phase97_actual_representative_targets_top_level_api.py`
- `tests/phase155_audit_only_nodeids.txt`
- `tests/test_phase155_audit_boundary.py`
- `README.md`
- `docs/design.md`
- `docs/development_log.md`
- `docs/roadmap.md`
- `docs/proof_records.md`

## Production files

None.

## Top-level import changes

None.

## Updated Phase153 audit function

```python
def test_phase153_r3_10_all_group_reference_population_invariants():
  import re

  violations = []

  for (
    n,
    k,
    raw_presentation,
    _presentation,
  ) in _phase153_r3_10_presentations():
    rendered = (
      render_toda_group_proof_narrative_markdown(
        raw_presentation
      )
    )

    header_numbers = []
    body_marker_numbers = []

    for line in rendered.splitlines():
      header_match = re.match(
        r"^\*\*\[R(\d+)\]",
        line,
      )

      if header_match is not None:
        header_numbers.append(
          int(
            header_match.group(
              1
            )
          )
        )
        continue

      body_marker_numbers.extend(
        int(
          number
        )
        for number in re.findall(
          r"\[R(\d+)\]",
          line,
        )
      )

    if header_numbers:
      expected = list(
        range(
          1,
          len(
            header_numbers
          )
          + 1,
        )
      )

      if header_numbers != expected:
        violations.append(
          (
            n,
            k,
            "non_contiguous_reference_headers",
            tuple(
              header_numbers
            ),
          )
        )

      header_set = set(
        header_numbers
      )

      for marker in body_marker_numbers:
        if marker in header_set:
          continue

        violations.append(
          (
            n,
            k,
            "body_marker_without_header",
            marker,
          )
        )

      continue

    if body_marker_numbers:
      violations.append(
        (
          n,
          k,
          "body_markers_without_reference_headers",
          tuple(
            body_marker_numbers
          ),
        )
      )

  assert violations == []
```

## Updated Phase97 audit function

```python
def test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api():
  actual = build_phase97_5_data()

  for key in REPRESENTATIVE_KEYS:
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
    source_presentation = (
      report_candidate
      .presentation
      .source
    )

    assert (
      source_presentation.source_candidate
      is source_candidate
    )
    assert (
      source_presentation
      .result_source
      .source_entry
      is source_candidate
      .group_result
      .source_entry
    )

    goal_source = (
      source_candidate.goal_source
    )

    if goal_source is None:
      assert (
        source_presentation.goal_source
        is None
      )
      continue

    presented_goal_source = (
      source_presentation.goal_source
    )

    assert presented_goal_source is not None
    assert (
      presented_goal_source
      .source_goal_source
      is goal_source
    )
    assert (
      presented_goal_source
      .repository_source
      .source_entry
      is goal_source.source_entry
    )
    assert (
      presented_goal_source
      .repository_source
      .phase
      == goal_source
      .source_entry
      .phase
    )
    assert (
      presented_goal_source
      .repository_source
      .theorem
      == goal_source
      .source_entry
      .theorem
    )
    assert (
      presented_goal_source.branch_name
      == goal_source.branch_name
    )
```

## Deleted audit functions

- `test_phase144_6_r5_43_11d_final_completion_invariants_pass`
- `test_phase144_6_r5_43_11d_renderer_remains_generic`
- `test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates`

The last deletion does not discard the observation: 117 duplicate candidates are
recorded as Phase156 input.
