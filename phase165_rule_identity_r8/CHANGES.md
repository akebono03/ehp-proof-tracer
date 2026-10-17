# Phase 165 R8 変更一覧

- 新規 `phase165_rule_identity_r8/audit.py`: `classify_pair()` と `main()` を追加。既存規則の前提・結論・Guard を読み取り専用で比較する。
- 新規 `phase165_rule_identity_r8/test_audit.py`: `test_r8_pair_has_same_forward_patterns()`、`test_r8_composition_rule_has_additional_guard()` を追加。
- 新規 `run.ps1`: リポジトリ直下を基準に監査と対象限定 pytest のみ実行する。
- 本番コードは変更しない。旧 Catalog は呼び出さない。規則の削除・統合を行わない。
- 完了条件：2規則のパターン一致と Guard の相違を実行時に確認できる。
- 次段階：統一規則台帳全体の ID・適用条件・探索接続状態を監査する。全体 pytest は Phase 末尾まで行わない。
