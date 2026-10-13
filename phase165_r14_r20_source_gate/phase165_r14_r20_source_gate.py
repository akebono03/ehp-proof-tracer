"""R14-R20: check explicit adopted-TeX diagonal source, keep Prop 4.2 unapproved."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r14_r19_registry_gate import (
    DiagonalSourceReview,
    reviewed_diagonal_bridge,
)
from phase165_r14_r14_diagonal_and_prop42 import review_prop42_scope
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge

DIAGONAL_IDS = (
    "phase165:r14r19:toda51:diagonal:n1",
    "phase165:r14r19:toda51:diagonal:n2",
)


@dataclass(frozen=True)
class AdoptedTextReview:
    """Explicit adopted source text supplied for review; not original-edition certification."""
    source_text: str
    reviewer_confirmed_scope: bool = False


def diagonal_text_matches(review: AdoptedTextReview) -> bool:
    """Check the complete diagonal clause and adjoining stable notation exactly."""
    if not isinstance(review, AdoptedTextReview):
        raise TypeError("AdoptedTextReview required")
    text = " ".join(review.source_text.split())
    return (
        r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z" in text
        and r"G_0=\gen{\iota}\cong \mathbb Z" in text
        and r"\iota=E^{\infty}\iota_n" in text
        and r"\pi^{1}_{i}=0" in text
    )


def source_scoped_reviewed_bridge(base, review: AdoptedTextReview | None):
    """Require source span AND independent affirmative scope review."""
    if review is None or not diagonal_text_matches(review):
        return base, (), "SOURCE_SCOPE_MISSING"
    if not review.reviewer_confirmed_scope:
        return base, (), "EXPLICIT_REVIEW_REQUIRED"
    return reviewed_diagonal_bridge(
        base,
        DiagonalSourceReview(
            assertion_ids=DIAGONAL_IDS,
            adopted_tex_clause_confirmed=True,
            original_edition_confirmed=False,
        ),
    )


def prop42_candidate_report(bridge):
    """Never infer EHP exactness from locator alone."""
    rows = review_prop42_scope(bridge)
    return tuple({
        "assertion_id": row["assertion_id"],
        "source_text": row["source_text"],
        "scope_certified": False,
        "proof_eligible": False,
    } for row in rows)


def audit_r20():
    base, _ = build_phase165_r5_manifest_bridge()
    before = (len(base.registry._assertions), len(base.proof_links))
    bridge, ids, status = source_scoped_reviewed_bridge(base, None)
    candidates = prop42_candidate_report(base)
    assert bridge is base and before == (
        len(base.registry._assertions), len(base.proof_links)
    )
    return {
        "phase": "165 R14-R20",
        "source_scope_review_gate": status,
        "reviewed_diagonal_entries_added": len(ids),
        "prop42_candidates": candidates,
        "prop42_certified": False,
        "new_proof_steps": 0,
        "pi32_proved": False,
        "full_pytest_run": False,
        "status": "SOURCE_SCOPE_GATE_IMPLEMENTED_REVIEW_STILL_REQUIRED",
    }
