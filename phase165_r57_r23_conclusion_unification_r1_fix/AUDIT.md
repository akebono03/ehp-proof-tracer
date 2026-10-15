# R23-R1 原因と修正

失敗した3テストは、`_instantiate_nested()` が `PatternVariable` を dataclass として再構築していたことが原因です。`PatternVariable` の置換を dataclass 分岐より先に実行します。`_match_nested()` および外部 API は変更しません。既存の7テストを維持し、`PatternVariable` 単体の回帰テスト1件を追加します。

本体の前提生成、候補発見、群別 Adapter は変更しません。全体 pytest は実施しません。
