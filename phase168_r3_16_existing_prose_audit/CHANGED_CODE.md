# 対象ファイル・追加位置

既存コードへの変更はありません。監査用の新規 `phase168_r3_16_existing_prose_audit.py` とテストは ZIP 内の同名位置に追加します。

## クラス・関数・import 全文

```python
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

```

## テスト全文

```python
import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_16_existing_prose_audit import audit_existing_typed_prose
from proof import ProofRule, ProofStep


def _result():
    return make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.PARTIAL,
        proven_steps=(ProofStep(conclusion="unsupported sentinel", premises=(), rule=ProofRule.GIVEN),),
    )


def test_audit_does_not_mutate_proof_steps():
    result = _result()
    before = result.proven_steps
    audit_existing_typed_prose(result)
    assert result.proven_steps == before


def test_audit_reports_step_index():
    records = audit_existing_typed_prose(_result())
    assert all(record.step_index >= 0 for record in records)


def test_wrong_argument_rejected():
    with pytest.raises(TypeError, match="PartialProofResult"):
        audit_existing_typed_prose(object())


def test_audit_entries_are_immutable():
    records = audit_existing_typed_prose(_result())
    if records:
        with pytest.raises((AttributeError, TypeError)):
            records[0].source = "changed"

```
