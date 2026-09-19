from pathlib import Path

from proof import (
  ProofRule,
)
from proof_repository import (
  ProofRepository,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_prop515_upper_bootstrap import (
  build_toda_prop515_upper_bootstrap,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515FiniteDimensionalStatement,
)


def test_phase100_12b_standard_integration_module_has_no_test_or_probe_imports():
  source = Path(
    "standard_production_repository.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_" not in source
  assert "import test_" not in source
  assert "from probes" not in source
  assert "import probes" not in source


def test_phase100_12b_standard_integration_builds_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  assert isinstance(
    repository,
    ProofRepository,
  )


def test_phase100_12b_standard_integration_has_deterministic_entry_order():
  repository = (
    build_standard_production_proof_repository()
  )

  assert tuple(
    entry.key
    for entry in repository.entries()
  ) == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )


def test_phase100_12b_standard_integration_reuses_single_closure_identity():
  repository = (
    build_standard_production_proof_repository()
  )

  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  low_result = (
    upper_result
    .sigma_chain_result
    .low_result
  )

  entries = (
    repository.entries()
  )

  assert (
    entries[0].step
    is low_result.prop56_step
  )

  assert (
    entries[1].step
    is low_result.prop58_step
  )

  assert (
    entries[2].step
    is low_result.prop511_step
  )

  assert (
    entries[3].step
    is upper_result.aggregate_step
  )


def test_phase100_12b_standard_integration_registers_expected_theorems():
  repository = (
    build_standard_production_proof_repository()
  )

  entries = (
    repository.entries()
  )

  expected_types = (
    TodaProp56FiniteDimensionalStatement,
    TodaProp58FiniteDimensionalStatement,
    TodaProp511FiniteDimensionalStatement,
    TodaProp515FiniteDimensionalStatement,
  )

  assert all(
    isinstance(
      entry.step.conclusion,
      expected_type,
    )
    for entry, expected_type
    in zip(
      entries,
      expected_types,
    )
  )


def test_phase100_12b_standard_integration_all_aggregate_steps_are_inference():
  repository = (
    build_standard_production_proof_repository()
  )

  assert all(
    entry.step.rule
    == ProofRule.INFERENCE
    for entry
    in repository.entries()
  )


def test_phase100_12b_standard_integration_preserves_prop515_direct_premises():
  repository = (
    build_standard_production_proof_repository()
  )

  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  prop515_step = (
    repository.entries()[3].step
  )

  assert (
    prop515_step.premises
    == upper_result.aggregate_step.premises
  )

  assert (
    prop515_step.premises[3]
    is upper_result
    .sigma_chain_result
    .low_result
    .pi12_5_step
  )

  assert (
    prop515_step.premises[4]
    is upper_result
    .sigma_chain_result
    .pi13_6_step
  )

  assert (
    prop515_step.premises[5]
    is upper_result
    .sigma_chain_result
    .pi14_7_step
  )

  assert (
    prop515_step.premises[6]
    is upper_result.pi15_8_step
  )

  assert (
    prop515_step.premises[7]
    is upper_result.higher_step
  )


def test_phase100_12b_standard_integration_builder_returns_fresh_repository():
  first = (
    build_standard_production_proof_repository()
  )

  second = (
    build_standard_production_proof_repository()
  )

  assert isinstance(
    first,
    ProofRepository,
  )

  assert isinstance(
    second,
    ProofRepository,
  )

  assert first is not second

  assert (
    first.entries()
    == second.entries()
  )


def test_phase100_12b_standard_integration_does_not_duplicate_entries():
  repository = (
    build_standard_production_proof_repository()
  )

  keys = tuple(
    entry.key
    for entry in repository.entries()
  )

  assert len(keys) == 4
  assert len(set(keys)) == 4
