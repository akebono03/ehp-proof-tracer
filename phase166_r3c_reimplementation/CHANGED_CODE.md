# Phase 166 R3-C 修正再実装（段階的接続）

## 変更対象

- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` のみ。
- 追加 `phase166_r3c_reimplementation/install.py`：`install()` を新設。
- 追加 `phase166_r3c_reimplementation/tests/test_r3c_reimplementation.py`：`_source()` と4つのテスト関数を新設。
- 追加 `run.ps1`、`README.md`、本書。
- import セクションの変更なし。`reconstruct_registered_goal()`、`search_shared_group_goal()`、Renderer、既存テストは変更しない。

## 実装内容

`build_shared_typed_bridge()` 内の既存 `prefix = f"shared:{index}:"` 直前に、元の Reference ID を保持している `source` に対し以下を実行する。

```python
        # R3-C: reuse Phase 163 positions on original reference IDs before
        # shared: index namespacing. No locator or synthetic rank matching.
        from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
            connect_phase163_publication_order,
        )
        source, _publication_binding = connect_phase163_publication_order(source)
```

置換済み `build_shared_typed_bridge()` を含む **実ファイル全文** は実行時 `INSTALLED_SOURCE.py.txt` に出力する。実装前の本番ソース全体はバックアップへ保存する。今回は公開検索の引用先を表す正しい型付き ID が未確定なので、仮の `assertions[0]` に対する順序判定を有効化しない。

## pytest・完了条件・次工程

限定テストは `tests/test_r3c_reimplementation.py`、`tests/test_phase166_r3b_publication_order_binding.py`、`tests/test_phase165_r3_recursive_search.py`。Web で `$n=2,k=1$` が `generic-complete-proof` を維持するか確認する。R3-C の最終完了には、仮 ID ではない証明対象の型付き位置を接続した後、共通探索の順序ゲートの実運用テストがなお必要。全体 pytest は Phase の終了時のみ。
