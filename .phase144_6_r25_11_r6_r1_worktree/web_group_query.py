from dataclasses import dataclass

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import (
  TodaGroupQueryDomainKind,
  classify_toda_group_query_domain,
  render_toda_group_query_domain_latex,
)
from toda_human_readable_renderer import (
  render_toda_group_result_latex,
)


@dataclass(frozen=True)
class WebGroupQueryView:
  n: int
  k: int
  status: TodaCalculationStatus
  result_latex: str | None
  proof_available: bool = False

  def __post_init__(
    self,
  ) -> None:
    if (
      isinstance(
        self.n,
        bool,
      )
      or not isinstance(
        self.n,
        int,
      )
    ):
      raise TypeError(
        "n must be an int"
      )

    if (
      isinstance(
        self.k,
        bool,
      )
      or not isinstance(
        self.k,
        int,
      )
    ):
      raise TypeError(
        "k must be an int"
      )

    if not isinstance(
      self.status,
      TodaCalculationStatus,
    ):
      raise TypeError(
        "status must be a TodaCalculationStatus"
      )

    if (
      self.result_latex is not None
      and not isinstance(
        self.result_latex,
        str,
      )
    ):
      raise TypeError(
        "result_latex must be a str or None"
      )

    if not isinstance(
      self.proof_available,
      bool,
    ):
      raise TypeError(
        "proof_available must be a bool"
      )

    if (
      self.status
      is TodaCalculationStatus.FOUND
    ):
      if self.result_latex is None:
        raise ValueError(
          "FOUND view must contain result_latex"
        )
    elif self.result_latex is not None:
      raise ValueError(
        "non-FOUND view must not contain result_latex"
      )


def build_standard_web_group_query_view(
  n: int,
  k: int,
) -> WebGroupQueryView:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = (
    classify_toda_group_query_domain(
      query
    )
  )

  if (
    domain.kind
    is not (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  ):
    return WebGroupQueryView(
      n=n,
      k=k,
      status=TodaCalculationStatus.FOUND,
      result_latex=(
        render_toda_group_query_domain_latex(
          domain
        )
      ),
      proof_available=False,
    )

  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  result_latex = None

  if (
    report.status
    is TodaCalculationStatus.FOUND
  ):
    result_latex = (
      render_toda_group_result_latex(
        report.candidates[
          0
        ].presentation.group
      )
    )

  return WebGroupQueryView(
    n=n,
    k=k,
    status=report.status,
    result_latex=result_latex,
    proof_available=(
      report.status
      is TodaCalculationStatus.FOUND
    ),
  )
