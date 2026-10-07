Phase 159 - pi_4^3 repair3c fix8
Semantic corridor boundary audit

背景
----
fix7 で hop depth による bounded upstream expansion は不適切と判明した。

代表6群:
- 1 hop: 866 added steps
- 2 hops: 2260 added steps
- 3 hops: 3644 added steps

pi_4^3 の必要4事実をすべて捕捉するには 3 hops 必要。

したがって hop 数ではなく semantic structure による絞り込みが必要。

目的
----
pi_4^3 の必要4事実について以下を確認する。

- block role
- dependency role
- local consumer count
- local premise count
- nearest provider-anchor distance
- statement type
- inference rule

同時に代表6群の current upstream chain に対して以下の候補 filter を適用し、
候補数を比較する。

1. semantic_block
   block role in {calculation, group_structure, map_property}

2. semantic_block_single_consumer

3. semantic_block_short_anchor
   anchor distance <= 3

4. semantic_block_single_consumer_short_anchor

5. semantic_block_single_consumer_short_anchor_non_relation

狙い
----
pi_4^3 の必要4事実をすべて保ちつつ、
unbounded upstream ancestry の大量導出詳細を一般規則で落とせる
semantic corridor の特徴を特定する。

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
tests/test_phase144_6_r5_30_upstream_calculation_attachment_audit.py

repository-wide pytest は実行しない。

完了条件
--------
- pi_4^3 4事実の共通 structural / semantic 特徴が分かる。
- その特徴を使った6群候補数が unbounded repair3c より十分小さい。
- pi 固有 hard-code を使わず production rule を設計できる見込みが立つ。

この結果を見るまで production selection は変更しない。
