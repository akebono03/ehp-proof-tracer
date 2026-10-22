"""Audit exact sources attached to proof steps without changing proof evidence."""
from __future__ import annotations

from dataclasses import dataclass

from phase168_r3_3_proof_narrative_model import ProofNarrativeModel


@dataclass(frozen=True)
class CitationOrigin:
    number: int
    locator: str
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...]
    rule_names: tuple[str, ...]
    source_kind: str
    duplicate_locator_of: int | None


@dataclass(frozen=True)
class CitationOriginReport:
    origins: tuple[CitationOrigin, ...]
    distinct_locators: tuple[str, ...]
    expected_locators: tuple[str, ...]
    unexpected_locators: tuple[str, ...]
    missing_locators: tuple[str, ...]
    repeated_locators: tuple[str, ...]

    @property
    def matches_expected_sources(self) -> bool:
        return not self.unexpected_locators and not self.missing_locators


def inspect_citation_origins(
    model: ProofNarrativeModel,
    *,
    expected_locators: tuple[str, ...] = ("(5.1)", "Proposition 5.1"),
) -> CitationOriginReport:
    """Inspect cited rule provenance; never discard a source or assert proof validity.

    A shared locator is reported as a duplicate candidate, not automatically
    merged: a displayed locator is not a complete bibliographic identity.
    """
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if not isinstance(expected_locators, tuple) or not all(
        isinstance(locator, str) and locator.strip() for locator in expected_locators
    ):
        raise TypeError("expected_locators must be a tuple of nonempty strings")
    seen: dict[str, int] = {}
    origins: list[CitationOrigin] = []
    repeated: list[str] = []
    for citation in model.citations:
        locator = (citation.reference.locator or citation.reference.label).strip()
        prior = seen.get(locator)
        if prior is None:
            seen[locator] = citation.number
        elif locator not in repeated:
            repeated.append(locator)
        names: list[str] = []
        for index in citation.step_indices:
            if index < 0 or index >= len(model.steps):
                raise ValueError("citation refers to a nonexistent proof step")
            rule = model.steps[index].inference_rule
            if rule is not None and rule.name not in names:
                names.append(rule.name)
        if citation.assertion_ids and names:
            kind = "linked_assertion_and_inference_rule"
        elif citation.assertion_ids:
            kind = "linked_assertion"
        elif names:
            kind = "inference_rule"
        else:
            kind = "unattributed"
        origins.append(CitationOrigin(
            number=citation.number,
            locator=locator,
            step_indices=citation.step_indices,
            assertion_ids=citation.assertion_ids,
            rule_names=tuple(names),
            source_kind=kind,
            duplicate_locator_of=prior,
        ))
    actual = tuple(seen)
    return CitationOriginReport(
        origins=tuple(origins),
        distinct_locators=actual,
        expected_locators=expected_locators,
        unexpected_locators=tuple(x for x in actual if x not in expected_locators),
        missing_locators=tuple(x for x in expected_locators if x not in actual),
        repeated_locators=tuple(repeated),
    )
