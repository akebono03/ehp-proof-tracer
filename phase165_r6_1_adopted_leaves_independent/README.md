# Phase 165 R6-1: 参照命題と固定 Goal の分離

変更対象: `phase165_r14_r36_adopted_backward.py` の `adopted_leaf_steps()` 全体。既存 import は他の関数で使用するため維持する。新規関数・クラスは追加しない。

従来の `backward_leaf_goals(pi32_goal())` による参照命題の選定をやめ、既存の型付き出典生成元と基礎命題 $E(\\iota_2)=\\iota_3$ から9件を構築する。これは一般的な全文献台帳ではなく既存採用資料の Source Bundle であり、数学的な事実の範囲は拡張しない。

限定テスト: `test_independent_source.py` を実行。変更前のバックアップあり。全体 pytest は実行しない。

完了条件: 旧 frontier への依存なしに9件を生成し、旧 frontier と同じ結論であること。R6-2 の共通逆向き探索規則・pi43 Adapter 削除は対象外。
