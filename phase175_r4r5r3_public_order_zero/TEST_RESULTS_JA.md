# Phase 175 R4R5R3 — テスト記録

- 現行 GitHub `develop`: `2789fb6297efaa35962695b95300063feb6e2ea2`（2026年11月17日確認）。
- 先行ユーザーの R4R5R2 本実行: 限定 pytest 195 PASS、π₈⁷・π₈⁴ の隔離零関係3件 PASS、一般規則1件、GIVEN 0件、先行群再探索なし。
- R4R5R3 作成環境: 模擬依存で R4R5R2 の既存テスト＋R4R5R3 の新規 Provider／Installer テスト **82 passed**（本番リポジトリではない）。
- `test_real_integration.py` は本番実行でのみ起動。現時点で本番の統合 pytest は未実施。
- 書込対象は `phase165_r52_r9_shared_math.py` 内 `shared_expansion_provider()` だけ。インストール後、関数全文を audit レポートディレクトリに保存。
- 全体 pytest は未実施（Phase 終了時のみ実施）。
- 完了判定: ユーザー Windows 上で DryRun／本実行、追加実統合テスト、Git diff と Source Guard が PASS すること。

## R4R5R3R1 再検証

ユーザー R4R5R3 DryRun: 限定 pytest 210 passed、Source Guard `R4R5R3_UNREVIEWED_HEAD` で FAIL。共有 Provider は未接続。GitHub `develop` の `175-4-5` コミットにより HEAD が更新されたことが原因。修正版では既存内容を保ったまま HEAD 祖先・差分パス検査を追加。R4R5R3R1 新規限定テストについては本書末尾の検証記録を参照。実環境 DryRun・本実行・公開 Provider 連携はユーザー実行まで未検証。全体 pytest は未実行。

R4R5R3R1 作成環境の模擬依存限定テスト: **90 passed**（既存 R4R5R2/R4R5R3 の合計82件に HEAD 履歴の新規8件を追加）。合成 Git 履歴で、正当な追加コミット、未審査の別ファイル、別履歴、規則 SHA256 不一致の拒否を確認。Windows 上の real integration pytest は未実行、DryRun 本実行の PASS も未確認。
