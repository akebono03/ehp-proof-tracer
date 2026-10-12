# Phase 164 R7-R8 変更後のコード

## 変更対象

- `phase164_r7_statement_resolution.py` — `resolve_registered_statement()` 全体（import 変更なし）
- `phase164_r4_r8_registry_reconstruction.py` — `reconstruct_phase164_r4_r8_pi5_3()` 全体と import 部分
- `tests/test_phase164_r7_r8_fixed_literature_resolution.py` — 新規ファイル全文

## 共通 resolver（全文）

```python
"""Phase 164 R7: read-only, fail-closed statement resolution.

Registry identities are canonical; a proof repository is only a storage backend.
This module neither creates ProofSteps nor changes citation eligibility.
"""
from dataclasses import dataclass
from typing import Any

from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from unified_statement_registry import AssertionEntry, AssertionOrigin, LiteratureEntry, ProofStepLink


@dataclass(frozen=True)
class ResolvedStatement:
    assertion: AssertionEntry
    reference: LiteratureEntry
    migration_status: MigrationStatus
    proof_link: ProofStepLink | None


def resolve_registered_statement(
    bridge: RegistryBridgeResult,
    assertion_id: str,
    *,
    proof_repository: Any = None,
    expected_conclusion: Any = None,
    citing_assertion_id: str | None = None,
    verified_assertion_ids: tuple[str, ...] = (),
    confirmed_fixed_step: Any = None,
    confirmed_source_locator: str | None = None,
    source_confirmation_recorded: bool = False,
) -> ResolvedStatement:
    """Resolve one assertion without treating registration as proof verification.

    When citing_assertion_id is specified, require the existing R2 citation
    policy to allow the reference. A proof link is checked against the actual
    repository entry if one is supplied. No arbitrary link is proof eligible.
    """
    fixed_mode = confirmed_fixed_step is not None
    if fixed_mode:
        if source_confirmation_recorded is not True:
            raise ValueError("fixed source confirmation required")
        if not isinstance(confirmed_source_locator, str) or not confirmed_source_locator:
            raise ValueError("fixed source locator required")
        if citing_assertion_id is not None or verified_assertion_ids:
            raise ValueError("fixed source confirmation is not R2 citation approval")
    elif source_confirmation_recorded or confirmed_source_locator is not None:
        raise ValueError("fixed source confirmation requires an actual proof step")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(assertion_id, str) or not assertion_id.strip():
        raise ValueError("assertion_id must be nonempty")
    assertion = bridge.registry.assertion(assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    records = tuple(record for record in bridge.records if record.assertion_id == assertion_id)
    if len(records) != 1:
        raise ValueError("migration record missing or ambiguous")
    status = records[0].status
    if status is not MigrationStatus.STRUCTURED:
        raise ValueError(f"assertion not structured: {status.value}")
    if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE:
        raise ValueError("source_archive_not_verified")
    if fixed_mode:
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            raise ValueError("confirmed fixed statement must be FIXED_STATEMENT")
        if assertion.dependencies:
            raise ValueError("confirmed fixed statement must have no dependencies")
        if reference.locator != confirmed_source_locator:
            raise ValueError("confirmed fixed source locator mismatch")
        if reference.publication_position is not None or assertion.available_after_position is not None:
            raise ValueError("confirmed fixed statement publication boundary changed")
        if assertion.content is not confirmed_fixed_step.conclusion:
            raise ValueError("confirmed fixed statement conclusion identity mismatch")

    if expected_conclusion is not None:
        if type(assertion.content) is not type(expected_conclusion):
            raise ValueError("registered conclusion type mismatch")
        equality = assertion.content == expected_conclusion
        if type(equality) is not bool or not equality:
            raise ValueError("registered conclusion mismatch")

    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
    if len(links) > 1:
        raise ValueError("ambiguous ProofStepLink")
    link = links[0] if links else None
    if link is not None:
        if fixed_mode:
            if link.repository_key is not None or link.step is not confirmed_fixed_step:
                raise ValueError("confirmed fixed literature ProofStep identity mismatch")
        elif assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("fixed literature cannot inherit internal proof link")
        step = link.step
        if proof_repository is not None and link.repository_key is not None:
            repository_step = proof_repository.get(link.repository_key).step
            if step is not None and step is not repository_step:
                raise ValueError("proof link/repository identity mismatch")
            step = repository_step
        if step is not None:
            if type(step.conclusion) is not type(assertion.content):
                raise ValueError("proof link conclusion type mismatch")
            equality = step.conclusion == assertion.content
            if type(equality) is not bool or not equality:
                raise ValueError("proof link conclusion mismatch")

    if fixed_mode and link is None:
        raise ValueError("confirmed fixed literature requires a ProofStepLink")

    if citing_assertion_id is not None:
        eligibility = assess_phase164_r2_citation(
            bridge, assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not eligibility.usable:
            raise ValueError(
                f"citation not eligible: {assertion_id}: "
                f"{eligibility.status.value}/{eligibility.reason}"
            )
    return ResolvedStatement(assertion, reference, status, link)

```

## π₅³ 変更後 import 全文

```python
"""Phase 164 R4-R8: reconstruct pi_5^3 using two registered fixed references."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    reconstruct_phase161_r7_validated_goal,
    validate_phase161_r7_provenance,
)
from phase163_r3_registry_validation import audit_dependencies
from phase163_r4_registry_bridge import MigrationStatus
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r7_statement_resolution import resolve_registered_statement
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin

```

## 新規テストファイル全文

```python
"""Phase 164 R7-R8: special fixed-literature resolution stays separate from R2 citation."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r6_typed_binding import register_phase164_r4_r6_typed_bindings
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from phase164_r7_statement_resolution import resolve_registered_statement
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope="module")
def source_case():
    leaves = build_phase59_3_data()["premise_steps"]
    literature = tuple(step for step in leaves if step.rule is ProofRule.INFERENCE)
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    registration = register_phase164_r4_r6_typed_bindings(
        crosswalk, literature, user_confirmed_original=True,
    )
    return crosswalk, leaves, literature, registration


def _resolve(registration, index=0, **kwargs):
    binding = registration.bindings[index]
    arguments = dict(
        expected_conclusion=binding.step.conclusion,
        confirmed_fixed_step=binding.step,
        confirmed_source_locator=binding.locator,
        source_confirmation_recorded=True,
    )
    arguments.update(kwargs)
    return resolve_registered_statement(registration.bridge, binding.assertion_id, **arguments)


def test_r78_both_confirmed_references_preserve_exact_proof_steps(source_case):
    _, _, _, reg = source_case
    for index in range(2):
        resolved = _resolve(reg, index)
        assert resolved.assertion.origin is AssertionOrigin.FIXED_STATEMENT
        assert resolved.proof_link is reg.bridge.proof_links[index]
        assert resolved.proof_link.step is reg.bindings[index].step
        assert resolved.reference.publication_position is None
        assert resolved.assertion.available_after_position is None


def test_r78_requires_original_source_confirmation(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="source confirmation"):
        _resolve(reg, source_confirmation_recorded=False)


def test_r78_rejects_wrong_locator(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="locator mismatch"):
        _resolve(reg, confirmed_source_locator="(5.4)")


def test_r78_rejects_cloned_step(source_case):
    _, _, _, reg = source_case
    altered = replace(reg.bindings[0].step)
    with pytest.raises(ValueError, match="conclusion identity mismatch|ProofStep identity mismatch"):
        _resolve(reg, confirmed_fixed_step=altered)


def test_r78_does_not_grant_r2_citation(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="not R2 citation approval"):
        _resolve(reg, citing_assertion_id=reg.bindings[1].assertion_id)


def test_r78_ordinary_resolver_still_rejects_fixed_proof_link(source_case):
    _, _, _, reg = source_case
    with pytest.raises(ValueError, match="fixed literature cannot inherit internal proof link"):
        resolve_registered_statement(reg.bridge, reg.bindings[0].assertion_id)


def test_r78_rejects_changed_availability_position(source_case):
    _, _, _, reg = source_case
    assertion = reg.bridge.registry.assertion(reg.bindings[0].assertion_id)
    # mutate the local isolated registry only; never change production data
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    new_registry = UnifiedStatementRegistry()
    for b in reg.bindings:
        ref = reg.bridge.registry.reference("toda:" + b.locator)
        new_registry.add_reference(ref)
        old = reg.bridge.registry.assertion(b.assertion_id)
        new_registry.add_assertion(replace(old, available_after_position=1) if b.assertion_id == assertion.assertion_id else old)
    mutated = RegistryBridgeResult(new_registry, reg.bridge.records, reg.bridge.proof_links)
    with pytest.raises(ValueError, match="publication boundary changed"):
        resolve_registered_statement(
            mutated, assertion.assertion_id,
            expected_conclusion=reg.bindings[0].step.conclusion,
            confirmed_fixed_step=reg.bindings[0].step,
            confirmed_source_locator=reg.bindings[0].locator,
            source_confirmation_recorded=True,
        )


def test_r78_existing_pi53_proof_reconstructs(source_case):
    crosswalk, leaves, _, _ = source_case
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, _known_trusted_roots(leaves),
        user_confirmed_original=True,
    )
    assert len(result.validated.reconstruction.derived_steps) == 7
    assert result.citation_mode == "confirmed_fixed_literature"

```

変更関数の全文はインストール後の `phase164_r4_r8_registry_reconstruction.py` 内にあり、パッケージ適用では当該関数内の検証部分を一括で置き換えます。
