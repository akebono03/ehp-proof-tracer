# Phase 155 Closure-R2C-R3-R1 changed code

## Changed repository files

- `tests/test_phase96_proof_step_source_presentation.py`
- `tests/test_phase155_audit_boundary.py`

## Top-level import changes

No top-level import changes. `TodaGroupQuery` is imported locally inside the two modified Phase96 test functions.

## Phase96 replacement 1

```python
def test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch():
  from proof import (
    ProofRule,
    ProofStep,
  )
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationCandidate,
  )
  from toda_group_query import (
    TodaGroupQuery,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  base = build_phase95_2_candidate(
    "phase155.phase96.result",
    query,
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase155.phase96.aggregate",
    step=ProofStep(
      conclusion="synthetic aggregate",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    phase="68",
    theorem="Toda Proposition 5.8",
  )
  candidate = TodaCalculationCandidate(
    group_result=base.group_result,
    explanation=base.explanation,
    goal_source=TodaCalculationGoalSource(
      source_entry=aggregate_entry,
      branch_name="pi9_5_group_relation",
    ),
  )

  presentation = (
    build_toda_calculation_candidate_source_presentation(
      candidate
    )
  )

  assert isinstance(
    presentation,
    TodaCalculationCandidateSourcePresentation,
  )
  assert (
    presentation.source_candidate
    is candidate
  )
  assert (
    presentation
    .goal_source
    .source_goal_source
    is candidate.goal_source
  )
  assert (
    presentation
    .goal_source
    .repository_source
    .source_entry
    is aggregate_entry
  )
  assert (
    presentation
    .goal_source
    .repository_source
    .phase
    == "68"
  )
  assert (
    presentation
    .goal_source
    .repository_source
    .theorem
    == "Toda Proposition 5.8"
  )
  assert (
    presentation.goal_source.branch_name
    == "pi9_5_group_relation"
  )
```

## Phase96 replacement 2

```python
def test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct():
  from proof import (
    ProofRule,
    ProofStep,
  )
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationCandidate,
  )
  from toda_group_query import (
    TodaGroupQuery,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  base = build_phase95_2_candidate(
    "phase155.phase96.distinct.result",
    query,
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase155.phase96.distinct.aggregate",
    step=ProofStep(
      conclusion="synthetic aggregate",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    phase="68",
    theorem="Toda Proposition 5.8",
  )
  candidate = TodaCalculationCandidate(
    group_result=base.group_result,
    explanation=base.explanation,
    goal_source=TodaCalculationGoalSource(
      source_entry=aggregate_entry,
      branch_name="pi9_5_group_relation",
    ),
  )

  presentation = (
    build_toda_calculation_candidate_source_presentation(
      candidate
    )
  )

  assert (
    presentation.result_source.source_entry
    is candidate.group_result.source_entry
  )
  assert (
    presentation
    .goal_source
    .repository_source
    .source_entry
    is aggregate_entry
  )
  assert (
    presentation.result_source.source_entry
    is not presentation
    .goal_source
    .repository_source
    .source_entry
  )
```

## Boundary replacement

```python
def test_phase155_audit_boundary_contains_only_reviewed_phase144_or_phase153_tests():
  nodeids = _phase155_audit_nodeids()

  assert all(
    (
      nodeid.startswith(
        "tests/test_phase144_"
      )
      or nodeid.startswith(
        "tests/test_phase153_"
      )
    )
    for nodeid in nodeids
  )
```
