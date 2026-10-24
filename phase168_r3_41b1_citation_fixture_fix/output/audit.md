# Phase 168 R3-41B — 共通 Partial Narrative 監査

既存 ProofStep のみ表示し、未解決 Goal は証明済みとしない。

| Case | 状態 | Goal | 診断 | ステップ | QEDなし |
|---|---|---|---|---|---|
| not_searched | PASS | PASS | PASS | PASS | PASS |
| partial | PASS | PASS | PASS | PASS | PASS |
| search_failed | PASS | PASS | PASS | PASS | PASS |

- 既存完成4群の全文比較は compare.py で別途確認。
- 既存 Web fallback と明示 legacy API は維持。
- 全体 pytest は実行しない。
