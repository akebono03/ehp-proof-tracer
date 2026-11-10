# R52R2 監査計画

- 監査済み GitHub `develop` HEAD: `0d0b6b31582ff3e505d14fdde5eaf5e9a0b343d7`。
- 失敗条件: `next(iter(original_bridge.registry._assertions))` は辞書キー `str` を返すため、`.assertion_id` の参照が `AttributeError` となる。
- 修正: `next(iter(original_bridge.registry._assertions.values())).assertion_id` に置換する。
- 既存の `Source Guard`、引用元の Registry、R35 数学的推論規則、Provider、Web、Renderer は変更しない。
- 変更対象（既存）: `phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py` の `inspect_public_kernel_source_bound_probe()` 全体。`tests/test_static.py` に新規テスト関数を末尾追加。
- 変更対象（新規）: R52R2 ディレクトリの `patch.py`、`run.ps1`、`tests/test_patch.py`、説明文書。新規テストの追加位置は `tests/test_static.py` の既存の最終テスト関数の後。
- 適用順: Source Guard → 変更前ハッシュ検証 → DryRun → 変更後ハッシュ検証 → R52 監査 → R52 限定 pytest → R52R2 パッチテスト。
- 完了条件: R52 本監査が例外なく完走、R52/R52R2 の限定 pytest PASS。プローブ結果が `partial` の場合も、未解決を誠実に報告する。
- 次の R53 との境界: R52 の実測結果の解析までは公開 Provider を変更しない。Phase 174 全体 pytest は最後にのみ実行。
