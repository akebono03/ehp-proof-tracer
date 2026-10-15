# Phase 165 R5-R9 監査設計

## 対象

- `phase162_web_narrative_integration.py`（旧 Web Narrative および `_phase162_ehp_leaves`）
- `phase162_r3_narrative_connection.py`（旧 Narrative）
- `toda_group_proof_narrative_proof_chain_renderer.py`（Proof Chain 専用描画）
- `toda_group_proof_narrative_concrete_transport.py`（Transport 専用描画）
- 上記を参照するプロジェクト直下の `.py` と `tests/` 配下のテスト

## GitHub 現行コードで確認した事実

`phase162_pi5_3_web_replay.py` は `_phase162_ehp_leaves` を旧 Web モジュールから import している。そのため、旧 Web モジュールの丸ごと削除は現状では安全と認定できない。

`phase162_web_narrative_integration.py` は `render_phase162_r3_narrative` を直接呼ぶ。`tests/test_phase162_r3_narrative_connection.py` には旧関数のテストがある。外部利用・動的 import は静的検査だけでは否定できない。

## 判定基準

- `RETAIN_DEPENDENT_MODULE`: 稼働中の Python モジュールから import または直接呼出あり。削除前に依存を移設し、関連テストを実行する必要がある。
- `RETAIN_TEST_CONTRACT_REVIEW`: テスト側に依存あり。旧 API 契約の維持・移行をレビューする必要がある。
- `NO_STATIC_DEPENDENCY_REVIEW_DYNAMIC`: 静的依存は検出されない。削除を意味せず、外部利用と動的 import の確認が必要。

## R5-R9 の完了条件

依存関係の所在と関数単位の撤去判定を `audit.json` と `review.md` に記録すること。R5 全体の最終認定には、表示内容の回帰、旧 Phase 162 fixture 6件の不整合、独立経路の実行時検証が別途必要。

## テスト範囲

`test_audit.py` の7件のみ。全体 pytest は Phase 165 最後にのみ実施。
