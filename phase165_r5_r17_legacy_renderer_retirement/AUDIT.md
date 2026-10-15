# Phase 165 R5-R17 撤去境界

- 削除候補：旧 Narrative モジュール4個と、対応する専用表示テスト5個。
- 維持：`phase162_ehp_leaf_inputs.py`、ProofStep、型付き命題、推論規則、共通 Backward Search、共通 Renderer。
- 実行前に `install.py` がルートおよび `tests/` の直接 import を AST で監査する。未知の直接依存を見つけたら削除しない。
- 古い Phase ディレクトリや audit スクリプトは歴史的記録として維持するため、旧モジュールを読み込むスクリプトは今後動かなくなることがある。
- 文字列からの動的 import は静的検査の限界。Git 履歴とバックアップから復旧可能。
- 旧 Renderer の専用テストは旧仕様の検証であり、現在の共通 Renderer の数学的正当性を証明するものではない。共通経路の限定回帰テストを別途実行する。
- Phase 162 fixture 由来の既知のテスト失敗は解決しない。全体 pytest は Phase 165 の最後にだけ実施。
