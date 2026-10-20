# Phase 166 R3-Q 探索前提比較監査

## 変更対象

- 新規 `phase166_r3q_premise_comparison/audit.py`：`contains_relation()`、`ordered_given_ids()`、`implicit_given_ids()`、`describe()`、`inspect()`、`main()` を追加。各関数の全文と import 全文は `audit.py` に収録。
- 新規 `phase166_r3q_premise_comparison/run.ps1`：リポジトリの root を基準にモジュール実行。
- 新規 `README.md` と `CHANGED_CODE.md`。

本番コードおよび既存テストは変更しない。

## 監査項目

$π_3^2$、$π_4^3$、$π_5^4$ の登録済み目標ごとに、元の文献前提集合と掲載順判定後の集合を比較する。目標を含む複合主張も候補として報告するが、位置未設定の候補は明示する。候補を勝手に一意化しない。`ProofStepLink` の増減は、既存の screen 関数の仕様に従って報告する。

## 完了条件と次工程

レポート出力に成功し、削除された GIVEN の ID と掲載位置を確認できること。ここでは通常 Web 探索を切り替えない。次工程で原因を確認してから最小変更する。全体 pytest は Phase 166 終了時だけ実行。
