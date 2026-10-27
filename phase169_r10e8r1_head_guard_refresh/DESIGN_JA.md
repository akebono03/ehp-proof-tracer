# Phase 169 R10E8-R1 — HEAD ガード更新

## 変更対象

既存の R10E8 本体は変更しない。新規追加するのは、`phase169_r10e8r1_head_guard_refresh/run.ps1` と説明用 `README.md`、`DESIGN_JA.md` のみ。

ZIP には、元の R10E8 パッケージを完全に再収録する。元の `run.ps1` も原文のままとするため、元のパッケージが Git 管理済みでも、その実行スクリプトに差分が発生しない。

## 監査した Git 履歴

- `c3573d29e21688f54e73cf4d51ad53a5591d7959`：R10E8 の初回レビュー時点。
- `2ccc356113f0322511c37b37929ecd8952498646`：R10E7 の監査パッケージ追加のみ。
- `940d1d1cc2e9943e9d2955c7204a4392984d65e9`：R10E8 のパッケージ追加のみ。

両コミットで、本番変更対象ファイルの Git blob は不変。

- `phase169_r10d2_general_family_definition/family_citation.py`：`4a33870892e139ac52d7b26503584b4d9624e0ba`
- `phase165_r52_r9_shared_math.py`：`e010e52fb06a20eb6c60557022ffb024036ed5c0`

## 実行方針

新しいラッパーの `run.ps1` は `develop` と上記3件の HEAD を要求する。その上で、対象2ファイルの Git blob とローカル作業ツリーを個別検査し、元の `phase169_r10e8_hyoujigen_generic_suspension.patch` を呼び出す。

機能の追加、系列ごとの懸垂規則の追加、文献台帳の推論規則の緩和は行わない。限定テストに失敗した場合は対象の元のバイト列に復元する。

## テストと完了条件

R10E8、R10D2、R10E5、R10E4 の限定 pytest と、`π_{23}^{15}`・`π_{24}^{15}` の再探索監査のみを行う。全体 pytest は Phase 169 完了時まで実行しない。

R10E8-R1 は実行ガードを修正する段階であり、群の証明完成を保証しない。両群の `complete` 判定、Trust Boundary の検証、文章の表示確認は後続の結果に従って判断する。
