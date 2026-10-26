# Phase 169 R3M1 — 同一群テストの模擬データ修正

## 確認済みの原因

`test_same_group_as_target_is_rejected` は source_n=4, source_k=2
（π₆⁴）を対象にしていたが、以前の `_stub_result` は `_relation(3)`
（π₅³）を返していた。`resolve_prior_group_result` の正しい入力検証が
先に ValueError を出し、自己参照禁止の検証に到達しなかった。

## 変更対象

- `phase169_r3m_prior_result_catalog/tests/test_prior_results.py`
  - `test_same_group_as_target_is_rejected(monkeypatch)`：全文置換。
  - テストの import、他のテスト、既存の本番コードは変更しない。
- この手順書（新規）。

## 変更後のテスト関数全文

```python
def test_same_group_as_target_is_rejected(monkeypatch):
    """The DB mock must refer to the very same group as the target."""
    same_group = _relation(4)
    monkeypatch.setattr(
        prior_results,
        "_database_result_candidates",
        lambda **kwargs: (same_group,),
    )
    result = prior_results.resolve_prior_group_result(
        _bridge(), source_n=4, source_k=2, citing_assertion_id="target_id",
    )
    assert result.relation == same_group
    assert result.source_assertion_id is None
    assert result.eligible is False
    assert result.reason == "same_group_as_target"
```

## pytest

```powershell
python -B -m pytest -q .\phase169_r3m_prior_result_catalog\tests\test_prior_results.py
```

既存 run.ps1 を利用し、成功時には証明探索を実行しない R3M の読取り専用監査も継続する。
全体 pytest は実行しない。

## 完了条件

- 限定テスト6件が成功する。
- 自己参照禁止ケースは `same_group_as_target` となる。
- DB 行の型・群番号の検証は変更せず保持する。
- 実データについて、出典の先行性を読取り専用監査で確認する。

## 次工程との境界

R3M1 は限定テスト修正のみ。検索への先行 DB 結果の接続、未確認出典の
利用資格の拡張、Narrative Renderer の変更は R3M1 では行わない。
