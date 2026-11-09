# R40 テスト状況

- Python AST 構文検査：PASS。
- R40_STATIC：4 PASS（パッケージ作成環境）。
- R40_RULE・R40_REAL_AUDIT・R40_GUARD：ユーザー Windows 環境で実行。
- R39_REAL_PROOF・R6_HISTORICAL・R38_PUBLIC：ユーザー Windows 環境で限定回帰。
- 全体 pytest：未実施。

誤った `GIVEN` 昇格、偽の DB citation、不正な先行順序を拒否することを合格条件とする。隔離推論の成功と公開検索・Web 完成は別判定。
