# Phase 165 R52-R14 — Root self-citation guard

## 目的

内部証明で、目標と同じ結論を持つ固定 Reference を証明の根として使わない。文献台帳から命題を削除せず、該当探索の証明コンテキストにおいてのみリンクを除外する。その他の命題・群からの利用は維持する。

## 変更対象

- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal()` 全体のみ置換。既存 import は変更しない。
- `test_phase165_r52_r14_root_dependency_guard.py`: 新規、3テスト。ルートに追加。

## 今回の境界

- 文献掲載順 `publication_position`、主張順 `component_position`、証明での利用順 `available_after_position` が未確定なものを推測して埋めない。
- 目標そのものの直接引用だけを無効化。間接的な数学的循環依存の完全検出や一般命題の特殊化は未実装。
- `ProofStep.GIVEN` は削除せず、他の証明では利用可能。
- 全体 pytest は行わない。

## 完了条件

R14 新規テストおよび関連テスト PASS。`pi_3^2` が `INFERENCE` によって証明され、同じ結論の `GIVEN` を最終根にしない。
