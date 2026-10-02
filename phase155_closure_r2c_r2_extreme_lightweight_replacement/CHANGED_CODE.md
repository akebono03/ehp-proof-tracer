# Phase 155 Closure-R2C-R2 changed code

## Changed repository files

- `tests/test_phase95_top_level_calculation_orchestration.py`
- `tests/test_phase97_single_found_calculation_to_report_api.py`
- `tests/test_phase97_not_found_multiple_results_top_level_handling.py`

## Import changes

No top-level import changes. All new dependencies are local imports inside the three replacement test functions.

## Replacement 1 — Phase95

```python
def test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order(
  monkeypatch,
):
  from types import SimpleNamespace

  import toda_calculation as calculation_module
  import toda_calculation_goal_discovery as discovery_module
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalCandidate,
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationResult,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first_base = build_phase95_2_candidate(
    "phase155.extreme.first",
    query,
  )
  second_base = build_phase95_2_candidate(
    "phase155.extreme.second",
    query,
  )

  first_entry = (
    first_base
    .group_result
    .source_entry
  )
  second_entry = (
    second_base
    .group_result
    .source_entry
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  first_source = TodaCalculationGoalSource(
    source_entry=first_entry,
    branch_name="synthetic_first",
  )
  second_source = TodaCalculationGoalSource(
    source_entry=second_entry,
    branch_name="synthetic_second",
  )

  goal_by_entry = {
    id(
      first_entry
    ): TodaCalculationGoalCandidate(
      target=query.target,
      goal=(
        first_base
        .group_result
        .proof_step
        .conclusion
      ),
      source=first_source,
    ),
    id(
      second_entry
    ): TodaCalculationGoalCandidate(
      target=query.target,
      goal=(
        second_base
        .group_result
        .proof_step
        .conclusion
      ),
      source=second_source,
    ),
  }

  def extract_one(
    entry,
    actual_query,
  ):
    assert actual_query is query
    return (
      goal_by_entry[
        id(
          entry
        )
      ],
    )

  monkeypatch.setattr(
    discovery_module,
    "extract_concrete_toda_calculation_goal_candidates",
    extract_one,
  )

  discovery = (
    discovery_module
    .discover_concrete_toda_calculation_goal_candidates(
      repository,
      query,
    )
  )

  assert tuple(
    candidate.source.source_entry
    for candidate in discovery.candidates
  ) == (
    first_entry,
    second_entry,
  )

  monkeypatch.setattr(
    calculation_module,
    "build_known_toda_calculation_result",
    lambda actual_repository, actual_query: (
      TodaCalculationResult(
        query=actual_query,
        candidates=(),
      )
    ),
  )
  monkeypatch.setattr(
    calculation_module,
    "discover_concrete_toda_calculation_goal_candidates",
    lambda actual_repository, actual_query: discovery,
  )

  result_by_source_entry_id = {
    id(
      first_entry
    ): (
      first_base
      .group_result
    ),
    id(
      second_entry
    ): (
      second_base
      .group_result
    ),
  }

  def normalize_one(
    goal_candidate,
  ):
    return (
      result_by_source_entry_id[
        id(
          goal_candidate
          .source
          .source_entry
        )
      ],
    )

  monkeypatch.setattr(
    calculation_module,
    "normalize_recovered_toda_calculation_goal_candidate",
    normalize_one,
  )

  result = (
    calculation_module
    .build_toda_calculation_result(
      repository,
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert tuple(
    candidate.goal_source.source_entry
    for candidate in result.candidates
  ) == (
    first_entry,
    second_entry,
  )
  assert tuple(
    candidate.group_result
    for candidate in result.candidates
  ) == (
    first_base.group_result,
    second_base.group_result,
  )
```

## Replacement 2 — Phase97 provenance

```python
def test_phase97_3_aggregate_found_preserves_goal_source_provenance(
  monkeypatch,
):
  import toda_calculation_report as report_module
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationCandidate,
    TodaCalculationResult,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  base = build_phase95_2_candidate(
    "phase155.report.provenance",
    query,
  )
  source_entry = (
    base
    .group_result
    .source_entry
  )
  goal_source = TodaCalculationGoalSource(
    source_entry=source_entry,
    branch_name="synthetic_branch",
  )
  candidate = TodaCalculationCandidate(
    group_result=base.group_result,
    explanation=base.explanation,
    goal_source=goal_source,
  )
  calculation_result = TodaCalculationResult(
    query=query,
    candidates=(
      candidate,
    ),
  )

  monkeypatch.setattr(
    report_module,
    "build_toda_calculation_result",
    lambda repository, actual_query: calculation_result,
  )

  result = (
    report_module
    .build_toda_found_calculation_report_result(
      ProofRepository(),
      query,
    )
  )

  source_candidate = (
    result.candidates[
      0
    ].source_candidate
  )

  assert (
    source_candidate
    is candidate
  )
  assert (
    source_candidate.goal_source
    is goal_source
  )
  assert (
    source_candidate
    .goal_source
    .source_entry
    is source_entry
  )
  assert (
    source_candidate
    .goal_source
    .branch_name
    == "synthetic_branch"
  )

  source_presentation = (
    result.candidates[
      0
    ].presentation.source
  )

  assert (
    source_presentation
    .goal_source
    .source_goal_source
    is goal_source
  )
  assert (
    source_presentation
    .goal_source
    .repository_source
    .source_entry
    is source_entry
  )
  assert (
    source_presentation
    .goal_source
    .branch_name
    == "synthetic_branch"
  )
```

## Replacement 3 — Phase97 multiple-order

```python
def test_phase97_4_multiple_aggregate_results_preserve_goal_source_order(
  monkeypatch,
):
  import toda_calculation_report as report_module
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationCandidate,
    TodaCalculationResult,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first_base = build_phase95_2_candidate(
    "phase155.report.first",
    query,
  )
  second_base = build_phase95_2_candidate(
    "phase155.report.second",
    query,
  )

  first_entry = (
    first_base
    .group_result
    .source_entry
  )
  second_entry = (
    second_base
    .group_result
    .source_entry
  )

  first_goal_source = (
    TodaCalculationGoalSource(
      source_entry=first_entry,
      branch_name="synthetic_first",
    )
  )
  second_goal_source = (
    TodaCalculationGoalSource(
      source_entry=second_entry,
      branch_name="synthetic_second",
    )
  )

  first = TodaCalculationCandidate(
    group_result=first_base.group_result,
    explanation=first_base.explanation,
    goal_source=first_goal_source,
  )
  second = TodaCalculationCandidate(
    group_result=second_base.group_result,
    explanation=second_base.explanation,
    goal_source=second_goal_source,
  )

  calculation_result = TodaCalculationResult(
    query=query,
    candidates=(
      first,
      second,
    ),
  )

  monkeypatch.setattr(
    report_module,
    "build_toda_calculation_result",
    lambda repository, actual_query: calculation_result,
  )

  result = (
    report_module
    .build_toda_calculation_report_result(
      ProofRepository(),
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert tuple(
    report_candidate.source_candidate
    for report_candidate in result.candidates
  ) == (
    first,
    second,
  )
  assert tuple(
    report_candidate
    .source_candidate
    .goal_source
    .source_entry
    for report_candidate in result.candidates
  ) == (
    first_entry,
    second_entry,
  )
  assert tuple(
    report_candidate
    .presentation
    .source
    .goal_source
    .repository_source
    .source_entry
    for report_candidate in result.candidates
  ) == (
    first_entry,
    second_entry,
  )
```
