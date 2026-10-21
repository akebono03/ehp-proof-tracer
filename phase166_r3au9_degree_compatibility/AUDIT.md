# Phase 166 R3-AU-9 監査

## 対象ファイルと関数

新規 `audit.py`：`read_csv`、`parse_ints`、`parse_number`、`inspect`、`write_csv`、`main`。新規 `test_r3au9.py`：3テスト。新規 `run.ps1`、`README.md`、`AUDIT.md`。既存コードは変更しない。

## 方針

`Element` は表示元 ID の順序付き合成、`gen_coe` は一次結合の係数、`generator` は任意の参考表記である。`HyoujiGen.csv` の `n,k` から得る `source=n+k`、`target=n` は「基礎次数の候補」として照合する。隣接因子の `left.target` と `right.source` を比較するが、不一致だけでデータ不正としない。`stable` に基づく懸垂次数は自動補完・認定しない。

## 出力と完了条件

`results/summary.json`、`results/all_degree_rows.csv`、`results/degree_review_rows.csv`。全データの基礎次数照合と要追加規則行の抽出ができれば完了。次段階で `stable` の意味と懸垂規約を既存 DB・コードから確認する。全体 pytest は Phase 終了時のみ。
