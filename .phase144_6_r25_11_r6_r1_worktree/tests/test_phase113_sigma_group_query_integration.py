import main as cli_main
import pytest

from expression import (
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof_repository import ProofRepository
from toda_calculation_facade import (
  build_standard_toda_report,
  build_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


@pytest.mark.parametrize(
  "index",
  (
    10,
    11,
    12,
  ),
)
def test_phase113_standard_group_query_reuses_generic_sigma_specialization(
  index,
):
  result = build_standard_toda_report(
    n=index,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  assert len(
    result.candidates
  ) == 1

  candidate = (
    result.calculation_result
    .candidates[
      0
    ]
  )

  group_result = (
    candidate.group_result
  )

  assert (
    group_result.target
    == TodaPrimaryGroup(
      group_dimension=index + 7,
      sphere_dimension=index,
    )
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )

  assert (
    group_result.group_structure.order
    == 16
  )

  assert (
    group_result.group_structure
    .generator
    .generator
    == GeneratorSymbol(
      family="σ",
      index=index,
    )
  )


def test_phase113_sigma11_group_query_preserves_prop515_provenance():
  result = build_standard_toda_report(
    n=11,
    k=7,
  )

  candidate = (
    result.calculation_result
    .candidates[
      0
    ]
  )

  source_entry = (
    candidate
    .group_result
    .source_entry
  )

  assert (
    source_entry.phase
    == "75"
  )

  assert (
    source_entry.theorem
    == "Toda Proposition 5.15"
  )

  n = ScalarSymbol(
    name="n",
  )

  assert (
    source_entry.step.premises[
      0
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=7,
      ),
      sphere_dimension=n,
    )
  )


def test_phase113_explicit_empty_repository_does_not_invent_sigma_specialization():
  result = build_toda_report(
    ProofRepository(),
    n=11,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )

  assert result.candidates == ()


def test_phase113_cli_11_7_returns_sigma11_group(
  capsys,
):
  exit_code = cli_main.main(
    [
      "11",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    r"$\pi_{18}^{11}$"
    in captured.out
  )

  assert (
    r"\mathbb{Z}/16\{\sigma_{11}\}"
    in captured.out
  )


def test_phase113_existing_pi12_5_group_query_remains_available():
  result = build_standard_toda_report(
    n=5,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  assert (
    result.target
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )
