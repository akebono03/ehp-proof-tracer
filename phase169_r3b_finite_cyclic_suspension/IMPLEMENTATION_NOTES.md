# Phase 169 R3B — 実装・検証境界

## 変更対象（最初に確定）

- `phase165_r12_r24_web_search_connection.py` — ファイル全体を置換。
- `expand_finite_cyclic_relation()` — 関数全体を置換。元の `CyclicStructureStatement` 経路は先頭で維持。
- `finite_cyclic_suspension_transport_inference_rule()` — 同じファイルで既存 `expand_finite_cyclic_relation()` の直前に新規追加。戻り値は `InferenceRule`。
- `tests/test_phase169_r3b_finite_cyclic_suspension.py` — 新規ファイル。6関数と必要な import をすべて収録。

## 完全なコード

- 変更後 import の全文とファイル全文：`full_files/phase165_r12_r24_web_search_connection.py`。
- 新規推論規則の関数全文：`full_functions/finite_cyclic_suspension_transport_inference_rule.py`。
- 変更後の探索関数全文：`full_functions/expand_finite_cyclic_relation.py`。
- テスト import とテスト関数全文：`tests/test_phase169_r3b_finite_cyclic_suspension.py`。
- 実行用 `run.ps1`・監査 `audit.py`・適用 `apply.py` は省略なしの全文。

## 数学的境界

群の型付き等式 $A=\mathbb Z/m\{a\}$、懸垂同型 $E:A\to B$、生成元像 $E(a)=b$ がそれぞれ証明された場合に限り $B=\mathbb Z/m\{b\}$ を推論する。

$$[31m注意**：DB が持つ群構造は探索用 Goal にすぎず、`ProofStep` に変換しない。

今回は 2-stem の組成生成元に限定した後ろ向き候補だけを追加する。$$[31mToda (4.5) の範囲外**であるため、安定輸送の同型性を主張しない。

## R3B の確認事項

- 現行の $\pi_4^2$ の `complete` を維持。
- $\pi_5^3$ の root に候補規則が1本追加される。
- その候補には下位群構造、EHP 懸垂同型性、生成元の像という独立した3前提が残る。
- 由来不明の GIVEN は増えない。
- 限定 pytest のみ実施。全体 pytest は Phase 169 完了時に限る。

## 次の境界

R3C では、この3前提のうち懸垂同型性を Prop.4.2 の EHP 完全性と文献順で利用可能な命題から導出する。生成元の像は別の独立した一般規則として扱い、先取りしない。
