# Phase 171 R20R12R2 — 原因と監査方針

## 原因

R20R12 の `verified_order_four_summary()` は `element_tex(order.element)` によって位数4の生成元を表示していた。しかし `element_tex` は添字のない `ν′` を対応対象とせず `None` を返す。表示失敗時の `return None` が実際の証明本文テストを失敗させた。

## 今回の変更

変更対象は `phase171_r20r12_verified_cyclic_narrative/projection.py` の import と `verified_order_four_summary` の生成元表示の1行。既存の汎用 `render_toda_expression_latex(order.element)` を利用する。証明木の検証、既存の前提・出典、公開探索、Renderer の内容は変更しない。元の `R20R12` テストを含めた限定 pytest と、実際の公開探索の完成証明監査を行う。

## 監査条件

1. `develop` ブランチである。
2. 元の `projection.py` の内容がレビュー済み SHA-256 と一致する。
3. Renderer が R20R12 により変更された後の想定内容と一致する。
4. 修正後、元の失敗テストと追加テストが PASS する。
5. 公開探索の `complete`、位数4推論、Reference が維持される。
6. 未証明の `GIVEN`、完成証明木の注入、全体 pytest は行わない。

従来の `phase168_r3_5_model_renderer.py` には一切書き込まない。
