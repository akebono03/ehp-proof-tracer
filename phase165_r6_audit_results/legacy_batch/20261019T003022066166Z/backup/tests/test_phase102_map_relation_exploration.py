import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
)
from map_facts import EHP_H_MAP
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_map_relation_exploration import (
  RepositoryMapRelationOccurrence,
  find_repository_map_relation_occurrences,
)
from test_phase58_hopf_eta5_bridge import (
  build_phase58_4_data,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def test_phase102_4_actual_h_nu_prime_equals_eta5_is_extracted_losslessly():
  data = build_phase58_4_data()

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_eta5"
      ]
    )
  )

  entry = ProofRepositoryEntry(
    key="phase58.h_nu_prime_eta5",
    step=final_step,
    phase="58",
    theorem="Toda Lemma 5.2 / Hopf bridge",
  )

  repository = ProofRepository()
  repository.register(
    entry
  )

  result = (
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
    )
  )

  assert len(
    result
  ) == 1

  occurrence = result[
    0
  ]

  assert isinstance(
    occurrence,
    RepositoryMapRelationOccurrence,
  )

  assert (
    occurrence
    .source_pattern_occurrence
    .source_occurrence
    .entry
    is entry
  )

  assert (
    occurrence.relation
    is final_step.conclusion
  )

  assert (
    occurrence.map_application
    is final_step.conclusion.lhs
  )

  assert (
    occurrence.map
    is final_step.conclusion.lhs.map
  )

  assert (
    occurrence.input_expression
    is final_step.conclusion.lhs.expression
  )

  assert (
    occurrence.output_expression
    is final_step.conclusion.rhs
  )

  assert occurrence.map == EHP_H_MAP

  assert (
    occurrence.output_expression
    == data[
      "eta_5"
    ]
  )


def test_phase102_4_map_symbol_filter_matches_h():
  data = build_phase58_4_data()

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_eta5"
      ]
    )
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase58.h_nu_prime_eta5",
      step=final_step,
    )
  )

  assert len(
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
      map_symbol=EHP_H_MAP,
    )
  ) == 1

  assert (
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
      map_symbol=MapSymbol(
        name="E",
      ),
    )
    == ()
  )


def test_phase102_4_non_map_relation_is_excluded():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator(),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase102.non-map",
      step=ProofStep(
        conclusion=Relation(
          lhs=nu_prime,
          rhs=eta_5,
          relation_type=RelationType.EQUALITY,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  assert (
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
    )
    == ()
  )


def test_phase102_4_generator_on_map_output_only_is_excluded():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator(),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase102.output-only",
      step=ProofStep(
        conclusion=Relation(
          lhs=MapApplication(
            map=EHP_H_MAP,
            expression=eta_5,
          ),
          rhs=nu_prime,
          relation_type=RelationType.EQUALITY,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  assert (
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
    )
    == ()
  )


def test_phase102_4_non_equality_map_relation_is_excluded():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator(),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase102.order",
      step=ProofStep(
        conclusion=Relation(
          lhs=MapApplication(
            map=EHP_H_MAP,
            expression=nu_prime,
          ),
          rhs=eta_5,
          relation_type=RelationType.ORDER,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  assert (
    find_repository_map_relation_occurrences(
      repository,
      nu_prime_generator(),
    )
    == ()
  )


def test_phase102_4_repository_order_is_preserved():
  generator = nu_prime_generator()

  first_element = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=generator,
  )

  second_element = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  output = HomotopyElement(
    name="η₅",
    dimension=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  first_entry = ProofRepositoryEntry(
    key="phase102.first",
    step=ProofStep(
      conclusion=Relation(
        lhs=MapApplication(
          map=MapSymbol(
            name="H",
          ),
          expression=first_element,
        ),
        rhs=output,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  second_entry = ProofRepositoryEntry(
    key="phase102.second",
    step=ProofStep(
      conclusion=Relation(
        lhs=MapApplication(
          map=MapSymbol(
            name="E",
          ),
          expression=second_element,
        ),
        rhs=output,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    find_repository_map_relation_occurrences(
      repository,
      generator,
    )
  )

  assert tuple(
    occurrence
    .source_pattern_occurrence
    .source_occurrence
    .entry
    for occurrence in result
  ) == (
    first_entry,
    second_entry,
  )


def test_phase102_4_unknown_generator_returns_empty_tuple():
  repository = ProofRepository()

  assert (
    find_repository_map_relation_occurrences(
      repository,
      GeneratorSymbol(
        family="ζ",
        index=999,
      ),
    )
    == ()
  )


def test_phase102_4_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    find_repository_map_relation_occurrences(
      "not-a-repository",
      nu_prime_generator(),
    )


def test_phase102_4_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_map_relation_occurrences(
      ProofRepository(),
      "ν′",
    )


def test_phase102_4_rejects_invalid_map_symbol_filter():
  with pytest.raises(
    TypeError,
    match=(
      "map_symbol must be a MapSymbol or None"
    ),
  ):
    find_repository_map_relation_occurrences(
      ProofRepository(),
      nu_prime_generator(),
      map_symbol="H",
    )
