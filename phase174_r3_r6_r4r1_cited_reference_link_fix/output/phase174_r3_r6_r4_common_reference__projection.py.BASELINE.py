"""Read-only Reference prose for previously registered, source-checked Toda laws.

The registered source assertion, not a nearby string, inferred group goal, or
bibliography heading, authorizes each formula.  No inference or new GIVEN is
constructed here.  This projection applies to every valid cited instance.
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


def project_cited_universal_toda_reference_body(
    assertion: object, registry: object, statement: object,
) -> str | None:
    """Display one authenticated general GIVEN, retaining its source conditions.

    A matching locator or a forged dataclass alone is never sufficient.  The
    caller must supply the actual, already cited registry assertion.  Source
    text checking and publication screening happen upstream, not in Renderer.
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
        sentence = (
            r"$n$ を偶数とし, $\Delta(\iota_{2n-1})=0$ と仮定する."
            "\n"
            r"このとき $E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}$ は単射で, "
            r"$\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2$."
        )
    elif type(statement) is Toda55UniversalDoubleStatement:
        locator = "(5.5)"
        source_chapter = "05"
        publication_position = 8600
        canonical = Toda55UniversalDoubleStatement()
        sentence = r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$."
    else:
        return None

    # The assertion must be the object owned by this exact registry, not
    # a free-standing imitation with a convincing citation label.
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
    return sentence
