# R38R1 テスト記録（2026-11-09）

- 現行 GitHub `develop` の R9 `rule.py` Git blob SHA は `2c44c68be90cb761d7bdd35e29f23977b5f93a2e`（40桁）。
- 旧 R38 `PINNED` の同値は39桁で末尾 `e` が欠落。
- Python 構文検査：PASS。
- 限定 pytest（新規 `tests/test_patch.py`）：**5 PASS**。
- 旧版と修正版で AST 上の関数・import の相違：なし。トップレベル SHA の末尾1文字のみ変更。
- ZIP 整合性：PASS。
- GitHub develop の直近レビュー済み HEAD：`2e3fcfbea1a3816b146cf53320f9a3bbee618c52`（R37 の統合）。
- **ユーザー環境での Source Guard・R38 の限定 pytest：未実施。**
- **全体 pytest：未実施**（Phase 最終時のみ）。
