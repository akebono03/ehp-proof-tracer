# R57-R13 変更コード全文

## 変更対象
- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal()` のみ置換。import変更なし。
- 新規 `phase165_r57_r13_proof_order_catalog.py`: `phase165_r52_r9_shared_math.py` と同じ階層へ新規追加。import全文・全クラスを含む。
- 新規 `phase165_r57_r13_proof_order_catalog/test_phase165_r57_r13_proof_order_catalog.py`: テスト全文。
- `run.ps1` と `install.py`: 導入用。

## search_shared_group_goal() 全文
```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None,
                              proof_order_catalog=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    if proof_order_catalog is not None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot be mixed with caller order")
        prior, target_order = proof_order_catalog.select_prior(goal)
    else:
        prior = validate_prior_internal_proofs(
            ordered_completed_proofs, target_order, completed_internal_proofs
        )
    if bridge is None:
        bridge = build_shared_typed_bridge()
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
    )
    if proof_use_order == "registered":
        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)
    if proof_use_order is not None:
        from phase165_r52_r18_proof_order import restrict_by_proof_use_order
        proof_context = restrict_by_proof_use_order(
            proof_context, goal=goal, policy=proof_use_order,
        )
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )
```

## 新規 catalog モジュール全文
```python
"""R57-R13: registered, strictly earlier internal proof lookup.

Order positions are reviewed proof-use metadata, not publication order or
an inference from group dimensions. No repository replay is performed.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_r17_internal_dependency import (
    CompletedInternalProof,
    depends_on,
    same_statement,
    validate_ancestry,
)
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof, validate_prior_internal_proofs
from proof import ProofStep


@dataclass(frozen=True)
class ProofOrderRecord:
    """Registered target with an independently reviewed proof-use position."""
    statement: object
    position: int
    completed: CompletedInternalProof | None = None

    def __post_init__(self) -> None:
        if self.statement is None:
            raise ValueError("statement is required")
        if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position < 0:
            raise ValueError("position must be a nonnegative integer")
        if self.completed is not None:
            if not isinstance(self.completed, CompletedInternalProof):
                raise TypeError("completed must be CompletedInternalProof")
            validate_ancestry(self.completed.root)
            if not same_statement(self.completed.root.conclusion, self.statement):
                raise ValueError("registered proof does not prove its statement")


class ProofOrderCatalog:
    """Register reviewed positions once; look up prior proof steps per goal."""

    def __init__(self) -> None:
        self._records: list[ProofOrderRecord] = []

    def register(self, record: ProofOrderRecord) -> None:
        if not isinstance(record, ProofOrderRecord):
            raise TypeError("record must be ProofOrderRecord")
        if any(same_statement(item.statement, record.statement) for item in self._records):
            raise ValueError("duplicate target statement")
        if any(item.position == record.position for item in self._records):
            raise ValueError("duplicate proof position")
        self._records.append(record)

    def select_prior(self, goal: object) -> tuple[tuple[CompletedInternalProof, ...], int]:
        """Fail closed without a registered target; exclude current/later roots."""
        matches = [item for item in self._records if same_statement(item.statement, goal)]
        if len(matches) != 1:
            raise ValueError("target has no unique registered proof order")
        target = matches[0]
        earlier = sorted(
            (item for item in self._records if item.position < target.position and item.completed is not None),
            key=lambda item: item.position,
        )
        ordered = []
        for item in earlier:
            assert item.completed is not None
            validate_ancestry(item.completed.root)
            if depends_on(item.completed.root, goal):
                raise ValueError("earlier proof depends on current goal")
            ordered.append(OrderedCompletedProof(item.completed, item.position))
        return validate_prior_internal_proofs(tuple(ordered), target.position), target.position
```

## テスト全文
```python
"""R57-R13: lookup earlier completed proofs from reviewed catalog records."""
import pytest

from phase165_r52_r17_internal_dependency import CompletedInternalProof
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep


def _complete(statement):
    source = ProofStep(conclusion="sourced premise: " + statement, premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(
        name="test generic deduction",
        premise_patterns=(PremisePattern(statement_type=str),),
        conclusion_builder=lambda steps: statement,
    )
    return CompletedInternalProof(ProofStep(
        conclusion=statement, premises=(source,), rule=ProofRule.INFERENCE,
        inference_rule=rule,
    ))


def test_catalog_selects_earlier_completed_proofs_without_query_order():
    catalog = ProofOrderCatalog()
    earlier = _complete("earlier result")
    later = _complete("later result")
    catalog.register(ProofOrderRecord("earlier result", 4, earlier))
    catalog.register(ProofOrderRecord("target result", 5))
    catalog.register(ProofOrderRecord("later result", 6, later))
    reusable, target_position = catalog.select_prior("target result")
    assert target_position == 5
    assert reusable == (earlier,)


def test_catalog_fails_closed_when_target_order_missing():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("earlier result", 4, _complete("earlier result")))
    with pytest.raises(ValueError, match="registered proof order"):
        catalog.select_prior("unknown target")


def test_catalog_rejects_duplicates_and_unverified_positions():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord("A", 0))
    with pytest.raises(ValueError, match="duplicate proof position"):
        catalog.register(ProofOrderRecord("B", 0))
    with pytest.raises(ValueError, match="duplicate target"):
        catalog.register(ProofOrderRecord("A", 1))
    with pytest.raises(ValueError, match="position"):
        ProofOrderRecord("B", True)


def test_catalog_rejects_mismatched_proof_conclusion():
    with pytest.raises(ValueError, match="does not prove"):
        ProofOrderRecord("goal", 2, _complete("other goal"))


def test_shared_search_has_catalog_parameter_after_install():
    from inspect import signature
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert "proof_order_catalog" in signature(search_shared_group_goal).parameters


def test_shared_search_rejects_unknown_catalog_order_before_search():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    with pytest.raises(ValueError, match="registered proof order"):
        search_shared_group_goal(n=4, k=1, group_structure="unregistered candidate",
                                 proof_order_catalog=ProofOrderCatalog())
```

## 実行 pytest
```powershell
python -m pytest -q phase165_r57_r13_proof_order_catalog/test_phase165_r57_r13_proof_order_catalog.py
python -m pytest -q phase165_r57_r12_ordered_internal_transport/test_phase165_r57_r12_ordered_internal_transport.py
python -m pytest -q phase165_r57_r11_proof_order_gate/test_phase165_r57_r11_proof_order_gate.py
```

## 完了条件
- 既に登録された順位だけから先行完成 ProofStep を検索時に取得する。
- 同順位・後順位、循環、順位不明、重複登録を拒否する。
- 既存の R57-R12 と R57-R11 の関連テストに回帰がない。

## 次段階との境界
- 群全体の正式順位の採番・登録と $\pi_4^3$ の内部完成証明の台帳登録は次段階。
- Toda (4.5) の具体同型と $E(\eta_3)=\eta_4$ の証明接続は次段階。
