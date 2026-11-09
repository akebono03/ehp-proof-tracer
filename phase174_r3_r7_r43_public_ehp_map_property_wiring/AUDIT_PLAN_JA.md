# Phase 174 R3-R7-R43 監査計画

## 変更対象

既存ファイルは `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` だけを変更する。関数冒頭の R41 既存接続の直後に、R5 と R37 の一般 `GoalExpansion` Provider を追加する。既存 import は変更しない。新規ファイルは本 ZIP の R43 ディレクトリ内に追加する。

## 事前検証

GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `f5b6899b124d435c224870476b2448454f77b1b5` と、その直前の R41 HEAD `f604062833ff4dc2756daa96235814983f98fbf2` を確認済み。R42 merge は R42 ディレクトリ11ファイルのみ。対象ファイル Git blob は `8bb72fe9b3fe22c1917c51971b12338d62be9e9b`。R5、R37、R3、R40、R41、R42 の関連コードとテストを GitHub から照合した。

## 数学的な境界

R5 は `ImageZeroStatement(E)` と EHP の exactness の2件をそれぞれ INFERENCE として要求。R37 は Hopf 単射性、EHP image=kernel、下側 Delta の核、Toda Proposition 2.7 の型付き公式の4件を INFERENCE として要求する。R43 はこれらの推論規則を変更せず、公開候補として接続するだけ。新しい数学的 `GIVEN`、目標群の直接登録、群ごとの Narrative、証明済み root は追加しない。

## 実行と合否

DryRun はファイルを変更しない。通常実行は Source Guard の検証後に一関数のみ変更、変更後の関数全文と import 全文を出力し、公共候補監査と限定 pytest を実行する。正式な完了条件は Source Guard、公開 R5/R37/R41 候補、group-root scoped DB prior の採用、既存関連テストの PASS。Web HTTP の実測や最終群の完成は対象外。全体 pytest は Phase 174 の最後に実行する。

## 次 Phase との境界

R44 以降は通常の Proof Search で generator-zero まで実際に証明が進むか、上側 Delta 全射性の別のサブゴールで止まるかを特定する。R43 では再帰探索の DB prior 承認条件を変更しない。
