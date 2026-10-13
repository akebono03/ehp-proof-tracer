# Phase 165 R14-R20 — Toda (5.1) 出典範囲のレビューゲート

## 変更対象

- 新規 `phase165_r14_r20_source_gate.py`：`AdoptedTextReview`、`diagonal_text_matches()`、`source_scoped_reviewed_bridge()`、`prop42_candidate_report()`、`audit_r20()` の完全な実装。
- 新規 `test_phase165_r14_r20_source_gate.py`：テスト6関数全文。
- 新規 `audit.py`、`run.ps1`、`README.md`。

既存クラス・関数・import・文書の変更はありません。

## 実装・制約

ユーザーが示した Toda (5.1) の番号付き式と隣接する表示数式の TeX を、本文範囲を確認するための基準とします。単なる `(5.1)` locator 一致ではなく、対角群の等式・安定群の等式・安定懸垂の表記まで含まれることを確認します。

文字列が一致しても自動認証しません。独立の `reviewer_confirmed_scope=True` が明示されている場合のみ、R19 既存登録機構を通じて、**採用 TeX のレビュー済み**型付き命題を独立 Registry に登録します。Toda 原著版の照合済みという意味ではありません。通常実行では確認フラグを与えないため、新規 ProofStep は0です。

Proposition 4.2 の候補2件は原文を `phase165_r14_r20_output/report.md` に記録しますが、テキストだけから一般的な EHP 完全性の適用条件を認証したとは扱いません。

## テスト・完了条件

6件の pytest と read-only 監査のみ。採用 TeX 出典範囲の欠落、レビュー未完了、Proposition 4.2 の未承認を正しく扱い、標準監査で証明を生成しないこと。全体 pytest は Phase 165 最後にのみ実行。

## 次の境界

Proposition 4.2 の本文と適用条件を人間が数学的に検証し、一般形を Registry に登録すること。その後、既存の Δ=0 と E 同型の共通規則へ接続すること。
