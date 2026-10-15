# R57-R16 変更コード全文

## 変更対象

- `phase165_r55_nk_only_goal.py`：`search_group_from_registered_goal()` 全体を置換。import は変更なし。
- 新規 `phase165_r57_r16_web_proof_order.py`：ファイル全体。既存 import への変更なし。
- 新規 `phase165_r57_r16_web_proof_order/test_phase165_r57_r16_web_proof_order.py`：対象テスト全文。
- `install.py`, `run.ps1`：配布・実行用。

## `search_group_from_registered_goal()` 全文

```python
def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None):
    """Resolve a typed goal; use reviewed on-demand proof order for ordinary calls."""
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    if bridge is None:
        bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    if len(candidates) != 1:
        explanation = (
            "群構造・生成元の型付き証明目標が文献命題台帳に未登録"
            if not candidates else
            "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
        )
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(TodaPrimaryGroup(n + k, n),),
            diagnostics=(explanation,),
        )
    candidate = candidates[0]
    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
    # Goal candidates and proof order are metadata, NEVER a GIVEN evidence source.
    result = search_shared_group_goal(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
```

## 新規モジュール全文

```python
"""R57-R16: reviewed, finite proof-use order metadata for ordinary Web queries.

This is NOT publication order, a proof assertion, or a derived group result.
Group structures are selected afresh from the typed registry. No completed
ProofStep is persisted. Unreviewed/missing/ambiguous order is fail-closed.
"""
from __future__ import annotations

from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord


# Agreed proof-development order. These are (sphere dimension, stem), NOT
# stored group answers; expanding this table requires separate review.
REVIEWED_PROOF_TARGET_ORDER: tuple[tuple[int, int], ...] = (
    (2, 1),  # pi_3^2
    (3, 1),  # pi_4^3
    (4, 1),  # pi_5^4
)


def resolve_reviewed_order_catalog(bridge, *, n: int, k: int):
    """Return a position-only catalog or a diagnostic, with no fake premises.

    Queries not covered by an explicit reviewed order retain ordinary shared
    search without a recursive catalog. Missing earlier typed goals prevent
    granting reviewed reuse; no structure is guessed from (n,k).
    """
    key = (n, k)
    if key not in REVIEWED_PROOF_TARGET_ORDER:
        return None, None
    from phase165_r55_nk_only_goal import registered_group_goal_candidates

    target_index = REVIEWED_PROOF_TARGET_ORDER.index(key)
    catalog = ProofOrderCatalog()
    for position, (source_n, source_k) in enumerate(
        REVIEWED_PROOF_TARGET_ORDER[:target_index + 1]
    ):
        candidates = registered_group_goal_candidates(
            bridge, n=source_n, k=source_k,
        )
        if len(candidates) != 1:
            reason = ("型付き証明目標が未登録" if not candidates
                      else "型付き証明目標が複数存在")
            return None, (
                "先行証明の順序データを適用できません: "
                f"π_{source_n + source_k}^{source_n} の{reason}"
            )
        catalog.register(ProofOrderRecord(
            statement=candidates[0], position=position,
        ))
    return catalog, None
```

## 新規テスト全文

```python
"""Targeted proof-order policy checks: no saved proofs or manufactured claims."""
import ast
from pathlib import Path

import pytest

from install import replace_function


PACKAGE = Path(__file__).resolve().parent


def test_reviewed_order_is_explicit_not_generated():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "REVIEWED_PROOF_TARGET_ORDER" in text
    assert "(2, 1)" in text and "(3, 1)" in text and "(4, 1)" in text
    assert "for n in range" not in text
    assert "ProofStep(" not in text
    assert "ProofRule.GIVEN" not in text


def test_catalog_uses_registered_candidates_and_no_completed_roots():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "registered_group_goal_candidates" in text
    assert "len(candidates) != 1" in text
    assert "ProofOrderRecord(" in text
    assert "completed=" not in text


def test_web_selector_supplies_catalog_automatically():
    tree = ast.parse((PACKAGE / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8"))
    fn = tree.body[0]
    assert fn.name == "search_group_from_registered_goal"
    assert [a.arg for a in fn.args.kwonlyargs] == ["n", "k", "bridge", "proof_order_catalog"]
    source = ast.unparse(fn)
    assert "resolve_reviewed_order_catalog" in source
    assert "proof_order_catalog=proof_order_catalog" in source
    assert "ProofSearchStatus.SEARCH_FAILED" in source


def test_existing_explicit_catalog_not_overwritten():
    src = (PACKAGE / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")
    assert "if proof_order_catalog is None:" in src


def test_installer_is_idempotent_and_fail_closed():
    before = "def f():\n    return 1\n"
    after = "def f():\n    return 2\n"
    output, changed = replace_function(before, "f", before, after)
    assert changed
    repeated, changed = replace_function(output, "f", before, after)
    assert not changed and repeated == output
    with pytest.raises(RuntimeError, match="unexpected"):
        replace_function("def f():\n    return 9\n", "f", before, after)


def test_outside_reviewed_scope_has_no_catalog():
    text = (PACKAGE / "phase165_r57_r16_web_proof_order.py").read_text(encoding="utf8")
    assert "if key not in REVIEWED_PROOF_TARGET_ORDER:" in text
    assert "return None, None" in text
```
