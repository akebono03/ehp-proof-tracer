"""Audit typed prose already available in the legacy shared narrative path.

No code in this module changes proof steps, search, or rendering.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from proof import ProofStep
from toda_group_proof_narrative_shared_components import (
    _render_generic_narrative_step,
    _render_generic_narrative_statement_prose,
)
from web_group_proof_common import _group_proof_statement_latex


@dataclass(frozen=True)
class ExistingProseAuditEntry:
    step_index: int
    type_name: str
    source: str
    prose: str | None
    error: str | None


def audit_existing_typed_prose(result: PartialProofResult) -> tuple[ExistingProseAuditEntry, ...]:
    """Check previously unrenderable conclusions against the shared typed prose."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    entries = []
    for index, step in enumerate(result.proven_steps):
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        if latex is not None and fallback is None:
            continue
        source = "typed_statement"
        try:
            prose = _render_generic_narrative_statement_prose(step.conclusion)
            if prose is None:
                source = "generic_step_fallback"
                prose = _render_generic_narrative_step(step)
            if not isinstance(prose, str) or not prose.strip():
                entries.append(ExistingProseAuditEntry(
                    index, type(step.conclusion).__name__, source, None,
                    "empty_or_non_string",
                ))
                continue
            entries.append(ExistingProseAuditEntry(
                index, type(step.conclusion).__name__, source, prose, None,
            ))
        except (TypeError, ValueError, AttributeError, NotImplementedError) as exc:
            entries.append(ExistingProseAuditEntry(
                index, type(step.conclusion).__name__, source, None,
                type(exc).__name__ + ": " + str(exc),
            ))
    return tuple(entries)
