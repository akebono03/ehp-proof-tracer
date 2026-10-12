"""Phase 163 R2: metadata model only; no proof search or migration."""
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ReferenceKind(str, Enum):
    DEFINITION = "definition"
    PROPOSITION = "proposition"
    LEMMA = "lemma"
    THEOREM = "theorem"
    COROLLARY = "corollary"
    EQUATION = "equation"
    REMARK = "remark"


class AssertionKind(str, Enum):
    STATEMENT = "statement"
    DEFINITION = "definition"


class AssertionOrigin(str, Enum):
    FIXED_STATEMENT = "fixed_statement"
    PROOF_INTERNAL = "proof_internal"


@dataclass(frozen=True)
class LiteratureEntry:
    reference_id: str
    kind: ReferenceKind
    locator: str
    source_id: str | None = None
    publication_position: int | None = None

    def __post_init__(self) -> None:
        _nonempty(self.reference_id, "reference_id")
        _nonempty(self.locator, "locator")
        if not isinstance(self.kind, ReferenceKind):
            raise TypeError("kind must be a ReferenceKind")
        _positive_optional(self.publication_position, "publication_position")


@dataclass(frozen=True)
class AssertionEntry:
    assertion_id: str
    reference_id: str
    kind: AssertionKind
    content: Any
    origin: AssertionOrigin = AssertionOrigin.FIXED_STATEMENT
    component_position: int | None = None
    available_after_position: int | None = None
    scope: Any = None
    defined_symbol: str | None = None
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.assertion_id, "assertion_id")
        _nonempty(self.reference_id, "reference_id")
        if not isinstance(self.kind, AssertionKind):
            raise TypeError("kind must be an AssertionKind")
        if not isinstance(self.origin, AssertionOrigin):
            raise TypeError("origin must be an AssertionOrigin")
        if self.content is None:
            raise ValueError("content is required")
        _positive_optional(self.component_position, "component_position")
        _positive_optional(self.available_after_position, "available_after_position")
        if self.kind is AssertionKind.DEFINITION:
            _nonempty(self.defined_symbol, "defined_symbol")
        if not isinstance(self.dependencies, tuple):
            raise TypeError("dependencies must be a tuple")
        for dependency in self.dependencies:
            _nonempty(dependency, "dependency")
        if self.assertion_id in self.dependencies:
            raise ValueError("self-dependency is forbidden")


@dataclass(frozen=True)
class AssertionInstantiation:
    assertion_id: str
    concrete_content: Any
    substitutions: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.assertion_id, "assertion_id")
        if self.concrete_content is None:
            raise ValueError("concrete_content is required")
        if not isinstance(self.substitutions, tuple):
            raise TypeError("substitutions must be a tuple")
        names = []
        for binding in self.substitutions:
            if not isinstance(binding, tuple) or len(binding) != 2:
                raise TypeError("each substitution must be a pair")
            _nonempty(binding[0], "variable")
            names.append(binding[0])
        if len(names) != len(set(names)):
            raise ValueError("duplicate substitution variable")


@dataclass(frozen=True)
class ProofStepLink:
    assertion_id: str
    repository_key: str | None = None
    step: Any = None

    def __post_init__(self) -> None:
        _nonempty(self.assertion_id, "assertion_id")
        if self.repository_key is not None:
            _nonempty(self.repository_key, "repository_key")
        if self.repository_key is None and self.step is None:
            raise ValueError("repository_key or step is required")
        if self.step is not None:
            from proof import ProofStep
            if not isinstance(self.step, ProofStep):
                raise TypeError("step must be a ProofStep")


class UnifiedStatementRegistry:
    """Small in-memory catalog; no availability/search eligibility decisions."""

    def __init__(self) -> None:
        self._references: dict[str, LiteratureEntry] = {}
        self._assertions: dict[str, AssertionEntry] = {}

    def add_reference(self, entry: LiteratureEntry) -> None:
        if not isinstance(entry, LiteratureEntry):
            raise TypeError("entry must be a LiteratureEntry")
        if entry.reference_id in self._references:
            raise ValueError("duplicate reference_id")
        self._references[entry.reference_id] = entry

    def add_assertion(self, entry: AssertionEntry) -> None:
        if not isinstance(entry, AssertionEntry):
            raise TypeError("entry must be an AssertionEntry")
        if entry.reference_id not in self._references:
            raise ValueError("unknown reference_id")
        if entry.assertion_id in self._assertions:
            raise ValueError("duplicate assertion_id")
        self._assertions[entry.assertion_id] = entry

    def reference(self, reference_id: str) -> LiteratureEntry:
        return self._references[reference_id]

    def assertion(self, assertion_id: str) -> AssertionEntry:
        return self._assertions[assertion_id]

    def assertions_for(self, reference_id: str) -> tuple[AssertionEntry, ...]:
        return tuple(entry for entry in self._assertions.values()
                     if entry.reference_id == reference_id)


def _nonempty(value: str, field: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a str")
    if not value.strip():
        raise ValueError(f"{field} must not be empty")


def _positive_optional(value: int | None, field: str) -> None:
    if value is not None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field} must be an int or None")
        if value <= 0:
            raise ValueError(f"{field} must be positive")
