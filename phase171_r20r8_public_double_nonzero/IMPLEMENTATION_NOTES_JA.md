# Phase 171 R20R8 実装記録

## 目的

既存 `inferred_nonzero_double_rule`（型付き等式と非零像から二倍の非零性を導く規則）への後ろ向き探索候補のみを追加する。$(5.3)$ の固定出典から型付き二倍関係を取り出し、先行群の出典と `HyoujiGen.csv` に基づく型付き生成元から `GeneratorImage` を**証明目標としてのみ**組み立てる。どちらの前提も公開探索で改めて証明される必要がある。

## 変更対象

- `phase171_r2j_r4_r7_nonzero_nu_order/source.py`: 新規関数 `expand_public_nonzero_double_from_cited_source` を末尾に追加。
- `phase165_r52_r9_shared_math.py`: `shared_expansion_provider` 内の R20R7 接続直後に追加関数の import と呼び出しを追加。import は関数内の局所 import とする。
- 新規パッケージ `phase171_r20r8_public_double_nonzero/` のインストーラ、監査、限定テスト、全文提示記録を追加。

## 検証と安全性

- R20R6 Git コミットの既知 blob から R20R7 の内容を再構成し、現在の2ファイルを全文照合する。ローカル変更とコミット後の状態を同等に検証する。
- 改行 CRLF/LF を維持する。バックアップ、失敗時の復元、再実行の冪等性を用意する。
- 新規 `GIVEN` なし。既存の完成証明木は公開探索へ取り込まない。
- 全体 pytest は Phase 終了時まで行わない。

## 完了条件・次工程

`PHASE171_R20R8_DOUBLE_NONZERO=CERTIFIED_PUBLIC_PROPOSAL_PRESENT`。これは**候補生成規則**が証明済みの独立した推論木と一致することを意味し、公開探索の完成を意味しない。R20R9 では残る `typed_double_equality` の接続を別途検証する。
