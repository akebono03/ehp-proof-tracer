# Phase 166 R3-AU-7 監査

## 変更対象

新規 `audit.py`：`read_rows`、`parse_integers`、`inspect`、`main`。
新規 `test_r3au7.py`：3件の限定テスト。
新規 `run.ps1`、README.md、AUDIT.md。
既存ファイルの変更なし。

## 方針

`sphere.csv` の同一 `(n,k)` 内で `gen_coe` の非零位置 `i` と直和成分 `id=i` の対応を調べる。`Element` は表示元の順序付き合成であり、群成分 ID と混同しない。`generator` 欄は参考情報であり空欄をエラーにしない。零ベクトル17行は今回の対象外とする。

## 完了条件

複数非零係数を持つ行について、全非零位置の対応先と欠落・重複を記録する。対応の数学的認定や typed expression の実装は次工程とする。全体 pytest は Phase 166 終了時のみ実施する。
