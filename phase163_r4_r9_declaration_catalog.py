"""Phase 163 R4-R9: additive, source-unverified Definition/Choice catalog.

No claim of external truth, citation eligibility or proof derivation is made.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase163_r4_r8_choice_registration import ChoiceSnapshot, LiteratureChoice
from proof import ProofRule, ProofStep


class DeclarationKind(str, Enum):
    DEFINITION = "definition"
    CHOICE = "choice"


class DeclarationProvenance(str, Enum):
    SOURCE_UNVERIFIED = "source_unverified"


@dataclass(frozen=True)
class LiteratureDeclaration:
    """Typed payload and traceable source; intentionally not a proven theorem."""

    declaration_id: str
    reference_id: str
    kind: DeclarationKind
    defined_symbol: str
    content: Any
    source_step: ProofStep | None = None
    assertion_id: str | None = None
    provenance: DeclarationProvenance = DeclarationProvenance.SOURCE_UNVERIFIED

    def __post_init__(self) -> None:
        for field in ("declaration_id", "reference_id", "defined_symbol"):
            value = getattr(self, field)
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string")
            if not value.strip():
                raise ValueError(f"{field} must not be empty")
        if not isinstance(self.kind, DeclarationKind):
            raise TypeError("kind must be a DeclarationKind")
        if self.provenance is not DeclarationProvenance.SOURCE_UNVERIFIED:
            raise ValueError("external verification cannot be inferred")
        if isinstance(self.content, str) or self.content is None:
            raise TypeError("content must be a typed mathematical object")
        if self.assertion_id is not None and (
            not isinstance(self.assertion_id, str) or not self.assertion_id.strip()
        ):
            raise ValueError("assertion_id must be nonempty")
        if self.source_step is not None:
            if not isinstance(self.source_step, ProofStep):
                raise TypeError("source_step must be ProofStep")
            if self.source_step.rule is not ProofRule.GIVEN or self.source_step.premises:
                raise ValueError("declarations accept only leaf GIVEN witnesses")
            if self.source_step.conclusion != self.content:
                raise ValueError("source_step conclusion must match content")


@dataclass(frozen=True)
class DeclarationCatalog:
    """Immutable supplemental catalog; the base registry is not mutated."""

    bridge: RegistryBridgeResult
    declarations: tuple[LiteratureDeclaration, ...]

    def find(self, declaration_id: str) -> LiteratureDeclaration:
        return next(x for x in self.declarations if x.declaration_id == declaration_id)

    def for_reference(self, reference_id: str) -> tuple[LiteratureDeclaration, ...]:
        return tuple(x for x in self.declarations if x.reference_id == reference_id)


def register_declarations(
    base: RegistryBridgeResult,
    declarations: tuple[LiteratureDeclaration, ...],
) -> DeclarationCatalog:
    """Validate reference and optional component identities; grant no citation rights."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(declarations, tuple):
        raise TypeError("declarations must be a tuple")
    identities: set[str] = set()
    assertions: set[str] = set()
    for declaration in declarations:
        if not isinstance(declaration, LiteratureDeclaration):
            raise TypeError("declarations must contain LiteratureDeclaration")
        if declaration.declaration_id in identities:
            raise ValueError("duplicate declaration_id")
        identities.add(declaration.declaration_id)
        try:
            base.registry.reference(declaration.reference_id)
        except KeyError as exc:
            raise ValueError("unknown reference_id") from exc
        if declaration.assertion_id is not None:
            try:
                linked = base.registry.assertion(declaration.assertion_id)
            except KeyError as exc:
                raise ValueError("unknown assertion_id") from exc
            if linked.reference_id != declaration.reference_id:
                raise ValueError("assertion/reference mismatch")
            if declaration.assertion_id in assertions:
                raise ValueError("duplicate assertion binding")
            assertions.add(declaration.assertion_id)
    return DeclarationCatalog(bridge=base, declarations=declarations)


def adapt_r8_choice(choice: LiteratureChoice) -> LiteratureDeclaration:
    """Retain the actual R8 choice content and its unverified provenance."""
    if not isinstance(choice, LiteratureChoice):
        raise TypeError("choice must be LiteratureChoice")
    return LiteratureDeclaration(
        declaration_id="choice:" + choice.assertion_id,
        reference_id="toda:" + choice.reference_locator,
        kind=DeclarationKind.CHOICE,
        defined_symbol=choice.defined_symbol,
        content=choice.statement,
        source_step=choice.source_step,
        assertion_id=choice.assertion_id,
    )


def adapt_r8_snapshot(snapshot: ChoiceSnapshot) -> DeclarationCatalog:
    if not isinstance(snapshot, ChoiceSnapshot):
        raise TypeError("snapshot must be ChoiceSnapshot")
    return register_declarations(
        snapshot.bridge, tuple(adapt_r8_choice(x) for x in snapshot.choices)
    )
