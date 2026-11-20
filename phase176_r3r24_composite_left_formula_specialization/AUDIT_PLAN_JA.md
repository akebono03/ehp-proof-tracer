# Phase 176 R3R24 — 型付き左合成の最小修正

## 対象

- 変更対象: `phase171_r2h_prop22_cited_hopf/source.py` の `_formula_parts()` 全体のみ。
- 新規: `phase176_r3r24_composite_left_formula_specialization/` 以下のインストーラ、監査、テスト、実行スクリプト、文書。
- import 節の変更なし。既存 API 名・引数は維持。

## 型判定

既存の `expression_endpoints()` を利用し、合成左因子の内側接続と右側の suspension 接続が一致する場合に限り、Toda Proposition 2.2 の公式形を受理する。括り方が異なる式の自動同一視、右合成の値の仮定、出典の無条件登録は行わない。

## 完了条件

DryRun、限定 pytest、`git diff --check` が PASS すること。群構造の完成は完了条件ではない。全体 pytest は Phase 終了時のみ。

## 次段階

R3R25 で導出済みの Hopf 像を右合成公式に代入するための一般的な証明義務を別途確認する。R3R24 は特殊化の型の入口に限定する。
