import main as cli_main

from homotopy_groups import (
  FreeCyclicGroup,
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
from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import (
  TodaGroupQueryDomainKind,
  classify_toda_group_query_domain,
)
from web_group_query import (
  build_standard_web_group_query_view,
)


def test_phase130_10_query_accepts_negative_k():
  query = TodaGroupQuery(
    n=4,
    k=-1,
  )

  assert query.k == -1
  assert (
    query.target.group_dimension
    == 3
  )


def test_phase130_10_k0_returns_identity_group():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=10,
        k=0,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.group_structure,
    FreeCyclicGroup,
  )
  assert (
    group_result.generators[
      0
    ].generator.family
    == "ι"
  )
  assert (
    group_result.generators[
      0
    ].generator.index
    == 10
  )


def test_phase130_10_n1_positive_k_reuses_phase56_zero():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=1,
        k=5,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.group_structure
    is None
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "56"
  )
  assert len(
    result.candidates[
      0
    ].group_result.proof_step.premises
  ) == 1


def test_phase130_10_negative_k_positive_dimension_uses_connectivity_zero():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=7,
        k=-5,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.group_structure
    is None
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.theorem
    == "Sphere connectivity"
  )


def test_phase130_10_pi0_query_is_classified_as_boundary():
  domain = classify_toda_group_query_domain(
    TodaGroupQuery(
      n=3,
      k=-3,
    )
  )

  assert (
    domain.kind
    is TodaGroupQueryDomainKind.PI_ZERO_BOUNDARY
  )


def test_phase130_10_negative_group_dimension_is_outside_domain():
  domain = classify_toda_group_query_domain(
    TodaGroupQuery(
      n=2,
      k=-3,
    )
  )

  assert (
    domain.kind
    is (
      TodaGroupQueryDomainKind
      .OUTSIDE_CLASSICAL_UNSTABLE_DOMAIN
    )
  )


def test_phase130_10_cli_displays_pi0_boundary(
  capsys,
):
  exit_code = cli_main.main(
    [
      "3",
      "-3",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert (
    "pi_{0}^{3}"
    in captured.out
  )
  assert (
    "one path component"
    in captured.out
  )


def test_phase130_10_cli_displays_negative_dimension_domain_message(
  capsys,
):
  exit_code = cli_main.main(
    [
      "2",
      "-3",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert (
    "pi_{-1}^{2}"
    in captured.out
  )
  assert (
    "outside the classical unstable "
    "homotopy-group domain"
    in captured.out
  )


def test_phase130_10_web_displays_pi0_boundary_latex():
  view = (
    build_standard_web_group_query_view(
      n=3,
      k=-3,
    )
  )

  assert (
    view.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    view.result_latex
    == (
      r"\pi_{0}(S^{3})"
      r"\text{ has one path component}"
    )
  )


def test_phase130_10_web_displays_negative_dimension_domain_latex():
  view = (
    build_standard_web_group_query_view(
      n=2,
      k=-3,
    )
  )

  assert (
    view.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    "outside the classical unstable"
    in view.result_latex
  )
