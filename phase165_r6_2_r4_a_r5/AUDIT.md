# Phase 165 R6-2 R4-A-R5 監査記録

- 現行 GitHub の `phase165_r8_rule_provider.py`、`phase165_r57_r23_conclusion_unification.py`、`phase165_r57_r25_premise_generation.py`、`phase165_r52_r9_shared_math.py`、`phase165_r52_r23_existing_rule_adapter.py` と R4-A-R4 実装を確認。
- 既存本番コードは一切変更しない。R4-A-R4 の登録済み Goal 選択を再利用し、AST と逆向き照合結果から観測理由を分類する。
- `NO_CONCLUSION_MATCH` は監査対象の Goal 集合での不一致のみを意味し、規則が不適用であるとの一般的な証明ではない。
- `UNBOUND_VARIABLE` は証人不足を確定しない。`PREMISE_REJECTED_OR_GUARD_UNKNOWN` は guard 不成立と断定しない。
- `STATIC_R8_PATH` は実行時の再帰到達性確認ではない。
- Adapter の `GoalExpansion` 分岐と使用 factory は AST で監査し、Adapter 本体は実行しない。
- 文献証人による候補生成の実行検証と再帰的証明の完成確認は次段階。全体 pytest は Phase 最後のみ。

## 変更対象

新規 `r5_audit.py` の `classify_goal`、`audit_adapter`、`audit_shared`、`perform`、`markdown`、`main`。新規 `test_r5_audit.py` の6テスト。新規 `run.ps1`、`README.md`、`AUDIT.md`。既存ファイル・関数の変更なし。
