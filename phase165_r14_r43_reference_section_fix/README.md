# Phase 165 R43 — Reference 欄の区切り線対応修正

## 変更対象
- `phase165_r14_r43_reference_reason.py`：`enrich_common_narrative()` の関数全文を変更。空の Reference 欄に残る `---` と見出しを本文扱いせず、既存の出典葉から Reference を挿入する。
- `test_phase165_r14_r43_reference_reason.py`：既存テスト5件の全文に加え、区切り線のみの空欄・既存 Reference 非重複の回帰テスト2件を追加。
- `install.py`：前版と同じ。共通 Renderer のフック導入済みなら再変更せず、補助モジュールだけ更新する。
- `run.ps1`：対象テスト7件のみを実行する。

## 完了条件
Reference が Toda (5.1)、Proposition 4.2、Proposition 5.1 を含み、既存の参照欄を重複表示せず、完全性の理由を保持する。全体 pytest は実行しない。

## 次工程との境界
新たな証明探索規則、型付き命題、Web 専用 Renderer は追加しない。実際の Web 表示で最終確認する。
