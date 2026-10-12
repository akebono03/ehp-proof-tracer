"""Toda TeX as adopted citation source, distinct from typed proof eligibility."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib

from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import AssertionOrigin


class TexCitationStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TexCitationDecision:
    status: TexCitationStatus
    reason: str
    assertion_id: str
    proof_step_eligible: bool = False

    @property
    def usable_as_reference(self) -> bool:
        return self.status is TexCitationStatus.ALLOWED


def assess_adopted_tex_citation(
    bridge: RegistryBridgeResult,
    cited_assertion_id: str,
    *,
    citing_assertion_id: str | None = None,
) -> TexCitationDecision:
    """Allow source-text citation from the adopted Toda TeX, never a typed axiom.

    With a citing assertion, enforce strictly earlier source order in the same
    adopted document. Without one, allow bibliographic quotation only.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    cited = bridge.registry.assertion(cited_assertion_id)

    def decision(status: TexCitationStatus, reason: str) -> TexCitationDecision:
        return TexCitationDecision(status, reason, cited_assertion_id)

    if cited.origin is not AssertionOrigin.SOURCE_ARCHIVE:
        return decision(TexCitationStatus.DENIED, "not_adopted_tex_archive")
    body = cited.content
    if not isinstance(body, dict):
        return decision(TexCitationStatus.UNKNOWN, "archive_content_not_source_text")
    raw = body.get("source_text")
    sha = body.get("source_sha256")
    if (not isinstance(raw, str) or not raw or not isinstance(sha, str)
            or hashlib.sha256(raw.encode("utf-8")).hexdigest() != sha):
        return decision(TexCitationStatus.DENIED, "source_text_integrity_failed")
    ref = bridge.registry.reference(cited.reference_id)
    if not ref.source_id or "Toda translated TeX" not in ref.source_id:
        return decision(TexCitationStatus.UNKNOWN, "not_adopted_tex_document")
    if citing_assertion_id is None:
        return decision(TexCitationStatus.ALLOWED, "adopted_tex_source_citation")
    if cited_assertion_id == citing_assertion_id:
        return decision(TexCitationStatus.DENIED, "self_citation")
    citing = bridge.registry.assertion(citing_assertion_id)
    to_ref = bridge.registry.reference(citing.reference_id)
    if to_ref.source_id != ref.source_id:
        return decision(TexCitationStatus.UNKNOWN, "different_source_document")
    src_position = body.get("source_position")
    citing_position = citing.content.get("source_position") if isinstance(citing.content, dict) else None
    if (type(src_position) is not int or type(citing_position) is not int):
        return decision(TexCitationStatus.UNKNOWN, "source_order_not_available")
    if src_position >= citing_position:
        return decision(TexCitationStatus.DENIED, "not_prior_to_citing_statement")
    return decision(TexCitationStatus.ALLOWED, "earlier_adopted_tex_citation")
