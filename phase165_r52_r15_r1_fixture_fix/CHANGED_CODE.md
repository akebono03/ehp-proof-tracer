# 変更一覧

- 変更するファイル: `phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py` の全文置換。
- 変更する関数: `_fixture()` 全体。
- 新規テスト: `test_ordered_reference_rejects_different_document_order()` （ファイル末尾）。
- `source_id` を両 Reference で指定。既存 `assess_citation()` の条件は変更しない。
- 本番コード: 変更なし。
- 検証: R15 6件 + Phase164 R2 + R9 の対象 pytest。全体 pytest は Phase165 終了時。
- 次境界: 確定した文献位置を使う Web 本番経路への接続。

## `_fixture()`（全体）

```python
def _fixture(*, available=1, cited_position=1, citing_position=2, dependencies=(), source_id='Toda'):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('ref', ReferenceKind.PROPOSITION, 'Proposition sample', source_id='Toda', publication_position=cited_position))
    registry.add_reference(LiteratureEntry('goal', ReferenceKind.PROPOSITION, 'Goal sample', source_id=source_id, publication_position=citing_position))
    registry.add_assertion(AssertionEntry('cited', 'ref', AssertionKind.STATEMENT, 'fact', available_after_position=available, dependencies=dependencies))
    registry.add_assertion(AssertionEntry('citing', 'goal', AssertionKind.STATEMENT, 'theorem'))
    step = ProofStep('fact', (), ProofRule.GIVEN)
    bridge = RegistryBridgeResult(registry, (MigrationRecord('test', 'cited', 'cited', MigrationStatus.STRUCTURED, 'fixture'),), (ProofStepLink('cited', step=step),))
    return bridge, step

```

## 新規テスト（全体）

```python
def test_ordered_reference_rejects_different_document_order():
    bridge, _ = _fixture(source_id='Different document')
    assert ordered_typed_reference_steps(
        bridge, 'fact', 'citing', verified_assertion_ids=('cited',)
    ) == ()
```

既存 import は変更なし。置換用テストファイルには import 部分を含む全文を収録。
