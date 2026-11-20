# Phase 176 R3R9 — 右合成の型境界監査

## 目的

Phase 176 R3R8 では、Toda Lemma 5.7 の明示条項から、$E(\eta_2\circ\nu')=0$ を表す `GeneratorImage` の推論ステップが独立環境で証明できた。一方、$\pi_7^2$ の生成元 $\eta_2\circ\nu'\circ\eta_6$ が懸垂で零になることはまだ証明されていない。今回は既存の型付き規則が直接対応できるかを監査する。

## 点検対象

- 既存の先行 DB 結果と生成元の3因子分解
- Lemma 5.7 の出典の一意な選別と基礎零像の実際の推論
- 合成写像の端点と `GeneratorImage` の写像型
- `composite_generator_image_rule` と `generator_zero_from_composite_rule` の既存候補
- 出典を接続した独立 Provider と通常 Provider の、合成後の零像目標に対する候補数

## 厳守事項

候補は証明ではない。基礎零像から合成後の零像へと直接飛躍しない。`Relation` と `GeneratorImage` を暗黙に同一視しない。先行 DB の群表示を新しい文献 GIVEN とみなさない。

既存 Production コード・数学的推論規則・GIVEN・表示器・ドキュメントは変更しない。全体 pytest は Phase 176 の最後のみ実施する。

## 完了条件

DryRun、本監査、限定 pytest が PASS し、`report.json` に上記の型と候補を記録する。証明完成の判定は常に `false` とする。次の R3R10 では、実測された型境界に対して既存規則の組み合わせで足りるか、独立した一般規則が必要かを判断する。
