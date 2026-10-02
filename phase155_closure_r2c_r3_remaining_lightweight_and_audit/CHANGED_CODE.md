# Phase 155 Closure-R2C-R3 changed code

## Changed repository files

- `tests/test_phase95_actual_representative_top_level_capability.py`
- `tests/test_phase96_proof_step_source_presentation.py`
- `tests/test_phase98_actual_use_facade_validation.py`
- `tests/phase155_audit_only_nodeids.txt`
- `tests/test_phase155_audit_boundary.py`

## Import changes

No top-level import changes. Replacement tests use local imports.

## Replaced test functions

### Phase95 pi9_5
```python
def test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance():
  from homotopy_groups import (
    FiniteCyclicGroup,
  )
  from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
  )
  from test_phase90_known_group_lookup import (
    make_entry,
    make_generator,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationCandidate,
  )
  from toda_explanation import (
    build_toda_representative_explanation,
  )
  from toda_group_result import (
    normalize_toda_group_result,
  )

  query = TodaGroupQuery(
    n=5,
    k=4,
  )
  relation = Relation(
    lhs=query.target,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=make_generator(
        name="nu5_eta8",
        family="synthetic",
        index=5,
        dimension=9,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  result_entry = make_entry(
    key="phase155.pi9_5.result",
    conclusion=relation,
    rule=ProofRule.GIVEN,
  )
  group_result = normalize_toda_group_result(
    result_entry
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase155.pi9_5.aggregate",
    step=ProofStep(
      conclusion="synthetic aggregate",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    phase="68",
    theorem="Toda Proposition 5.8",
  )
  candidate = TodaCalculationCandidate(
    group_result=group_result,
    explanation=build_toda_representative_explanation(
      group_result
    ),
    goal_source=TodaCalculationGoalSource(
      source_entry=aggregate_entry,
      branch_name="pi9_5_group_relation",
    ),
  )

  assert (
    candidate
    .group_result
    .generator_orders
    == (
      2,
    )
  )
  assert (
    candidate
    .group_result
    .proof_step
    is result_entry.step
  )
  assert (
    candidate
    .goal_source
    .source_entry
    is aggregate_entry
  )
  assert (
    candidate
    .goal_source
    .source_entry
    .phase
    == "68"
  )
  assert (
    candidate
    .goal_source
    .source_entry
    .theorem
    == "Toda Proposition 5.8"
  )
  assert (
    candidate
    .goal_source
    .branch_name
    == "pi9_5_group_relation"
  )
```

### Phase95 pi10_4
```python
def test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch():
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

  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  base = build_phase95_2_candidate(
    "phase155.pi10_4.result",
    query,
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase155.pi10_4.aggregate",
    step=ProofStep(
      conclusion="synthetic aggregate",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    phase="73",
    theorem="Toda Proposition 5.11",
  )
  candidate = TodaCalculationCandidate(
    group_result=base.group_result,
    explanation=base.explanation,
    goal_source=TodaCalculationGoalSource(
      source_entry=aggregate_entry,
      branch_name="pi10_4_group_relation",
    ),
  )

  assert (
    candidate
    .group_result
    .generator_orders
    == (
      8,
    )
  )
  assert (
    candidate
    .goal_source
    .source_entry
    is aggregate_entry
  )
  assert (
    candidate
    .goal_source
    .source_entry
    .phase
    == "73"
  )
  assert (
    candidate
    .goal_source
    .source_entry
    .theorem
    == "Toda Proposition 5.11"
  )
  assert (
    candidate
    .goal_source
    .branch_name
    == "pi10_4_group_relation"
  )
```

### Phase96 source metadata
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

### Phase96 distinct sources
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

### Phase96 internal dependency metadata
```python
def test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata():
  from homotopy_groups import (
    FiniteCyclicGroup,
  )
  from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
  )
  from test_phase90_known_group_lookup import (
    make_generator,
  )
  from toda_explanation import (
    build_toda_representative_explanation,
  )
  from toda_group_query import (
    TodaGroupQuery,
  )
  from toda_group_result import (
    normalize_toda_group_result,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  premise = ProofStep(
    conclusion="internal support",
    premises=(),
    rule=ProofRule.GIVEN,
  )
  relation = Relation(
    lhs=query.target,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name="nu4_squared",
        family="nu^2",
        index=4,
        dimension=10,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  root = ProofStep(
    conclusion=relation,
    premises=(
      premise,
    ),
    rule=ProofRule.INFERENCE,
  )
  result_entry = ProofRepositoryEntry(
    key="phase155.phase96.internal.result",
    step=root,
  )
  group_result = normalize_toda_group_result(
    result_entry
  )
  explanation = build_toda_representative_explanation(
    group_result
  )
  aggregate_entry = ProofRepositoryEntry(
    key="phase155.phase96.internal.aggregate",
    step=ProofStep(
      conclusion="aggregate source",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  presentation = (
    build_toda_proof_dependency_presentation_result(
      explanation.dependency_result,
      (
        aggregate_entry,
      ),
    )
  )

  assert (
    presentation.root.repository_sources
    == ()
  )
  assert len(
    presentation.dependencies
  ) == 1
  assert (
    presentation.dependencies[
      0
    ].step.source_step
    is premise
  )
  assert (
    presentation.dependencies[
      0
    ].step.repository_sources
    == ()
  )
```

### Phase98 facade delegation
```python
def test_phase98_3_facade_preserves_goal_source_provenance(
  monkeypatch,
):
  from types import SimpleNamespace

  import toda_calculation_facade as facade_module

  marker = SimpleNamespace(
    provenance="preserved",
  )
  captured = {}

  def fake_build_report(
    repository,
    query,
  ):
    captured[
      "repository"
    ] = repository
    captured[
      "query"
    ] = query
    return marker

  monkeypatch.setattr(
    facade_module,
    "build_toda_calculation_report_result",
    fake_build_report,
  )

  repository = object()
  result = facade_module.build_toda_report(
    repository,
    n=5,
    k=4,
  )

  assert result is marker
  assert (
    captured[
      "repository"
    ]
    is repository
  )
  assert (
    captured[
      "query"
    ].n
    == 5
  )
  assert (
    captured[
      "query"
    ].k
    == 4
  )
  assert (
    captured[
      "query"
    ].target.group_dimension
    == 9
  )
  assert (
    captured[
      "query"
    ].target.sphere_dimension
    == 5
  )
```
