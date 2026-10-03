Phase156-R6 — focused/sharded regression

変更対象
========
Production changes:
- なし

既存 test changes:
- なし

新規 package:
- phase156_r6_focused_sharded_regression/
  - phase156_r6_sharded_reference_regression.py
  - aggregate_phase156_r6_shards.py
  - test_phase156_r6_sharding.py
  - run_phase156_r6_focused_sharded_regression.ps1
  - README.txt

目的
====
Phase156-R1〜R5 で確定した Reference minimal-display contract を、
focused regression と4分割 shard regression の両方で固定する。

shard
=====
母集団:
- n=2..15
- k=0..7
- 112 groups

分割:
- global_index % 4
- 4 shards
- 各 shard 28 groups
- 各 shard は n=2..15 をすべて含む
- 各 n について各 shard は2つの k を持つ

各 shard の必須 invariant
=========================
1. Reference header は連番
2. body `[R#]` marker には対応 header がある
3. boundary-used statement selection が R3 selector と一致
4. entry-external used statement selection が R3 selector と一致
5. same-entry internal usage のみで複数 public statement にしない
6. final public canonical Reference statement と proof body の exact duplicate = 0

informational
=============
Reference header が explicit body `[R#]` marker を持たないケースは、
R5 final contract に従い違反にしない。

focused regression
==================
- tests/test_phase153_r5_reference_selection.py
- tests/test_phase153_r6_reference_granularity.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- Phase153 public Reference audit-only invariant

完了条件
========
各 shard:
- groups = 28
- exceptions = 0
- violations = 0

aggregate:
- shards = 4
- groups = 112
- unique groups = 112
- duplicate groups = 0
- missing groups = 0
- unexpected groups = 0
- exceptions = 0
- violations = 0

Repository-wide pytest
======================
R6 では実行しない。

次
==
PASS 後:
Phase156 closure
- documentation 更新
- repository-wide pytest
- Phase156 完了判定

Phase157 の機能は先取りしない。
