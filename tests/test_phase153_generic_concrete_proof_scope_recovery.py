import pytest

from proof import (
  ProofStep,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import (
  TodaGroupQuery,
)


_CONCRETE_CASES = (
  (
    5,
    1,
    "standard.toda.concrete::pi_6_5",
    "60",
    "Toda Lemma 5.4",
    "Toda Lemma 5.4 pi_6^5 finite-cyclic specialization",
  ),
  (
    6,
    4,
    "standard.toda.concrete::pi_10_6",
    "68",
    "Toda Proposition 5.8",
    "Toda Proposition 5.8 pi_10^6 zero",
  ),
  (
    7,
    3,
    "standard.toda.concrete::pi_10_7",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_10^7 nu_7 specialization",
  ),
  (
    7,
    5,
    "standard.toda.concrete::pi_12_7",
    "70",
    "Toda Proposition 5.9",
    "Toda Proposition 5.9 pi_12^7 zero",
  ),
  (
    9,
    3,
    "standard.toda.concrete::pi_12_9",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_12^9 nu_9 specialization",
  ),
  (
    11,
    2,
    "standard.toda.concrete::pi_13_11",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_13^11 eta_11 squared",
  ),
  (
    13,
    1,
    "standard.toda.concrete::pi_14_13",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_14^13 eta_13",
  ),
)


@pytest.mark.parametrize(
  (
    "n",
    "k",
    "expected_key",
    "expected_phase",
    "expected_theorem",
    "expected_rule_name",
  ),
  _CONCRETE_CASES,
)
def test_phase153_generic_concrete_recovery_precedes_stable_specialization(
  n,
  k,
  expected_key,
  expected_phase,
  expected_theorem,
  expected_rule_name,
):
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=n,
        k=k,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.source_entry.key
    == expected_key
  )
  assert (
    group_result.source_entry.phase
    == expected_phase
  )
  assert (
    group_result.source_entry.theorem
    == expected_theorem
  )
  assert (
    group_result.proof_step
    is group_result.source_entry.step
  )
  assert isinstance(
    group_result.proof_step,
    ProofStep,
  )
  assert (
    group_result.proof_step.inference_rule
    is not None
  )
  assert (
    group_result.proof_step.inference_rule.name
    == expected_rule_name
  )
  assert not (
    group_result.source_entry.key.startswith(
      "standard.toda.stable::"
    )
  )


def test_phase153_generic_concrete_recovery_keeps_stable_specialization_fallback():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=6,
        k=3,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.source_entry.key
    == (
      "standard.toda.stable::"
      "nu_6_specialization"
    )
  )
  assert (
    group_result.source_entry.phase
    == "65"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.6"
  )


def test_phase153_generic_concrete_recovery_does_not_mutate_repository_roots():
  repository = (
    build_standard_production_proof_repository()
  )

  before = tuple(
    entry.key
    for entry in repository.entries()
  )

  for (
    n,
    k,
    _expected_key,
    _expected_phase,
    _expected_theorem,
    _expected_rule_name,
  ) in _CONCRETE_CASES:
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=n,
        k=k,
      ),
    )

  after = tuple(
    entry.key
    for entry in repository.entries()
  )

  assert before == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )
  assert after == before
