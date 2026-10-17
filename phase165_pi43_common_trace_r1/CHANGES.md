# Phase 165 共通探索 R1 — 変更一覧

- 本番ファイル・クラス・関数の変更：なし。
- 新規 `phase165_pi43_common_trace_r1/audit.py`：`describe_expansions()`、`trace()` を追加。共通 Provider の実候補と第1階層の前提候補を JSON 出力。
- 新規 `phase165_pi43_common_trace_r1/test_audit.py`：監査記録の整形テスト2件。
- 新規 `run.ps1`：読み取り専用監査と対象 pytest を実行。

## 完了条件

Adapter が存在せず、root 候補数・適用 Rule 名・前提候補が記録できること。証明の完成は完了条件に含めない。

## 次の段階との境界

監査に基づく共通規則の追加／逆向き適用機構の修正は次の段階。全体 pytest は実施しない。
