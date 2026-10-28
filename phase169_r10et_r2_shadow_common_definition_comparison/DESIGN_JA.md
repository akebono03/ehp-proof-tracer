# Phase 169 R10ET-R2 — 共通 Definition 優先の比較監査

## 現行コードから確認した根拠

監査結果の GitHub `develop` HEAD は `a5892721436effaf7be759ff17afd3bd427814ed`（コミット `10et`）。R10ET-R1 の監査出力は同コミットに保存されている。R1 実行当時の基準 HEAD は `36e4dc41427ec4437009c96b01cacb07dc165bf6`。

26-stem の $\pi_{69}^{43}$ では、[R1] DB prior と [R2] Toda (4.5) が root の先行2前提を支持し、[R3] ν-family definition と [R4] Chapter V, i) は `GeneratorImage` の祖先であった。[R3] は48件、[R4] は30件の引用付きイメージ推論に関わる。引用は表示上のノイズではなく、現行 Proof Tree の実際の根拠である。

`phase165_r52_r9_shared_math.py` は旧引用付き候補を先に構築し、該当候補がない場合に共通 Definition を探索する。R10ET-R2 はこれを本体変更なしに比較する。

## R2 の実施方法

`shadow_provider_factory()` が通常の検索用 `shared_expansion_provider()` を生成した後、`prioritize_common_definition()` で包む。型付き `GeneratorImage` が `expand_defined_stable_element_image()` を満たす場合のみ、共通 Definition のゼロ前提規則を先に返す。満たさなければ既存の探索を完全に維持する。

この差し替えは監査プロセス内の一時的な関数参照のみであり、終了時には元の関数を復元する。Proof Tree は通常の Backward Search により再構築し、Trust Boundary を必ず再実行する。Renderer による引用隠蔽は行わない。

比較対象は26/11/14/16/9-stem の6ケース、1/2-stem の6ケース、過去の cyclic / direct sum Projection の4ケース。R10ET-R1 の `audit.json` と突き合わせ、元の引用、置換後の引用、Proof Tree 推論数、圧縮表示の有無を確認する。

## 修正判定に必要な条件

- 各群の Proof Tree が `complete` で、Trust Boundary が PASS。
- [R1] DB prior と [R2] Toda (4.5) が必要な場合は維持。
- `GeneratorImage` が共通 Definition で裏付けられ、余分な個別引用が実際に消える。
- 従前の反復懸垂圧縮が維持されること。特に R10A の巡回群 Projection は引用付き GIVEN の祖先を要求するので、ここで退行が発見される可能性がある。
- 既存のテスト期待値だけを書き換えて退行を隠蔽しない。

`READY_FOR_IMPLEMENTATION=False` が出た場合は、その表示経路の共通化を実装修正の対象に含める判断が必要。全体 pytest は Phase 最終段階まで実施しない。

## 変更対象

既存の本体、テスト、文書：変更なし。新規監査ディレクトリ内に `audit.py`、`run.ps1`、監査用のテスト、設計書と README を追加するだけ。
