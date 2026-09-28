from dataclasses import dataclass
from enum import Enum

from proof import (
  LiteratureReference,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  Relation,
)
from proof_repository import ProofRepositoryEntry
from toda_calculation_goal import (
  TodaCalculationGoalSource,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
)
from toda_proof_dependency import (
  TodaProofDependency,
  TodaProofDependencyResult,
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)


class TodaLiteratureSourceKind(Enum):
  REFERENCE = "reference"
  TEXT = "text"


TodaLiteratureSourceValue = (
  LiteratureReference
  | str
)


@dataclass(frozen=True)
class TodaLiteratureSourcePresentation:
  kind: TodaLiteratureSourceKind
  source: TodaLiteratureSourceValue

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaLiteratureSourceKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaLiteratureSourceKind"
      )

    if (
      self.kind
      is TodaLiteratureSourceKind.REFERENCE
    ):
      if not isinstance(
        self.source,
        LiteratureReference,
      ):
        raise TypeError(
          "reference source must be "
          "a LiteratureReference"
        )
      return

    if not isinstance(
      self.source,
      str,
    ):
      raise TypeError(
        "text source must be a str"
      )

    if not self.source:
      raise ValueError(
        "text source must not be empty"
      )


@dataclass(frozen=True)
class TodaRepositoryEntryPresentation:
  source_entry: ProofRepositoryEntry

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "source_entry must be "
        "a ProofRepositoryEntry"
      )

  @property
  def key(
    self,
  ) -> str:
    return self.source_entry.key

  @property
  def phase(
    self,
  ) -> str | None:
    return self.source_entry.phase

  @property
  def theorem(
    self,
  ) -> str | None:
    return self.source_entry.theorem


@dataclass(frozen=True)
class TodaCalculationGoalSourcePresentation:
  source_goal_source: TodaCalculationGoalSource
  repository_source: TodaRepositoryEntryPresentation

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_goal_source,
      TodaCalculationGoalSource,
    ):
      raise TypeError(
        "source_goal_source must be "
        "a TodaCalculationGoalSource"
      )

    if not isinstance(
      self.repository_source,
      TodaRepositoryEntryPresentation,
    ):
      raise TypeError(
        "repository_source must be a "
        "TodaRepositoryEntryPresentation"
      )

    if (
      self.repository_source.source_entry
      is not self.source_goal_source.source_entry
    ):
      raise ValueError(
        "repository source identity must match "
        "source_goal_source.source_entry"
      )

  @property
  def branch_name(
    self,
  ) -> str:
    return self.source_goal_source.branch_name


@dataclass(frozen=True)
class TodaProofStepPresentation:
  source_step: ProofStep
  role: TodaProofDependencyRole
  literature_source: (
    TodaLiteratureSourcePresentation
    | None
  )
  repository_sources: tuple[
    TodaRepositoryEntryPresentation,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_step,
      ProofStep,
    ):
      raise TypeError(
        "source_step must be a ProofStep"
      )

    if not isinstance(
      self.role,
      TodaProofDependencyRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaProofDependencyRole"
      )

    expected_role = (
      classify_toda_proof_step_role(
        self.source_step
      )
    )

    if self.role is not expected_role:
      raise ValueError(
        "role must match source_step "
        "classification"
      )

    expected_literature_source = (
      extract_toda_proof_step_literature_source(
        self.source_step
      )
    )

    if (
      self.literature_source
      != expected_literature_source
    ):
      raise ValueError(
        "literature_source must match "
        "source_step"
      )

    if not isinstance(
      self.repository_sources,
      tuple,
    ):
      raise TypeError(
        "repository_sources must be a tuple"
      )

    for repository_source in (
      self.repository_sources
    ):
      if not isinstance(
        repository_source,
        TodaRepositoryEntryPresentation,
      ):
        raise TypeError(
          "repository_sources must contain "
          "only TodaRepositoryEntryPresentation "
          "objects"
        )

      if (
        repository_source
        .source_entry
        .step
        is not self.source_step
      ):
        raise ValueError(
          "repository source step identity "
          "must match source_step"
        )

  @property
  def proof_rule(
    self,
  ) -> ProofRule:
    return self.source_step.rule

  @property
  def conclusion(
    self,
  ):
    return self.source_step.conclusion


@dataclass(frozen=True)
class TodaProofDependencyPresentation:
  source_dependency: TodaProofDependency
  step: TodaProofStepPresentation

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_dependency,
      TodaProofDependency,
    ):
      raise TypeError(
        "source_dependency must be "
        "a TodaProofDependency"
      )

    if not isinstance(
      self.step,
      TodaProofStepPresentation,
    ):
      raise TypeError(
        "step must be a "
        "TodaProofStepPresentation"
      )

    if (
      self.step.source_step
      is not self.source_dependency.proof_step
    ):
      raise ValueError(
        "step source identity must match "
        "source_dependency.proof_step"
      )

    if (
      self.step.role
      is not self.source_dependency.role
    ):
      raise ValueError(
        "step role must match "
        "source_dependency.role"
      )

  @property
  def depth(
    self,
  ) -> int:
    return self.source_dependency.depth

  @property
  def is_direct(
    self,
  ) -> bool:
    return self.source_dependency.is_direct


@dataclass(frozen=True)
class TodaProofDependencyPresentationResult:
  source_result: TodaProofDependencyResult
  root: TodaProofStepPresentation
  dependencies: tuple[
    TodaProofDependencyPresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      TodaProofDependencyResult,
    ):
      raise TypeError(
        "source_result must be "
        "a TodaProofDependencyResult"
      )

    if not isinstance(
      self.root,
      TodaProofStepPresentation,
    ):
      raise TypeError(
        "root must be a "
        "TodaProofStepPresentation"
      )

    if (
      self.root.source_step
      is not self.source_result.root_step
    ):
      raise ValueError(
        "root source identity must match "
        "source_result.root_step"
      )

    if not isinstance(
      self.dependencies,
      tuple,
    ):
      raise TypeError(
        "dependencies must be a tuple"
      )

    if (
      len(self.dependencies)
      != len(
        self.source_result.dependencies
      )
    ):
      raise ValueError(
        "dependencies must match "
        "source_result.dependencies"
      )

    for (
      presented_dependency,
      source_dependency,
    ) in zip(
      self.dependencies,
      self.source_result.dependencies,
    ):
      if not isinstance(
        presented_dependency,
        TodaProofDependencyPresentation,
      ):
        raise TypeError(
          "dependencies must contain only "
          "TodaProofDependencyPresentation "
          "objects"
        )

      if (
        presented_dependency
        .source_dependency
        is not source_dependency
      ):
        raise ValueError(
          "dependency identity must match "
          "source_result in order"
        )


@dataclass(frozen=True)
class TodaCalculationCandidateSourcePresentation:
  source_candidate: TodaCalculationCandidate
  result_source: TodaRepositoryEntryPresentation
  goal_source: (
    TodaCalculationGoalSourcePresentation
    | None
  )

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

    if not isinstance(
      self.result_source,
      TodaRepositoryEntryPresentation,
    ):
      raise TypeError(
        "result_source must be a "
        "TodaRepositoryEntryPresentation"
      )

    if (
      self.result_source.source_entry
      is not self.source_candidate
      .group_result
      .source_entry
    ):
      raise ValueError(
        "result_source identity must match "
        "candidate.group_result.source_entry"
      )

    if self.source_candidate.goal_source is None:
      if self.goal_source is not None:
        raise ValueError(
          "goal_source must be None when "
          "candidate.goal_source is None"
        )
      return

    if not isinstance(
      self.goal_source,
      TodaCalculationGoalSourcePresentation,
    ):
      raise TypeError(
        "goal_source must be a "
        "TodaCalculationGoalSourcePresentation"
      )

    if (
      self.goal_source.source_goal_source
      is not self.source_candidate.goal_source
    ):
      raise ValueError(
        "goal_source identity must match "
        "candidate.goal_source"
      )


def build_toda_literature_source_presentation(
  source: TodaLiteratureSourceValue,
) -> TodaLiteratureSourcePresentation:
  if isinstance(
    source,
    LiteratureReference,
  ):
    return TodaLiteratureSourcePresentation(
      kind=(
        TodaLiteratureSourceKind
        .REFERENCE
      ),
      source=source,
    )

  if isinstance(
    source,
    str,
  ):
    return TodaLiteratureSourcePresentation(
      kind=(
        TodaLiteratureSourceKind
        .TEXT
      ),
      source=source,
    )

  raise TypeError(
    "source must be a "
    "LiteratureReference or str"
  )


def extract_toda_proof_step_literature_source(
  proof_step: ProofStep,
) -> (
  TodaLiteratureSourcePresentation
  | None
):
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  conclusion = proof_step.conclusion

  if isinstance(
    conclusion,
    LiteratureStatement,
  ):
    return (
      build_toda_literature_source_presentation(
        conclusion.reference
      )
    )

  if (
    isinstance(
      conclusion,
      Relation,
    )
    and conclusion.source is not None
  ):
    return (
      build_toda_literature_source_presentation(
        conclusion.source
      )
    )

  return None


def build_toda_repository_entry_presentation(
  entry: ProofRepositoryEntry,
) -> TodaRepositoryEntryPresentation:
  if not isinstance(
    entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "entry must be a ProofRepositoryEntry"
    )

  return TodaRepositoryEntryPresentation(
    source_entry=entry,
  )


def build_toda_calculation_goal_source_presentation(
  goal_source: TodaCalculationGoalSource,
) -> TodaCalculationGoalSourcePresentation:
  if not isinstance(
    goal_source,
    TodaCalculationGoalSource,
  ):
    raise TypeError(
      "goal_source must be "
      "a TodaCalculationGoalSource"
    )

  return TodaCalculationGoalSourcePresentation(
    source_goal_source=goal_source,
    repository_source=(
      build_toda_repository_entry_presentation(
        goal_source.source_entry
      )
    ),
  )


def _repository_presentations_for_step(
  proof_step: ProofStep,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ],
) -> tuple[
  TodaRepositoryEntryPresentation,
  ...,
]:
  if not isinstance(
    repository_entries,
    tuple,
  ):
    raise TypeError(
      "repository_entries must be a tuple"
    )

  for entry in repository_entries:
    if not isinstance(
      entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "repository_entries must contain only "
        "ProofRepositoryEntry objects"
      )

  return tuple(
    build_toda_repository_entry_presentation(
      entry
    )
    for entry in repository_entries
    if entry.step is proof_step
  )


def build_toda_proof_step_presentation(
  proof_step: ProofStep,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ] = (),
) -> TodaProofStepPresentation:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  return TodaProofStepPresentation(
    source_step=proof_step,
    role=(
      classify_toda_proof_step_role(
        proof_step
      )
    ),
    literature_source=(
      extract_toda_proof_step_literature_source(
        proof_step
      )
    ),
    repository_sources=(
      _repository_presentations_for_step(
        proof_step,
        repository_entries,
      )
    ),
  )


def build_toda_proof_dependency_presentation(
  dependency: TodaProofDependency,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ] = (),
) -> TodaProofDependencyPresentation:
  if not isinstance(
    dependency,
    TodaProofDependency,
  ):
    raise TypeError(
      "dependency must be "
      "a TodaProofDependency"
    )

  return TodaProofDependencyPresentation(
    source_dependency=dependency,
    step=(
      build_toda_proof_step_presentation(
        dependency.proof_step,
        repository_entries,
      )
    ),
  )


def build_toda_proof_dependency_presentation_result(
  dependency_result: TodaProofDependencyResult,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ] = (),
) -> TodaProofDependencyPresentationResult:
  if not isinstance(
    dependency_result,
    TodaProofDependencyResult,
  ):
    raise TypeError(
      "dependency_result must be "
      "a TodaProofDependencyResult"
    )

  return TodaProofDependencyPresentationResult(
    source_result=dependency_result,
    root=(
      build_toda_proof_step_presentation(
        dependency_result.root_step,
        repository_entries,
      )
    ),
    dependencies=tuple(
      build_toda_proof_dependency_presentation(
        dependency,
        repository_entries,
      )
      for dependency in (
        dependency_result.dependencies
      )
    ),
  )


def build_toda_calculation_candidate_source_presentation(
  candidate: TodaCalculationCandidate,
) -> TodaCalculationCandidateSourcePresentation:
  if not isinstance(
    candidate,
    TodaCalculationCandidate,
  ):
    raise TypeError(
      "candidate must be "
      "a TodaCalculationCandidate"
    )

  goal_source = None

  if candidate.goal_source is not None:
    goal_source = (
      build_toda_calculation_goal_source_presentation(
        candidate.goal_source
      )
    )

  return TodaCalculationCandidateSourcePresentation(
    source_candidate=candidate,
    result_source=(
      build_toda_repository_entry_presentation(
        candidate
        .group_result
        .source_entry
      )
    ),
    goal_source=goal_source,
  )
