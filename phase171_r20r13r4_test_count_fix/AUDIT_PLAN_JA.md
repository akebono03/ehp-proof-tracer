# Phase 171 R20R13R4 監査計画

対象は R20R13R2 のテスト1関数のみ。既存の統合処理で得られた `[R3]より, ...` の行を `list.count()` で数える誤りを `startswith()` による行数集計に改める。

- DryRun: 訂正済み projection.py、Renderer 接続、対象テスト内容を検査
- 本番: テストファイル内の1行だけ置換し、元ファイルのバックアップと変更後全文を `output/` に保存
- 限定 pytest: 新規テストと R20R13R3 経由の関連テストを実行
- 監査: 公開探索 `complete`、3式が1行、Reference 8件を検証
- 次 Phase との境界: 論証規則・表示エンジンを改変しない。全体 pytest は Phase 171 終了時のみ
