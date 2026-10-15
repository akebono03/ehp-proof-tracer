# Phase 165 R5-R12 監査方針

- 既存の旧 Narrative 関数を削除する前に、関数単位の静的依存を記録する。
- GitHub の現行実装と関連テストを確認した。GitHub はローカルの R5-R11 適用前の場合があるため、実行先のコードを基準に判定する。
- `phase162_ehp_leaf_inputs.py` が存在し、Web Replay と旧 Web モジュールの両方が共通の `_phase162_ehp_leaves` を import することを検査する。
- Application と Test の依存を別々に報告する。
- `RETAIN_TEST_CONTRACT_REVIEW` は即削除を許可する判定ではない。
- 旧 Phase 162 fixture の6件の失敗は未解決として残す。
- 全体 pytest は Phase 165 最後にだけ実施する。
