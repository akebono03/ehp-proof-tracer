# Phase 166 R3-J 回帰復旧

- 症状：R3-J 後に Web の π₃² が `generic-partial-proof` となった。
- 推定原因：Web の検索対象を `citing_assertion_id` に切り替えた一方、採用済み (5.1) 等に必要な文献間順序が現行の型付き Reference に結び付いておらず、探索前提が空になった。
- 復旧：`phase165_r55_nk_only_goal.py::search_group_from_registered_goal` のみ R3-J 以前に戻す。
- 保持：Proposition 5.1 の5主張の `component_position=1..5`、R3-H、R3-G、その他の実装。
- 重要：この復旧は最終的な台帳一元化ではない。従来のオンデマンド先行証明経路が暫定復活するため、次の段階で台帳経路の文献間順序の接続と逆向き探索を別途修正する。
- 実リポジトリでの pytest は未実施。全体 pytest は Phase 166 終了時のみ。
