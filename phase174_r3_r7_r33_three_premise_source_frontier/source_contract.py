"""Read-only provenance contract for the three lower-Delta kernel inputs.

Only the order and exact printed clauses are certified here. A printed clause
is not an admitted proof step, and the later printed kernel must not be copied
into any source premise or proof provider.
"""
from __future__ import annotations

from dataclasses import dataclass

PROP58 = r"\begin{proposition}\label{prop:5.8}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
EQ510 = r"\begin{equation}\label{eq:5.10}"
END_PROPOSITION = r"\end{proposition}"
END_EQUATION = r"\end{equation}"
CODOMAIN_CLAUSE = r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
IMAGE_CLAUSE = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
DIAGONAL_CLAUSE = r"\pis{n}{S^n} = \z\gen{\iota_n}"
DERIVED_KERNEL = r"\ker\Delta=\gen{2\iota_{11}}"


@dataclass(frozen=True)
class SourceEvidence:
    name: str
    locator: str
    appears_before_prop59: bool
    statement_is_verified_proof_step: bool


def inspect_prior_three_clauses(text: str) -> tuple[SourceEvidence, ...]:
    """Verify order and source interval, never adopt a printed result."""
    if type(text) is not str:
        raise TypeError("Source text must be str")
    for boundary in (PROP58, PROP59, EQ510):
        if text.count(boundary) != 1:
            raise ValueError("Missing or ambiguous source boundary: " + boundary)
    p58 = text.index(PROP58)
    eq = text.index(EQ510)
    p59 = text.index(PROP59)
    if not (p58 < eq < p59):
        raise ValueError("Incorrect provenance order")
    end58 = text.find(END_PROPOSITION, p58)
    endeq = text.find(END_EQUATION, eq)
    if end58 == -1 or endeq == -1 or end58 >= eq or endeq >= p59:
        raise ValueError("Source boundary nesting is invalid")
    before = text[:p58]
    prop = text[p58:end58]
    equation = text[eq:endeq]
    later = text[p59:]
    if before.count(DIAGONAL_CLAUSE) != 1:
        raise ValueError("Earlier diagonal free-cyclic clause not unique")
    if prop.count(CODOMAIN_CLAUSE) != 1:
        raise ValueError("Proposition 5.8 codomain clause missing or ambiguous")
    if equation.count(IMAGE_CLAUSE) != 1:
        raise ValueError("Equation (5.10) generator image missing or ambiguous")
    if DERIVED_KERNEL not in later:
        raise ValueError("Later kernel statement missing; provenance unclear")
    if DERIVED_KERNEL in text[:p59]:
        raise ValueError("Derived kernel appears before the target proof")
    return (
        SourceEvidence("diagonal_domain", "general diagonal relation", True, False),
        SourceEvidence("finite_codomain", "Proposition 5.8", True, False),
        SourceEvidence("delta_generator_image", "equation (5.10)", True, False),
    )


def classify_three_premises(*, domain: bool, codomain: bool, image: bool) -> dict[str, object]:
    """False is a blocker, not a license to insert a direct GIVEN."""
    if any(type(x) is not bool for x in (domain, codomain, image)):
        raise TypeError("Every premise availability flag must be bool")
    evidence = {
        "domain_presentation": domain,
        "codomain_presentation": codomain,
        "signed_generator_image": image,
    }
    return {"premises": evidence, "all_screened": all(evidence.values()),
            "missing": tuple(k for k, v in evidence.items() if not v)}
