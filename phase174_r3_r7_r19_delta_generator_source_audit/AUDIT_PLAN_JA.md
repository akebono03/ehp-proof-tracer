# Phase 174 R3-R7-R19：Δ生成元・像の出典監査

## 変更範囲

既存の本番コード、既存テスト、数学的規則、DB、Narrative Renderer は変更しない。

新規ディレクトリ `phase174_r3_r7_r19_delta_generator_source_audit/` だけを追加する。
- `audit.py`：Git Source Guard、Toda Prop 5.9 と生成元 DB の監査、公開の未完成 Frontier 検査。
- `tests/test_audit.py`：Source Guard・出典構造・記号表示と型付き根拠の分離。
- `tests/test_public.py`：公開経路が誤って証明完了にならないことの検査。
- `run.ps1`：限定 pytest のみ。`-DryRun` は監査のみ。
- `README.md`：英語の実行概要。
- `CODE_FULL_JA.md`：新規ファイルのコード全文。

## 数学的な境界

Toda Proposition 5.9 には $\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ とある。ただし、結論の群構造を直接 `GIVEN` にして目標 $\pi_{12}^{7}=0$ を閉じない。

`data/HyoujiGen.csv` の名前 `Δ(ι13)` は記号表示であり、`MapApplication` の型付き証明に変換しない。R18 一般規則の前提には、別途検証された `TodaDeltaImageFreeCyclicStatement` が必要である。

現在の出典付き signed Δ witness が0件である場合も、それだけで「文献が存在しない」とは断定しない。今回の監査は現行公開 Source-screened context を対象にする。

## 完了条件

1. `SOURCE_GUARD=PASS`、Toda Prop 5.9 の命題と証明の順序を確認。
2. 既存 R18 の一般規則テストと公開 Frontier の限定 pytest が PASS。
3. `PUBLIC_DELTA_IMAGE_PROPOSALS=0` と `SIGNED_DELTA_WITNESSES=0` を検出。
4. 目標の `SEARCH_STATUS=search_failed`、`VERIFIED_STEPS=0` を維持。
5. `GIVEN` 追加0件・数学的規則追加0件・全体 pytest 未実施。

次段階では、引用・型付き生成元・写像適用の同一性を独立して導出可能か監査する。R19 では実装しない。
