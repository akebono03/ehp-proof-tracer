# Phase 166 R3-AU：`gen_coe` 生成元表示横断監査

## 現行コード確認

GitHub の `develop` を確認した。`SphereRepository` は `sphere(3).csv` の `gen_coe` を整数列として `GroupComponent.gen_coe` に格納するが、現行 production code には `gen_coe` から typed generator expression（型付き生成元式）を構築する変換経路がない。

したがって、R3-AU で DB 表記と生成 LaTeX の一致を自動的に「確認済み」とすることはできない。

## 今回の監査対象

`sphere.csv` が存在すればそれを使用し、存在しなければ現行 DB 名 `sphere(3).csv` を使用する。

112群に限定せず、CSV に登録されている全行を対象とする。各行について `n`, `k`, `id`, `orders`, `generator`, `Element`, `gen_coe` を記録する。

`gen_coe` は次の形に分類する。

- `empty`
- `single_basis`
- `single_basis_with_coefficient`
- `linear_combination`
- `invalid`

## 判定方針

現行コードに変換経路がないため、正常に読める `gen_coe` は `UNWIRED_GEN_COE_TO_TYPED_EXPRESSION` とする。

これは DB が誤っているという判定ではない。`gen_coe` と public renderer（公開表示器）がまだ接続されていない、という実装上の事実を表す。

`generator` 列、`C_1\omega_{23}`、`C_1^{(2)}`、`EF_1^{(1)}` 等の正確性も、この監査だけでは確定しない。

## 完了条件

全 DB 行が監査結果 CSV に現れ、高次 stem が除外されず、`gen_coe` の形別件数が summary に出力されること。

未接続の `gen_coe` について生成 LaTeX を捏造せず、`accuracy_confirmed=false` のまま記録すること。

## 次の境界

R3-AU の結果から、実際に `gen_coe` → typed generator expression の変換が必要かを判断する。その変換を追加する場合も、既存 DB の意味と既存テストから確定できる範囲だけを実装し、将来の生成元意味論を先取りしない。

全体 pytest は Phase 166 終了時まで実行しない。
