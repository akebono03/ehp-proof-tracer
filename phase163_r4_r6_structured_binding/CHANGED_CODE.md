# Phase 163 R4-R6 — 変更・コード全文

## 対象

- **新規** `phase163_r4_r6_structured_binding.py`: `FixedStatementBinding`, `bind_verified_fixed_statements`
- **新規** `tests/test_phase163_r4_r6_structured_binding.py`: 7つの軽量テスト
- **新規** `run.ps1`, `README.txt`
- 既存コードは変更しない。新規関数・クラスの追加位置は、新規の独立モジュール内。

## 設計境界

- `build_registry_bridge()` は既存のまま動作し、境界67件を `metadata_only` に維持する。
- 既存 `validate_cited_fixed_statement()` で検証できる引用 `ProofStep` を**明示的に渡した場合に限り**、指定の1件を構造化する。
- `FixedStatementBinding.expected_conclusion` は `ProofStep.conclusion` と厳密一致させる。
- 原本の台帳は変更せず、新しいスナップショットを返す。元となるメタデータは選択した成分のみ置換。
- これは引用境界と内容の一致検証。文献原本の数学的真偽・外部出典の確定ではない。
- テスト内の `Relation(lhs="H(nu_prime)", rhs="eta_5")` は接続契約を確かめる**テスト用の構造化オブジェクト**。本番の Toda 型の同一性を確認したものではない。
- Proposition 5.6 等の実際の既存 `ProofStep` を受け渡す接続・自動的な67件移行は未実施。
- 引用可否判定、一般型変数の具体化、Backward Search / Renderer、既存 Repository の書換えは範囲外。

## 新規モジュール（全文）

```python
"""Phase 163 R4-R6: opt-in typed binding of existing verified citation steps.

No automatic theorem discovery, proof execution, or citation permission is added.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from phase162_reference_boundary import validate_cited_fixed_statement
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from proof import ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    ProofStepLink,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class FixedStatementBinding:
    """Explicit association supplied after existing citation ancestry verification."""

    reference_locator: str
    component_key: str
    citation_step: ProofStep
    expected_conclusion: object

    def __post_init__(self) -> None:
        if not isinstance(self.reference_locator, str) or not self.reference_locator:
            raise ValueError("reference_locator is required")
        if not isinstance(self.component_key, str) or not self.component_key:
            raise ValueError("component_key is required")
        if not isinstance(self.citation_step, ProofStep):
            raise TypeError("citation_step must be a ProofStep")
        if self.expected_conclusion is None:
            raise ValueError("expected_conclusion is required")


def bind_verified_fixed_statements(
    base: RegistryBridgeResult,
    bindings: tuple[FixedStatementBinding, ...],
) -> RegistryBridgeResult:
    """Return a new registry snapshot with selected metadata entries typed.

    This checks an *existing* verified-citation boundary, not the external
    truth of a theorem. The original bridge snapshot is never mutated.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be a RegistryBridgeResult")
    if not isinstance(bindings, tuple):
        raise TypeError("bindings must be a tuple")

    selected: dict[str, FixedStatementBinding] = {}
    for binding in bindings:
        if not isinstance(binding, FixedStatementBinding):
            raise TypeError("bindings must contain FixedStatementBinding")
        identifier = f"boundary:{binding.reference_locator}:{binding.component_key}"
        if identifier in selected:
            raise ValueError(f"duplicate binding: {identifier}")
        # Existing validator checks the registered locator, component, identity,
        # citation shape and exact typed conclusion.
        validate_cited_fixed_statement(
            binding.citation_step,
            binding.reference_locator,
            binding.component_key,
            binding.expected_conclusion,
        )
        selected[identifier] = binding

    eligible = {
        record.assertion_id
        for record in base.records
        if record.source == "boundary"
        and record.status is MigrationStatus.METADATA_ONLY
    }
    if not set(selected).issubset(eligible):
        unknown = sorted(set(selected) - eligible)
        raise ValueError(f"binding is not a metadata-only boundary: {unknown}")

    result = UnifiedStatementRegistry()
    seen_refs: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        assertion = base.registry.assertion(record.assertion_id)
        if assertion.reference_id not in seen_refs:
            result.add_reference(base.registry.reference(assertion.reference_id))
            seen_refs.add(assertion.reference_id)
        if record.assertion_id in selected:
            binding = selected[record.assertion_id]
            assertion = replace(
                assertion, content=binding.citation_step.conclusion,
                kind=AssertionKind.STATEMENT,
            )
        result.add_assertion(assertion)

    records: list[MigrationRecord] = []
    proof_links: list[ProofStepLink] = list(base.proof_links)
    for record in base.records:
        if record.assertion_id in selected:
            binding = selected[record.assertion_id]
            records.append(replace(
                record,
                status=MigrationStatus.STRUCTURED,
                detail="Typed conclusion from existing verified citation boundary; not independently literature-verified",
            ))
            proof_links.append(ProofStepLink(
                assertion_id=record.assertion_id,
                step=binding.citation_step,
            ))
        else:
            records.append(record)

    return RegistryBridgeResult(result, tuple(records), tuple(proof_links))
```

## 新規テスト（import と全テスト全文）

```python
from dataclasses import replace

import pytest

from phase163_r4_r6_structured_binding import (
    FixedStatementBinding,
    bind_verified_fixed_statements,
)
from phase163_r4_registry_bridge import (
    MigrationStatus,
    build_registry_bridge,
)
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
)
from toda_literature_statement_boundary import get_toda_fixed_statement_component


LOCATOR = "(5.3)"
COMPONENT = "nu_prime_hopf_relation"


def _citation(conclusion):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{LOCATOR}:{COMPONENT}",
        label=LOCATOR,
    )
    leaf = ProofStep(
        conclusion=conclusion,
        premises=(),
        rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=conclusion,
        premises=(leaf,),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda (5.3)", locator=LOCATOR),
        ),
        foundational_reference=identity,
    )


def _binding():
    statement = Relation(lhs="H(nu_prime)", rhs="eta_5")
    return FixedStatementBinding(
        reference_locator=LOCATOR,
        component_key=COMPONENT,
        citation_step=_citation(statement),
        expected_conclusion=statement,
    )


def test_r4_r6_upgrades_only_selected_component():
    base = build_registry_bridge()
    binding = _binding()
    result = bind_verified_fixed_statements(base, (binding,))
    key = f"boundary:{LOCATOR}:{COMPONENT}"
    assert result.registry.assertion(key).content is binding.citation_step.conclusion
    assert result.registry.assertion(key).reference_id == f"toda:{LOCATOR}"
    assert len(result.proof_links) == len(base.proof_links) + 1
    assert next(r for r in result.records if r.assertion_id == key).status is MigrationStatus.STRUCTURED
    assert next(r for r in base.records if r.assertion_id == key).status is MigrationStatus.METADATA_ONLY
    assert base.registry.assertion(key).content == get_toda_fixed_statement_component(LOCATOR, COMPONENT)


def test_r4_r6_keeps_other_components_metadata_only():
    base = build_registry_bridge()
    result = bind_verified_fixed_statements(base, (_binding(),))
    for record in base.records:
        if record.assertion_id != f"boundary:{LOCATOR}:{COMPONENT}":
            assert next(r for r in result.records if r.source == record.source and r.source_key == record.source_key) == record


def test_r4_r6_rejects_mismatch():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(ValueError, match="Invalid fixed-statement citation"):
        bind_verified_fixed_statements(base, (replace(binding, expected_conclusion="false"),))


def test_r4_r6_rejects_unverified_witness():
    base = build_registry_bridge()
    binding = _binding()
    bad = replace(binding.citation_step, inference_rule=InferenceRule(name="not_verified"))
    with pytest.raises(ValueError, match="Invalid fixed-statement citation"):
        bind_verified_fixed_statements(base, (replace(binding, citation_step=bad),))


def test_r4_r6_rejects_unregistered_component():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(KeyError):
        bind_verified_fixed_statements(base, (replace(binding, component_key="invented"),))


def test_r4_r6_rejects_duplicate_binding():
    base = build_registry_bridge()
    binding = _binding()
    with pytest.raises(ValueError, match="duplicate binding"):
        bind_verified_fixed_statements(base, (binding, binding))


def test_r4_r6_empty_is_unchanged():
    base = build_registry_bridge()
    result = bind_verified_fixed_statements(base, ())
    assert result.records == base.records
    assert result.proof_links == base.proof_links
```

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase163_r4_r6_structured_binding.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r6_structured_binding\run.ps1"
```

実行する pytest: `python -m pytest -q tests/test_phase163_r4_r6_structured_binding.py`。
全体 pytest は Phase 163 最終段階のみ。

## 完了条件

- 明示された引用境界の構造化、未指定の成分の保持、原本不変、入力不正の拒否が PASS。
- 全件登録・数学的同一性確定は完了条件に含めない。

## 次フェーズとの境界

- R4 後続: 既存の実際の `ProofStep` と Definition の段階的対応、網羅性の監査。
- Phase 164: Search engine の統一台帳利用。R4-R6 で先取りしない。
