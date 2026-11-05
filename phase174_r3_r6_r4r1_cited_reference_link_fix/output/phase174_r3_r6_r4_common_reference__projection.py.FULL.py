"""Read-only Reference prose for previously registered, source-checked Toda laws.

The registered source assertion, not a nearby string, inferred group goal, or
bibliography heading, authorizes each formula. No inference or new GIVEN is
constructed here. A verified cited GIVEN can also supply the same formula when
an older Narrative Model lacks the registry assertion-ID binding.
"""
from __future__ import annotations

from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
)
from phase174_r3_r6_source_extension.source import Toda55UniversalDoubleStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _universal_toda_formula(statement: object) -> str | None:
    """Format the canonical typed source clause, without making it a proof."""
    if (type(statement) is Toda48UniversalConditionalStatement
            and statement == Toda48UniversalConditionalStatement()):
        return (
            r"$n$ を偶数とし, $\Delta(\iota_{2n-1})=0$ と仮定する."
            "\n"
            r"このとき $E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}$ は単射で, "
            r"$\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2$."
        )
    if (type(statement) is Toda55UniversalDoubleStatement
            and statement == Toda55UniversalDoubleStatement()):
        return r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$."
    return None


def project_cited_universal_toda_reference_body(
    assertion: object, registry: object, statement: object,
) -> str | None:
    """Display one authenticated general GIVEN, retaining its source conditions.

    A matching locator or a forged dataclass alone is never sufficient. The
    caller supplies the actual, already cited registry assertion. Source text
    checking and publication screening happen upstream, not in Renderer.
    """
    if not isinstance(assertion, AssertionEntry) or not isinstance(
        registry, UnifiedStatementRegistry
    ):
        return None

    if type(statement) is Toda48UniversalConditionalStatement:
        locator = "(4.8)"
        source_chapter = "04"
        publication_position = 7500
        canonical = Toda48UniversalConditionalStatement()
    elif type(statement) is Toda55UniversalDoubleStatement:
        locator = "(5.5)"
        source_chapter = "05"
        publication_position = 8600
        canonical = Toda55UniversalDoubleStatement()
    else:
        return None

    try:
        registered = registry.assertion(assertion.assertion_id)
    except KeyError:
        return None
    if registered is not assertion:
        return None

    if (
        statement != canonical
        or type(assertion.content) is not type(canonical)
        or assertion.content != statement
        or assertion.assertion_id != "toda:174:r3r6:universal:" + locator
        or assertion.reference_id != "toda:" + locator
        or assertion.kind is not AssertionKind.STATEMENT
        or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
        or assertion.scope != (
            "universal formula only", "no direct group conclusion",
        )
        or assertion.dependencies
    ):
        return None

    reference = registry.reference(assertion.reference_id)
    if (
        reference.reference_id != "toda:" + locator
        or reference.kind is not ReferenceKind.EQUATION
        or reference.locator != locator
        or reference.publication_position != publication_position
        or reference.source_id != (
            f"sources/toda/Toda_{source_chapter}_2.tex "
            "(adopted transcription; original edition unverified)"
        )
    ):
        return None
    return _universal_toda_formula(statement)


def project_verified_cited_toda_given_reference_body(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Recover a *display body* only from a cited and source-verified GIVEN leaf.

    This does not reconstruct registry links or promote a goal to a GIVEN.
    The cited step must have the exact canonical universal type, an explicit
    authentic source reference, and no premises. Source bytes and publication
    order are reverified; title matching alone never qualifies.
    """
    from proof import LiteratureReference, ProofRule, ProofStep
    from phase174_r3_r6_source_extension.source import verify_extension_texts

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    if locator == "(4.8)":
        canonical = Toda48UniversalConditionalStatement()
        expected_position = 7500
    elif locator == "(5.5)":
        canonical = Toda55UniversalDoubleStatement()
        expected_position = 8600
    else:
        return ()

    candidates: list[ProofStep] = []
    for step in cited_steps:
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            continue
        source_rule = step.inference_rule
        source_reference = getattr(source_rule, "literature_reference", None)
        source_locator = getattr(source_reference, "locator", None)
        source_name = getattr(source_rule, "name", None)
        if (
            step.premises
            or type(step.conclusion) is not type(canonical)
            or step.conclusion != canonical
            or source_locator != locator
            or source_name not in (
                "Cited universal Toda " + locator,
                "Registered fixed statement: " + locator,
            )
        ):
            continue
        candidates.append(step)
    if len(candidates) != 1:
        return ()

    # The adopted Toda TeX text and manifest order must still match the
    # previously checked source hashes. Do not trust an isolated citation title.
    try:
        positions = dict(verify_extension_texts())
    except (ValueError, OSError, UnicodeError):
        return ()
    if positions.get(locator) != expected_position:
        return ()
    sentence = _universal_toda_formula(candidates[0].conclusion)
    return (sentence,) if sentence is not None else ()
