# Phase 169 R10E4-R2 — DB 区切り行の処理

## 調査結果

`data/sphere.csv` には `k` のまとまりの区切りとして `n` が空欄のレコードがある。
例えば `k=0,n=` の行が `k=7,n=9` の安定基点より前にある。
旧 `_has_explicit_row()` では空欄を `int()` に渡して例外となり、その場で
検索全体を `False` としていた。

## 対応

空欄の `n` または `k` を持つ区切り行だけを読み飛ばす。
空欄ではない不正な整数は fail-closed（不許可）とする。
安定範囲の `SphereRepository` の自動補完結果は引き続き先行 DB 行として
採用しない。既存の `(k,n)` 順序、型付き構造、Provenance、Trust Boundary
の判定は変更しない。

## 対象

`phase169_r10e4_ordered_db_prior/db_prior.py` の `_has_explicit_row()` 全体のみ。
既存の import に変更なし。新規テストファイルおよび監査を追加。

## 検証

`tests/test_r10e4r2_db_separators.py`、R10E4、R10E2、R10E1、R7、R10D2、
Phase 168 Trust Boundary の限定 pytest を実行する。
全体 pytest は Phase 169 終了時に行う。
