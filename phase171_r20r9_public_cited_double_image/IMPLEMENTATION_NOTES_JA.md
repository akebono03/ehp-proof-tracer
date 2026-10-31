# Phase 171 R20R9R4 実装・監査記録

## 確定した原因：2か所の懸垂前後の元の混同

R20R9R2 は `2ν′=η_3^3` の引用関係の右辺と、導出目標 `2ν′=E(η_2^3)` の `E` の引数を直接比較していた。また `GeneratorImage.target_generator` にも `η_2^3` を割り当てていた。

数学的に `η_2^3` は懸垂前の `π_5^2` の元、`η_3^3` は懸垂後の `π_6^3` の元であり、両者は対象を異にする。そこで候補となる引用関係の右辺が懸垂後の群に属することを検査し、候補 `GeneratorImage` の target_generator にその右辺を使う。`typed_double_image_conclusion` の既存の型付き等式チェックが、最終的な一致と懸垂前後の型を検証する。

## 変更対象

* 本番ファイル `phase171_r2j_r4_r3_double_image_bridge/source.py` の `expand_public_cited_double_image_equality()` の2か所だけ。他の関数・import に変更なし。
* インストーラ `phase171_r20r9_public_cited_double_image/install.py` は R20R9R2 の全コードを逆変換で厳密に復元し、既存のインストール状態と照合する。
* テスト：修正前の等式比較に戻さないための検証を追加。pytest モジュールの同名衝突を避けるため `run.ps1` の分離実行は維持。
* `phase165_r52_r9_shared_math.py` は変更しない。

## 完了条件・境界

限定 pytest と実際の R4-R3 の `ProofStep` 一致・公開探索の監査が成功すること。新規 GIVEN は0、既存完成証明の公開探索への直接渡しなし。Web 表示の完了判定は次工程で実証する。全体 pytest は Phase 終了時だけ実行する。
