# Phase 169 R10ET-R3B — HEAD ガード改訂

## 背景

R10ET-R3 は、想定 HEAD `a5892721436effaf7be759ff17afd3bd427814ed` と実行時 HEAD `085b58cfa1bdf0e0e3d164fbff0c4e95deb07367` が異なるため、証明探索より前に終了した。GitHub 上でコミット間の差分を確認した結果、`085b58cf` の追加は R10ET-R2 監査ファイルと出力に限定される。続く `c63ca5d07904e7725cbfabc9db2d714845d9a8c7` は R10ET-R3 監査パッケージの追加のみである。

三つの HEAD で `phase165_r52_r9_shared_math.py` の Git blob SHA がすべて `61cbadb06f770c51a9c1f5a3c8026acf9e14aa` であり、証明探索本体・既存テストには差分がない。

## 変更対象

- `phase169_r10et_r3b_reviewed_head_guard/audit.py`：`main()` の HEAD ガードをレビュー済み3コミットの明示許可方式へ変更。元の R3 監査コード全体を同梱。
- `phase169_r10et_r3b_reviewed_head_guard/run.ps1`：R3B のモジュールを実行し、新規ガードテストを限定 pytest に追加。
- `phase169_r10et_r3b_reviewed_head_guard/tests/test_reviewed_head.py`：許可 SHA と既存 provider blob の検査。

既存ファイルには変更を加えない。差し替えの対象はメモリ上の provider factory および巡回群引用検査だけであり、R3 と同じである。証明探索、Trust Boundary、Reference と本文の比較方法は変更しない。

## 完了条件と Phase 境界

実行時に全対象の完成証明と Trust Boundary が維持され、追跡対象に変更がないこと。巡回群 Projection が回復するか、直和群 Projection に退行がないか、引用なしの「より」が生じるかはそれぞれ監査結果に記録する。

R3B は比較監査のみ。製品コードの修正・古い引用経路の除去・表示文章の変更は将来の R10ET-R4 以降に委ねる。全体 pytest は Phase 169 終了時のみ。
