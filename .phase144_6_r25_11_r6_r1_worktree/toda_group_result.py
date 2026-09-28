from dataclasses import dataclass

from expression import Expression
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepositoryEntry


TodaGroupStructure = (
  FreeCyclicGroup
  | FiniteCyclicGroup
  | DirectSumGroup
  | None
)


@dataclass(frozen=True)
class TodaGroupResult:
  target: TodaPrimaryGroup
  group_structure: TodaGroupStructure
  generators: tuple[
    Expression,
    ...,
  ]
  generator_orders: tuple[
    int | None,
    ...,
  ]
  source_entry: ProofRepositoryEntry
  proof_step: ProofStep

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.target,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "target must be a TodaPrimaryGroup"
      )

    if (
      self.group_structure
      is not None
      and not isinstance(
        self.group_structure,
        (
          FreeCyclicGroup,
          FiniteCyclicGroup,
          DirectSumGroup,
        ),
      )
    ):
      raise TypeError(
        "group_structure must be "
        "FreeCyclicGroup, "
        "FiniteCyclicGroup, "
        "DirectSumGroup, or None"
      )

    if not isinstance(
      self.generators,
      tuple,
    ):
      raise TypeError(
        "generators must be a tuple"
      )

    for generator in self.generators:
      if not isinstance(
        generator,
        Expression,
      ):
        raise TypeError(
          "generators must contain "
          "only Expression objects"
        )

    if not isinstance(
      self.generator_orders,
      tuple,
    ):
      raise TypeError(
        "generator_orders must be a tuple"
      )

    if (
      len(self.generators)
      != len(self.generator_orders)
    ):
      raise ValueError(
        "generators and generator_orders "
        "must have the same length"
      )

    for order in self.generator_orders:
      if order is None:
        continue

      if (
        isinstance(
          order,
          bool,
        )
        or not isinstance(
          order,
          int,
        )
      ):
        raise TypeError(
          "generator orders must be "
          "positive ints or None"
        )

      if order <= 0:
        raise ValueError(
          "generator orders must be positive"
        )

    if (
      self.group_structure
      is None
      and (
        self.generators
        or self.generator_orders
      )
    ):
      raise ValueError(
        "zero group result must have "
        "empty generators and "
        "generator_orders"
      )

    if not isinstance(
      self.source_entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "source_entry must be "
        "a ProofRepositoryEntry"
      )

    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    if (
      self.proof_step
      is not self.source_entry.step
    ):
      raise ValueError(
        "proof_step must be "
        "source_entry.step"
      )


def _extract_toda_group_generators_and_orders(
  group_structure,
) -> tuple[
  tuple[
    Expression,
    ...,
  ],
  tuple[
    int | None,
    ...,
  ],
]:
  if isinstance(
    group_structure,
    FreeCyclicGroup,
  ):
    return (
      (
        group_structure.generator,
      ),
      (
        None,
      ),
    )

  if isinstance(
    group_structure,
    FiniteCyclicGroup,
  ):
    return (
      (
        group_structure.generator,
      ),
      (
        group_structure.order,
      ),
    )

  if isinstance(
    group_structure,
    DirectSumGroup,
  ):
    generators = []
    orders = []

    for summand in (
      group_structure.summands
    ):
      if not isinstance(
        summand,
        (
          FreeCyclicGroup,
          FiniteCyclicGroup,
          DirectSumGroup,
        ),
      ):
        raise ValueError(
          "DirectSumGroup contains "
          "an unsupported summand type"
        )

      (
        summand_generators,
        summand_orders,
      ) = (
        _extract_toda_group_generators_and_orders(
          summand
        )
      )

      generators.extend(
        summand_generators
      )
      orders.extend(
        summand_orders
      )

    return (
      tuple(
        generators
      ),
      tuple(
        orders
      ),
    )

  raise ValueError(
    "unsupported Toda group structure"
  )


def normalize_toda_group_result(
  entry: ProofRepositoryEntry,
) -> TodaGroupResult:
  if not isinstance(
    entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "entry must be a ProofRepositoryEntry"
    )

  conclusion = entry.step.conclusion

  if isinstance(
    conclusion,
    TodaPrimaryGroupZeroStatement,
  ):
    return TodaGroupResult(
      target=conclusion.group,
      group_structure=None,
      generators=(),
      generator_orders=(),
      source_entry=entry,
      proof_step=entry.step,
    )

  if (
    not isinstance(
      conclusion,
      Relation,
    )
    or (
      conclusion.relation_type
      != RelationType.EQUALITY
    )
    or not isinstance(
      conclusion.lhs,
      TodaPrimaryGroup,
    )
    or not isinstance(
      conclusion.rhs,
      (
        FreeCyclicGroup,
        FiniteCyclicGroup,
        DirectSumGroup,
      ),
    )
  ):
    raise ValueError(
      "entry does not contain "
      "a normalizable Toda group result"
    )

  (
    generators,
    generator_orders,
  ) = (
    _extract_toda_group_generators_and_orders(
      conclusion.rhs
    )
  )

  return TodaGroupResult(
    target=conclusion.lhs,
    group_structure=conclusion.rhs,
    generators=generators,
    generator_orders=generator_orders,
    source_entry=entry,
    proof_step=entry.step,
  )
