# Phase 174 R3-R7-R10 監査計画

## 変更対象・追加位置

新規 `phase174_r3_r7_r10_cited_family_gap_audit/` のみ。

- `audit.py`：GitHub HEAD・ソース SHA と R9 JSON の検査、ν-family の正規型と既存 `GeneratorImage` の候補を検査する関数をファイル内に新規追加。
- `tests/test_audit.py`：監査契約テストを新規追加。既存テストの修正なし。
- `run.ps1`：同名 `test_audit.py` の import 衝突を避け、Phase 別に限定 pytest を実行。
- `README.md`：英語の実行説明。

既存本体・Proof Tree・Narrative・Web・共通5文書は変更しない。全体 pytest は実行しない。

## 数学的な対象

Toda Proposition 5.9 の採用転写では、ν_6 と η_9 の合成が零である一般関係を参照している。一方、R9 で得られた右結合の `GeneratorImage` が要求する左因子像には公開候補が0件である。出典、型付き系列定義、既存の候補、完成した ProofStep を混同しない。

R10 は左因子の `nu_6` と、引用済み ν-family の正規表示 `ν₆` を、表示名・GeneratorSymbol.family・次数・定義域と値域ごとに比較する。正規形に置き換えた検査対象について、`expand_cited_stable_family` と公開候補を別々に観測する。

これは元の Goal を勝手に正規形に置換する変更ではない。元の Goal の未解決状態を維持し、新たな GIVEN や未出典の具体的関係式を導入しない。

## 完了条件

1. 新規・関連限定 pytest と SHA Source Guard が PASS。
2. R9 の実行済み JSON の候補数・未完了契約を検証。
3. 引用済み ν-family 定義の存在、正規形と元の因子像との一致／不一致、候補数を JSON に記録。
4. 出典を使う場合も一般関係からの推論を必要とすることを明示。目標 `π₁₂⁷=0` の完成は宣言しない。

次段階 R11 は R10 の実測結果を確認してから、既存の正規化規則の再利用か、一般的な出典特殊化を最小限追加するか判断する。
