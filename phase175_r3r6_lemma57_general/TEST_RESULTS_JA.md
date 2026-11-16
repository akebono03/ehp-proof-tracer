# Phase 175 R3R6 — 検証記録

- GitHub `akebono03/ehp-proof-tracer` `develop` の現行コード・関連テスト、Toda `sources/toda/Toda_05_2.tex` および `phase163_r4_r94_output/manifest.json` を実装前に確認。
- R3R5 の Git Source Guard と前提別独立探索のコードを確認。
- この作業環境で `python -m pytest -q -p no:cacheprovider phase175_r3r6_lemma57_general/tests` を実施：**14 passed, 1 skipped**。skip は実リポジトリ依存の型付き推論テストモジュールである。
- Windows の実リポジトリでの結果は未実測。ZIP 内 `run.ps1` が新規・既存の限定 pytest を実行する。
- Git worktree に対する本番変更 0。新規一般出典 1 は孤立監査専用。特例の新規 GIVEN 0。
- Phase 175 全体 pytest：**未実施**。
- Open Goal が残る場合、監査 Gate の PASS は群の完成証明を意味しない。

## R3R6R1（2026-11-16）：Windows の既定文字コード修正

- ユーザー実測：Windows Python 3.10、R3R6 最初の限定 pytest は **54 passed, 1 failed**。失敗は既存 R3R5 テストの UTF-8 Markdown を `cp932` で読もうとした `UnicodeDecodeError`。数学的な推論や Source Guard の結果ではない。
- GitHub `develop` の `phase175_r3r5_pi73_lemma57_frontier/tests/test_audit.py::test_report_written_outside_source_tree`、同 `audit.write_report()`、`run.ps1` の UTF-8 環境設定を修正前に確認。
- 修正：R3R6 の `run.ps1` に `PYTHONUTF8=1` と `PYTHONIOENCODING=utf-8` を追加。新規 `tests/test_powershell_utf8.py` でテスト2件を追加。**R3R5 テストは変更していない**。
- ローカル実行：`python -m pytest -q -p no:cacheprovider phase175_r3r6_lemma57_general/tests/test_powershell_utf8.py` → **2 passed**。
- 作業環境には EHP Proof Tracer の本体依存モジュールがないため、同ディレクトリ全テストの収集は `phase175_r3r5_pi73_lemma57_frontier` 不在による import error で停止した。これは Windows 本リポジトリでの限定 pytest に代わる検証結果ではない。
- Python ソース全件の構文を `compile()` で確認する。ZIP 内の R3R6 既存 Python ファイルは元の `R3R6.zip` と内容一致、既存 R3R5 のファイルは一切含まれない。
- 全体 pytest：**未実施**（Phase 175 最終段階のみ）。R3R6 の数学的な完成結果は未実測。

## R3R6R2（2026-11-16）：Git 履歴の監査スコープ修正

- ユーザー実測：R3R6R1 の限定 pytest は **57 passed**。DryRun は `RuntimeError: R3_R2_LINEAGE_NOT_AUDIT_ONLY` で停止。数学的な推論ワーカーは未実行。
- GitHub `develop` の現行 `phase175_r3_pi73_hopf_lift/audit.py::verify_lineage`、`phase175_r3r5_pi73_lemma57_frontier/audit.py::scoped_preflight`、R3R5 のテスト、R3R6R1 の現在のソース・テストを確認してから修正。
- R3R6 の `audit.py` だけで、R2→HEAD 差分中に許可する R3R5 および R3R6 の**具体的な追加ファイル**を拡張。既存 R3 の Source Guard と R2 証拠・出典検証を維持。
- 新規 `tests/test_lineage.py` は一時 Git 履歴を実際に作成して追加許可・拒否のケースを検査。
- ローカル：`python -m pytest -q -p no:cacheprovider phase175_r3r6_lemma57_general/tests` → **29 passed, 1 skipped**。skip は実リポジトリ内でだけ使える typed math 依存モジュールで、Windows 側で検証する。
- Python 構文検査 PASS。ZIP CRC / ファイル一覧を別途検証。
- Git の変更・コミット・リセット操作は監査に含まない。既存数学モジュール・既存 R3R5 テストへの変更は 0。
- Windows 本実行・出典による零関係の成立は未実測。全体 pytest は未実施。
