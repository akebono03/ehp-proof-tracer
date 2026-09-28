import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from proof import (
  LiteratureReference,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from test_phase93_representative_explanation import (
  build_phase93_5_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
)
from toda_proof_presentation import (
  TodaCalculationCandidateSourcePresentation,
  TodaLiteratureSourceKind,
  TodaLiteratureSourcePresentation,
  TodaProofDependencyPresentationResult,
  TodaProofStepPresentation,
  TodaRepositoryEntryPresentation,
  build_toda_calculation_candidate_source_presentation,
  build_toda_literature_source_presentation,
  build_toda_proof_dependency_presentation_result,
  build_toda_proof_step_presentation,
  build_toda_repository_entry_presentation,
  extract_toda_proof_step_literature_source,
)


def test_phase96_5_proof_step_presentation_preserves_actual_step_and_role():
  data = build_phase93_5_data()

  step = data[
    "phase68"
  ][
    "hopf_zero_step"
  ]

  presentation = (
    build_toda_proof_step_presentation(
      step
    )
  )

  assert isinstance(
    presentation,
    TodaProofStepPresentation,
  )
  assert (
    presentation.source_step
    is step
  )
  assert (
    presentation.role
    is TodaProofDependencyRole.MAP_PROPERTY
  )
  assert (
    presentation.proof_rule
    is step.rule
  )
  assert (
    presentation.conclusion
    is step.conclusion
  )


def test_phase96_5_dependency_presentation_preserves_actual_order_depth_and_roles():
  data = build_phase93_5_data()

  dependency_result = (
    data[
      "explanation"
    ].dependency_result
  )

  presentation = (
    build_toda_proof_dependency_presentation_result(
      dependency_result
    )
  )

  assert isinstance(
    presentation,
    TodaProofDependencyPresentationResult,
  )
  assert (
    presentation.source_result
    is dependency_result
  )
  assert (
    presentation.root.source_step
    is dependency_result.root_step
  )

  assert all(
    presented.source_dependency
    is source
    for presented, source in zip(
      presentation.dependencies,
      dependency_result.dependencies,
    )
  )

  assert tuple(
    dependency.depth
    for dependency in presentation.dependencies
  ) == tuple(
    dependency.depth
    for dependency in dependency_result.dependencies
  )

  assert tuple(
    dependency.step.role
    for dependency in presentation.dependencies
  ) == tuple(
    dependency.role
    for dependency in dependency_result.dependencies
  )


def test_phase96_5_actual_dependency_roles_remain_first_class():
  data = build_phase93_5_data()

  presentation = (
    build_toda_proof_dependency_presentation_result(
      data[
        "explanation"
      ].dependency_result
    )
  )

  roles = {
    dependency.step.role
    for dependency in (
      presentation.dependencies
    )
  }

  assert (
    TodaProofDependencyRole.EHP_EXACTNESS
    in roles
  )
  assert (
    TodaProofDependencyRole.GROUP_STRUCTURE
    in roles
  )
  assert (
    TodaProofDependencyRole.MAP_PROPERTY
    in roles
  )
  assert (
    TodaProofDependencyRole.RELATION
    in roles
  )
  assert (
    TodaProofDependencyRole.DEFINITION
    in roles
  )


def test_phase96_5_literature_statement_preserves_reference_identity():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title="Composition Methods",
    year=1962,
    locator="Chapter V",
  )

  step = ProofStep(
    conclusion=LiteratureStatement(
      reference=reference,
      statement="test statement",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  source = (
    extract_toda_proof_step_literature_source(
      step
    )
  )

  assert isinstance(
    source,
    TodaLiteratureSourcePresentation,
  )
  assert (
    source.kind
    is TodaLiteratureSourceKind.REFERENCE
  )
  assert (
    source.source
    is reference
  )


def test_phase96_5_relation_literature_reference_preserves_identity():
  reference = LiteratureReference(
    label="Toda relation",
  )

  element = HomotopyElement(
    name="x",
    dimension=1,
    generator=GeneratorSymbol(
      family="x",
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs=element,
      rhs=element,
      relation_type=RelationType.EQUALITY,
      source=reference,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source = (
    extract_toda_proof_step_literature_source(
      step
    )
  )

  assert (
    source.kind
    is TodaLiteratureSourceKind.REFERENCE
  )
  assert (
    source.source
    is reference
  )


def test_phase96_5_relation_text_source_is_explicit_text_kind():
  element = HomotopyElement(
    name="x",
    dimension=1,
    generator=GeneratorSymbol(
      family="x",
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs=element,
      rhs=element,
      relation_type=RelationType.EQUALITY,
      source="internal note",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source = (
    extract_toda_proof_step_literature_source(
      step
    )
  )

  assert (
    source.kind
    is TodaLiteratureSourceKind.TEXT
  )
  assert (
    source.source
    == "internal note"
  )


def test_phase96_5_step_without_literature_source_remains_none():
  step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    extract_toda_proof_step_literature_source(
      step
    )
    is None
  )


def test_phase96_5_repository_entry_presentation_preserves_metadata_and_identity():
  step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  entry = ProofRepositoryEntry(
    key="phase96.test",
    step=step,
    phase="96",
    theorem="Test Theorem",
  )

  presentation = (
    build_toda_repository_entry_presentation(
      entry
    )
  )

  assert isinstance(
    presentation,
    TodaRepositoryEntryPresentation,
  )
  assert (
    presentation.source_entry
    is entry
  )
  assert (
    presentation.key
    == "phase96.test"
  )
  assert (
    presentation.phase
    == "96"
  )
  assert (
    presentation.theorem
    == "Test Theorem"
  )


def test_phase96_5_step_presentation_preserves_all_matching_repository_entries_without_selection():
  step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first = ProofRepositoryEntry(
    key="phase96.first",
    step=step,
    phase="96",
    theorem="First label",
  )
  second = ProofRepositoryEntry(
    key="phase96.second",
    step=step,
    phase="96",
    theorem="Second label",
  )

  presentation = (
    build_toda_proof_step_presentation(
      step,
      (
        first,
        second,
      ),
    )
  )

  assert tuple(
    source.source_entry
    for source in (
      presentation.repository_sources
    )
  ) == (
    first,
    second,
  )


def test_phase96_5_step_presentation_does_not_match_repository_by_structural_equality():
  first_step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equal_but_distinct_step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  entry = ProofRepositoryEntry(
    key="phase96.equal",
    step=equal_but_distinct_step,
    theorem="Equal but distinct",
  )

  presentation = (
    build_toda_proof_step_presentation(
      first_step,
      (
        entry,
      ),
    )
  )

  assert (
    presentation.repository_sources
    == ()
  )


def test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
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
    presentation.goal_source
    .source_goal_source
    is candidate.goal_source
  )
  assert (
    presentation.goal_source
    .repository_source
    .source_entry
    is data[
      "phase68_entry"
    ]
  )
  assert (
    presentation.goal_source
    .repository_source
    .phase
    == "68"
  )
  assert (
    presentation.goal_source
    .repository_source
    .theorem
    == "Toda Proposition 5.8"
  )
  assert (
    presentation.goal_source.branch_name
    == "pi9_5_group_relation"
  )


def test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
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
    presentation.goal_source
    .repository_source
    .source_entry
    is candidate
    .goal_source
    .source_entry
  )

  assert (
    presentation.result_source.source_entry
    is not presentation
    .goal_source
    .repository_source
    .source_entry
  )


def test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  aggregate_entry = (
    candidate
    .goal_source
    .source_entry
  )

  dependency_result = (
    candidate
    .explanation
    .dependency_result
  )

  presentation = (
    build_toda_proof_dependency_presentation_result(
      dependency_result,
      (
        aggregate_entry,
      ),
    )
  )

  assert (
    presentation.root.repository_sources
    == ()
  )

  assert all(
    dependency
    .step
    .repository_sources
    == ()
    for dependency in (
      presentation.dependencies
    )
  )


def test_phase96_5_literature_source_builder_rejects_invalid_source():
  with pytest.raises(
    TypeError,
    match=(
      "source must be a "
      "LiteratureReference or str"
    ),
  ):
    build_toda_literature_source_presentation(
      123
    )


def test_phase96_5_proof_step_builder_rejects_non_step():
  with pytest.raises(
    TypeError,
    match=(
      "proof_step must be a ProofStep"
    ),
  ):
    build_toda_proof_step_presentation(
      "not-a-step"
    )


def test_phase96_5_repository_builder_rejects_non_entry():
  with pytest.raises(
    TypeError,
    match=(
      "entry must be a ProofRepositoryEntry"
    ),
  ):
    build_toda_repository_entry_presentation(
      "not-an-entry"
    )


def test_phase96_5_step_presentation_rejects_wrong_role():
  step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "role must match source_step "
      "classification"
    ),
  ):
    TodaProofStepPresentation(
      source_step=step,
      role=(
        TodaProofDependencyRole
        .MAP_PROPERTY
      ),
      literature_source=None,
    )


def test_phase96_5_step_presentation_rejects_repository_entry_for_other_step():
  step = ProofStep(
    conclusion="statement",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  other_step = ProofStep(
    conclusion="other",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  other_entry = ProofRepositoryEntry(
    key="phase96.other",
    step=other_step,
  )

  with pytest.raises(
    ValueError,
    match=(
      "repository source step identity "
      "must match source_step"
    ),
  ):
    TodaProofStepPresentation(
      source_step=step,
      role=(
        TodaProofDependencyRole.OTHER
      ),
      literature_source=None,
      repository_sources=(
        TodaRepositoryEntryPresentation(
          source_entry=other_entry,
        ),
      ),
    )
