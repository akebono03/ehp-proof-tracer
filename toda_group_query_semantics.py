from dataclasses import dataclass
from enum import Enum

from toda_group_query import TodaGroupQuery


class TodaGroupQueryDomainKind(Enum):
  POSITIVE_DIMENSION = "positive_dimension"
  PI_ZERO_BOUNDARY = "pi_zero_boundary"
  OUTSIDE_CLASSICAL_UNSTABLE_DOMAIN = (
    "outside_classical_unstable_domain"
  )


@dataclass(frozen=True)
class TodaGroupQueryDomain:
  query: TodaGroupQuery
  kind: TodaGroupQueryDomainKind

  @property
  def group_dimension(
    self,
  ) -> int:
    return (
      self.query.n
      + self.query.k
    )


def classify_toda_group_query_domain(
  query: TodaGroupQuery,
) -> TodaGroupQueryDomain:
  if not isinstance(
    query,
    TodaGroupQuery,
  ):
    raise TypeError(
      "query must be a TodaGroupQuery"
    )

  group_dimension = (
    query.n
    + query.k
  )

  if group_dimension > 0:
    kind = (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  elif group_dimension == 0:
    kind = (
      TodaGroupQueryDomainKind
      .PI_ZERO_BOUNDARY
    )
  else:
    kind = (
      TodaGroupQueryDomainKind
      .OUTSIDE_CLASSICAL_UNSTABLE_DOMAIN
    )

  return TodaGroupQueryDomain(
    query=query,
    kind=kind,
  )


def render_toda_group_query_domain_cli_message(
  domain: TodaGroupQueryDomain,
) -> str:
  if not isinstance(
    domain,
    TodaGroupQueryDomain,
  ):
    raise TypeError(
      "domain must be a TodaGroupQueryDomain"
    )

  n = domain.query.n
  m = domain.group_dimension

  if (
    domain.kind
    is TodaGroupQueryDomainKind.PI_ZERO_BOUNDARY
  ):
    return (
      f"pi_{{0}}^{{{n}}}: "
      f"S^{n} is path-connected, so pi_0 has "
      "one path component. This is a pointed-set "
      "boundary and is not treated as a group "
      "result by EHP Proof Tracer."
    )

  if (
    domain.kind
    is (
      TodaGroupQueryDomainKind
      .OUTSIDE_CLASSICAL_UNSTABLE_DOMAIN
    )
  ):
    return (
      f"pi_{{{m}}}^{{{n}}}: outside the classical "
      "unstable homotopy-group domain handled by "
      "EHP Proof Tracer."
    )

  raise ValueError(
    "positive-dimensional queries do not have "
    "a domain-information CLI message"
  )


def render_toda_group_query_domain_latex(
  domain: TodaGroupQueryDomain,
) -> str:
  if not isinstance(
    domain,
    TodaGroupQueryDomain,
  ):
    raise TypeError(
      "domain must be a TodaGroupQueryDomain"
    )

  n = domain.query.n
  m = domain.group_dimension

  if (
    domain.kind
    is TodaGroupQueryDomainKind.PI_ZERO_BOUNDARY
  ):
    return (
      rf"\pi_{{0}}(S^{{{n}}})"
      r"\text{ has one path component}"
    )

  if (
    domain.kind
    is (
      TodaGroupQueryDomainKind
      .OUTSIDE_CLASSICAL_UNSTABLE_DOMAIN
    )
  ):
    return (
      rf"\pi_{{{m}}}(S^{{{n}}})"
      r"\text{ is outside the classical unstable "
      r"homotopy-group domain}"
    )

  raise ValueError(
    "positive-dimensional queries do not have "
    "a domain-information LaTeX rendering"
  )
