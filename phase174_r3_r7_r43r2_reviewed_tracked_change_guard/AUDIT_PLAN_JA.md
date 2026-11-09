# R43R2 監査計画

## 判明した障害

R43R1 の `verify_checkout()` は追跡変更が1件でもあれば一律に停止する。R43 が既に適用され、変更がレビュー済み `phase165_r52_r9_shared_math.py` の完全一致する Provider 追加だけであっても停止するため、差分の内容を検証して認可可能にする。

## 最小変更

- 変更対象：`phase174_r3_r7_r43r1_r3_sha_pin_fix/install.py` の `verify_checkout()` 全体のみ。
- 認可：追跡差分なし、または `phase165_r52_r9_shared_math.py` だけで R43 `expected_replacement()` とバイト内容が完全一致する場合。
- 拒否：ステージ済み変更、ほかの追跡ファイル変更、予定外差分、HEAD 不一致。
- 新規 R43R2 の修正コード・テスト・`run.ps1` を ZIP に同梱する。
- 生産コード、数学的規則、出典、既存 API、共通 Renderer は変更しない。
- 全体 pytest は実施しない。

## 完了条件と次工程

R43R2 Guard、元の R43R1 Guard、R43 公開 Provider 監査、各限定 pytest の PASS。次は R44 で実際の検索の障害を監査する。Web の最終根の完成は R43R2 の対象外。
