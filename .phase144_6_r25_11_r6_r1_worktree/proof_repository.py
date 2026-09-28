from dataclasses import dataclass

from proof import ProofStep


@dataclass(frozen=True)
class ProofRepositoryEntry:
  key: str
  step: ProofStep
  phase: str | None = None
  theorem: str | None = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.key,
      str,
    ):
      raise TypeError(
        "key must be a str"
      )

    if not self.key:
      raise ValueError(
        "key must not be empty"
      )

    if not isinstance(
      self.step,
      ProofStep,
    ):
      raise TypeError(
        "step must be a ProofStep"
      )

    if (
      self.phase is not None
      and not isinstance(
        self.phase,
        str,
      )
    ):
      raise TypeError(
        "phase must be a str or None"
      )

    if (
      self.theorem is not None
      and not isinstance(
        self.theorem,
        str,
      )
    ):
      raise TypeError(
        "theorem must be a str or None"
      )


class ProofRepository:
  def __init__(
    self,
  ) -> None:
    self._entries: dict[
      str,
      ProofRepositoryEntry,
    ] = {}

  def register(
    self,
    entry: ProofRepositoryEntry,
  ) -> None:
    if not isinstance(
      entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "entry must be a ProofRepositoryEntry"
      )

    if entry.key in self._entries:
      raise ValueError(
        f"duplicate repository key: {entry.key}"
      )

    self._entries[
      entry.key
    ] = entry

  def get(
    self,
    key: str,
  ) -> ProofRepositoryEntry:
    return self._entries[
      key
    ]

  def entries(
    self,
  ) -> tuple[
    ProofRepositoryEntry,
    ...,
  ]:
    return tuple(
      self._entries.values()
    )

  def find_by_conclusion(
    self,
    conclusion,
  ) -> tuple[
    ProofRepositoryEntry,
    ...,
  ]:
    return tuple(
      entry
      for entry in self._entries.values()
      if (
        entry.step.conclusion
        == conclusion
      )
    )

  def find_by_statement_type(
    self,
    statement_type: type,
  ) -> tuple[
    ProofRepositoryEntry,
    ...,
  ]:
    if not isinstance(
      statement_type,
      type,
    ):
      raise TypeError(
        "statement_type must be a type"
      )

    return tuple(
      entry
      for entry in self._entries.values()
      if isinstance(
        entry.step.conclusion,
        statement_type,
      )
    )

  def find_by_phase(
    self,
    phase: str,
  ) -> tuple[
    ProofRepositoryEntry,
    ...,
  ]:
    return tuple(
      entry
      for entry in self._entries.values()
      if entry.phase == phase
    )

  def find_by_theorem(
    self,
    theorem: str,
  ) -> tuple[
    ProofRepositoryEntry,
    ...,
  ]:
    return tuple(
      entry
      for entry in self._entries.values()
      if entry.theorem == theorem
    )

  def dependencies(
    self,
    entry: ProofRepositoryEntry,
  ) -> tuple[
    ProofStep,
    ...,
  ]:
    if not isinstance(
      entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "entry must be a ProofRepositoryEntry"
      )

    return entry.step.premises
