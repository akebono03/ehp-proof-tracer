from dataclasses import dataclass
from enum import Enum

from expression import Expression
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from toda_calculation_goal import (
  TodaCalculationGoalSource,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
)
from toda_ehp_result import (
  TodaEHPSequenceResult,
)
from toda_explanation import (
  TodaRepresentativeExplanationResult,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  TodaGroupResult,
  TodaGroupStructure,
)
from toda_proof_dependency import (
  TodaProofDependencyResult,
  TodaRecursiveProofProvenanceResult,
)


class TodaGeneratorOrderKind(Enum):
  INFINITE = "infinite"
  FINITE = "finite"


@dataclass(frozen=True)
class TodaGeneratorOrderPresentation:
  kind: TodaGeneratorOrderKind
  value: int | None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaGeneratorOrderKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGeneratorOrderKind"
      )

    if (
      self.kind
      is TodaGeneratorOrderKind.INFINITE
    ):
      if self.value is not None:
        raise ValueError(
          "infinite order must have "
          "value None"
        )
      return

    if (
      isinstance(
        self.value,
        bool,
      )
      or not isinstance(
        self.value,
        int,
      )
    ):
      raise TypeError(
        "finite order value must be "
        "a positive int"
      )

    if self.value <= 0:
      raise ValueError(
        "finite order value must be "
        "positive"
      )


@dataclass(frozen=True)
class TodaTargetPresentation:
  source_target: TodaPrimaryGroup

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_target,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "source_target must be "
        "a TodaPrimaryGroup"
      )

  @property
  def group_dimension(
    self,
  ):
    return (
      self.source_target
      .group_dimension
    )

  @property
  def sphere_dimension(
    self,
  ):
    return (
      self.source_target
      .sphere_dimension
    )


@dataclass(frozen=True)
class TodaGeneratorPresentation:
  source_generator: Expression
  order: TodaGeneratorOrderPresentation

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_generator,
      Expression,
    ):
      raise TypeError(
        "source_generator must be "
        "an Expression"
      )

    if not isinstance(
      self.order,
      TodaGeneratorOrderPresentation,
    ):
      raise TypeError(
        "order must be a "
        "TodaGeneratorOrderPresentation"
      )


class TodaGroupStructureKind(Enum):
  ZERO = "zero"
  FREE_CYCLIC = "free_cyclic"
  FINITE_CYCLIC = "finite_cyclic"
  DIRECT_SUM = "direct_sum"


TodaPresentedSourceGroupStructure = (
  FreeCyclicGroup
  | FiniteCyclicGroup
  | DirectSumGroup
  | None
)


@dataclass(frozen=True)
class TodaGroupStructurePresentation:
  kind: TodaGroupStructureKind
  source_structure: (
    TodaPresentedSourceGroupStructure
  )
  generator: (
    TodaGeneratorPresentation
    | None
  ) = None
  summands: tuple[
    "TodaGroupStructurePresentation",
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaGroupStructureKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGroupStructureKind"
      )

    if not isinstance(
      self.summands,
      tuple,
    ):
      raise TypeError(
        "summands must be a tuple"
      )

    for summand in self.summands:
      if not isinstance(
        summand,
        TodaGroupStructurePresentation,
      ):
        raise TypeError(
          "summands must contain only "
          "TodaGroupStructurePresentation "
          "objects"
        )

    if (
      self.kind
      is TodaGroupStructureKind.ZERO
    ):
      if self.source_structure is not None:
        raise ValueError(
          "zero group presentation must "
          "have source_structure None"
        )
      if self.generator is not None:
        raise ValueError(
          "zero group presentation must "
          "not have a generator"
        )
      if self.summands:
        raise ValueError(
          "zero group presentation must "
          "not have summands"
        )
      return

    if (
      self.kind
      is TodaGroupStructureKind.FREE_CYCLIC
    ):
      if not isinstance(
        self.source_structure,
        FreeCyclicGroup,
      ):
        raise TypeError(
          "free cyclic presentation must "
          "wrap a FreeCyclicGroup"
        )
      if not isinstance(
        self.generator,
        TodaGeneratorPresentation,
      ):
        raise TypeError(
          "free cyclic presentation must "
          "have a generator presentation"
        )
      if (
        self.generator.source_generator
        is not self.source_structure.generator
      ):
        raise ValueError(
          "free cyclic generator identity "
          "must match source_structure"
        )
      if (
        self.generator.order.kind
        is not TodaGeneratorOrderKind.INFINITE
      ):
        raise ValueError(
          "free cyclic generator must "
          "have infinite order"
        )
      if self.summands:
        raise ValueError(
          "free cyclic presentation must "
          "not have summands"
        )
      return

    if (
      self.kind
      is TodaGroupStructureKind.FINITE_CYCLIC
    ):
      if not isinstance(
        self.source_structure,
        FiniteCyclicGroup,
      ):
        raise TypeError(
          "finite cyclic presentation must "
          "wrap a FiniteCyclicGroup"
        )
      if not isinstance(
        self.generator,
        TodaGeneratorPresentation,
      ):
        raise TypeError(
          "finite cyclic presentation must "
          "have a generator presentation"
        )
      if (
        self.generator.source_generator
        is not self.source_structure.generator
      ):
        raise ValueError(
          "finite cyclic generator identity "
          "must match source_structure"
        )
      if (
        self.generator.order.kind
        is not TodaGeneratorOrderKind.FINITE
        or self.generator.order.value
        != self.source_structure.order
      ):
        raise ValueError(
          "finite cyclic generator order "
          "must match source_structure"
        )
      if self.summands:
        raise ValueError(
          "finite cyclic presentation must "
          "not have summands"
        )
      return

    if not isinstance(
      self.source_structure,
      DirectSumGroup,
    ):
      raise TypeError(
        "direct sum presentation must "
        "wrap a DirectSumGroup"
      )

    if self.generator is not None:
      raise ValueError(
        "direct sum presentation must "
        "not have a single generator"
      )

    if len(
      self.summands
    ) != len(
      self.source_structure.summands
    ):
      raise ValueError(
        "direct sum presentation summands "
        "must match source_structure"
      )

    for (
      presented_summand,
      source_summand,
    ) in zip(
      self.summands,
      self.source_structure.summands,
    ):
      if (
        presented_summand
        .source_structure
        is not source_summand
      ):
        raise ValueError(
          "direct sum summand identity "
          "must match source_structure "
          "in order"
        )


@dataclass(frozen=True)
class TodaGroupResultPresentation:
  source_group_result: TodaGroupResult
  target: TodaTargetPresentation
  group_structure: TodaGroupStructurePresentation
  generators: tuple[
    TodaGeneratorPresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_group_result,
      TodaGroupResult,
    ):
      raise TypeError(
        "source_group_result must be "
        "a TodaGroupResult"
      )

    if not isinstance(
      self.target,
      TodaTargetPresentation,
    ):
      raise TypeError(
        "target must be a "
        "TodaTargetPresentation"
      )

    if (
      self.target.source_target
      is not self.source_group_result.target
    ):
      raise ValueError(
        "target source identity must match "
        "source_group_result.target"
      )

    if not isinstance(
      self.group_structure,
      TodaGroupStructurePresentation,
    ):
      raise TypeError(
        "group_structure must be a "
        "TodaGroupStructurePresentation"
      )

    if (
      self.group_structure.source_structure
      is not self.source_group_result.group_structure
    ):
      raise ValueError(
        "group structure source identity "
        "must match source_group_result"
      )

    if not isinstance(
      self.generators,
      tuple,
    ):
      raise TypeError(
        "generators must be a tuple"
      )

    if (
      len(self.generators)
      != len(
        self.source_group_result
        .generators
      )
    ):
      raise ValueError(
        "generator presentations must "
        "match source_group_result generators"
      )

    for (
      presented_generator,
      source_generator,
      source_order,
    ) in zip(
      self.generators,
      self.source_group_result.generators,
      self.source_group_result.generator_orders,
    ):
      if not isinstance(
        presented_generator,
        TodaGeneratorPresentation,
      ):
        raise TypeError(
          "generators must contain only "
          "TodaGeneratorPresentation objects"
        )

      if (
        presented_generator
        .source_generator
        is not source_generator
      ):
        raise ValueError(
          "generator source identity must "
          "match source_group_result "
          "in order"
        )

      expected_order = (
        build_toda_generator_order_presentation(
          source_order
        )
      )

      if (
        presented_generator.order
        != expected_order
      ):
        raise ValueError(
          "generator order presentation "
          "must match source_group_result "
          "in order"
        )


@dataclass(frozen=True)
class TodaCalculationPresentationCandidate:
  source_candidate: TodaCalculationCandidate

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_candidate,
      TodaCalculationCandidate,
    ):
      raise TypeError(
        "source_candidate must be "
        "a TodaCalculationCandidate"
      )

  @property
  def group_result(
    self,
  ) -> TodaGroupResult:
    return (
      self.source_candidate
      .group_result
    )

  @property
  def explanation(
    self,
  ) -> TodaRepresentativeExplanationResult:
    return (
      self.source_candidate
      .explanation
    )

  @property
  def ehp_result(
    self,
  ) -> TodaEHPSequenceResult | None:
    return (
      self.explanation
      .ehp_result
    )

  @property
  def exactness_provenance(
    self,
  ) -> (
    TodaEHPExactnessUseProvenanceResult
    | None
  ):
    return (
      self.explanation
      .exactness_provenance
    )

  @property
  def dependency_result(
    self,
  ) -> TodaProofDependencyResult:
    return (
      self.explanation
      .dependency_result
    )

  @property
  def recursive_provenance(
    self,
  ) -> TodaRecursiveProofProvenanceResult:
    return (
      self.explanation
      .recursive_provenance
    )

  @property
  def goal_source(
    self,
  ) -> TodaCalculationGoalSource | None:
    return (
      self.source_candidate
      .goal_source
    )


@dataclass(frozen=True)
class TodaCalculationPresentationResult:
  source_result: TodaCalculationResult
  candidates: tuple[
    TodaCalculationPresentationCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      TodaCalculationResult,
    ):
      raise TypeError(
        "source_result must be "
        "a TodaCalculationResult"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        TodaCalculationPresentationCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "TodaCalculationPresentationCandidate "
          "objects"
        )

    if (
      len(self.candidates)
      != len(
        self.source_result
        .candidates
      )
    ):
      raise ValueError(
        "presentation candidates must match "
        "source_result candidates"
      )

    for (
      presentation_candidate,
      source_candidate,
    ) in zip(
      self.candidates,
      self.source_result.candidates,
    ):
      if (
        presentation_candidate
        .source_candidate
        is not source_candidate
      ):
        raise ValueError(
          "presentation candidate identity "
          "must match source_result candidate "
          "identity in order"
        )

  @property
  def query(
    self,
  ) -> TodaGroupQuery:
    return self.source_result.query

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return self.source_result.target

  @property
  def status(
    self,
  ) -> TodaCalculationStatus:
    return self.source_result.status


def build_toda_generator_order_presentation(
  order: int | None,
) -> TodaGeneratorOrderPresentation:
  if order is None:
    return TodaGeneratorOrderPresentation(
      kind=TodaGeneratorOrderKind.INFINITE,
      value=None,
    )

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
      "order must be a positive int "
      "or None"
    )

  if order <= 0:
    raise ValueError(
      "order must be positive"
    )

  return TodaGeneratorOrderPresentation(
    kind=TodaGeneratorOrderKind.FINITE,
    value=order,
  )


def build_toda_target_presentation(
  target: TodaPrimaryGroup,
) -> TodaTargetPresentation:
  if not isinstance(
    target,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target must be a TodaPrimaryGroup"
    )

  return TodaTargetPresentation(
    source_target=target,
  )


def build_toda_generator_presentation(
  generator: Expression,
  order: int | None,
) -> TodaGeneratorPresentation:
  if not isinstance(
    generator,
    Expression,
  ):
    raise TypeError(
      "generator must be an Expression"
    )

  return TodaGeneratorPresentation(
    source_generator=generator,
    order=(
      build_toda_generator_order_presentation(
        order
      )
    ),
  )


def build_toda_group_structure_presentation(
  group_structure: TodaGroupStructure,
) -> TodaGroupStructurePresentation:
  if group_structure is None:
    return TodaGroupStructurePresentation(
      kind=TodaGroupStructureKind.ZERO,
      source_structure=None,
    )

  if isinstance(
    group_structure,
    FreeCyclicGroup,
  ):
    return TodaGroupStructurePresentation(
      kind=(
        TodaGroupStructureKind
        .FREE_CYCLIC
      ),
      source_structure=group_structure,
      generator=(
        build_toda_generator_presentation(
          group_structure.generator,
          None,
        )
      ),
    )

  if isinstance(
    group_structure,
    FiniteCyclicGroup,
  ):
    return TodaGroupStructurePresentation(
      kind=(
        TodaGroupStructureKind
        .FINITE_CYCLIC
      ),
      source_structure=group_structure,
      generator=(
        build_toda_generator_presentation(
          group_structure.generator,
          group_structure.order,
        )
      ),
    )

  if isinstance(
    group_structure,
    DirectSumGroup,
  ):
    return TodaGroupStructurePresentation(
      kind=(
        TodaGroupStructureKind
        .DIRECT_SUM
      ),
      source_structure=group_structure,
      summands=tuple(
        build_toda_group_structure_presentation(
          summand
        )
        for summand in (
          group_structure.summands
        )
      ),
    )

  raise TypeError(
    "group_structure must be "
    "FreeCyclicGroup, "
    "FiniteCyclicGroup, "
    "DirectSumGroup, or None"
  )


def build_toda_group_result_presentation(
  group_result: TodaGroupResult,
) -> TodaGroupResultPresentation:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  generators = tuple(
    build_toda_generator_presentation(
      generator,
      order,
    )
    for (
      generator,
      order,
    ) in zip(
      group_result.generators,
      group_result.generator_orders,
    )
  )

  return TodaGroupResultPresentation(
    source_group_result=group_result,
    target=(
      build_toda_target_presentation(
        group_result.target
      )
    ),
    group_structure=(
      build_toda_group_structure_presentation(
        group_result.group_structure
      )
    ),
    generators=generators,
  )


def build_toda_calculation_presentation_result(
  calculation_result: TodaCalculationResult,
) -> TodaCalculationPresentationResult:
  if not isinstance(
    calculation_result,
    TodaCalculationResult,
  ):
    raise TypeError(
      "calculation_result must be "
      "a TodaCalculationResult"
    )

  candidates = tuple(
    TodaCalculationPresentationCandidate(
      source_candidate=candidate,
    )
    for candidate in (
      calculation_result
      .candidates
    )
  )

  return TodaCalculationPresentationResult(
    source_result=calculation_result,
    candidates=candidates,
  )
