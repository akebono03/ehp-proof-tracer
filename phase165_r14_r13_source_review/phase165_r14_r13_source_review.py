"""R14-R13 read-only semantic source review, not proof certification."""
from __future__ import annotations

from dataclasses import dataclass
from homotopy_groups import (
    TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement,
)
from phase165_r14_r12_registry_obligations import bind_delta_zero_obligations
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


@dataclass(frozen=True)
class ExactnessSourceReview:
    assertion_id: str
    locator: str
    source_text: str
    exactness_words_found: bool
    typed_specialization_verified: bool = False
    proof_eligible: bool = False


def collect_prop42_source_reviews(bridge):
    """Preserve entire archived source text; avoid choosing a false candidate."""
    obligation = bind_delta_zero_obligations(bridge)[1]
    rows = []
    for assertion_id in obligation.source_assertion_ids:
        assertion = bridge.registry.assertion(assertion_id)
        content = assertion.content
        if not isinstance(content, dict):
            raise TypeError("archive source must be a dictionary")
        source = content.get("source_text")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("archive source text missing")
        ref = bridge.registry.reference(assertion.reference_id)
        rows.append(ExactnessSourceReview(
            assertion_id=assertion_id,
            locator=ref.locator,
            source_text=source,
            exactness_words_found=("exact" in source.lower() or "完全" in source),
        ))
    return tuple(rows)


def diagonal_suspension_requirements():
    """The cyclic groups and generator suspension are independent obligations."""
    goal = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    )
    return {
        "goal": repr(goal),
        "method": "DIAGONAL_GENERATOR_TRANSPORT",
        "requirements": [
            "pi_1^1 = Z{iota_1}",
            "pi_2^2 = Z{iota_2}",
            "E(iota_1) = iota_2",
            "free_cyclic_generator_map_implies_isomorphism",
        ],
        "certified": False,
    }


def audit_r13(bridge=None):
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    before = (len(bridge.registry._assertions), len(bridge.proof_links))
    reviews = collect_prop42_source_reviews(bridge)
    after = (len(bridge.registry._assertions), len(bridge.proof_links))
    if before != after:
        raise RuntimeError("read-only source audit mutated the registry")
    return {
        "phase": "165 R14-R13",
        "mode": "READ_ONLY_SOURCE_TEXT_AND_DIAGONAL_SUSPENSION_REVIEW",
        "source_review_count": len(reviews),
        "source_reviews": [
            {"assertion_id": r.assertion_id, "locator": r.locator,
             "source_text": r.source_text,
             "exactness_words_found": r.exactness_words_found,
             "typed_specialization_verified": r.typed_specialization_verified,
             "proof_eligible": r.proof_eligible}
            for r in reviews
        ],
        "diagonal_suspension": diagonal_suspension_requirements(),
        "proposition42_single_clause_selected": False,
        "mathematical_semantics_certified": False,
        "proof_steps_created": 0,
        "pi32_proved": False,
        "full_pytest_run": False,
        "status": "SOURCE_CANDIDATES_VISIBLE_SPECIALIZATION_PENDING",
    }
