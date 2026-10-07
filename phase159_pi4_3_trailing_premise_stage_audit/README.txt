Phase 159 pi4_3 trailing premise stage audit

目的
====

repair6c:
- pi6_3 focused regressions 12 passed
- pi4_3 focused tests 7 passed

実際の pi4_3 public Narrative では結論重複は解消したが、

  以上より, pi4^3 = Z/2{eta3}.
  [R2]より, pi3^2 = Z{eta2}.
  □

となり、root conclusion の前提が結論後に残っている。

これは数学的な proof order として不適切。

確認内容
========

pi4_3 について各 contribution-renderer stage で

- root conclusion
- pi3^2 premise
- 「以上より,」

の paragraph index を記録する。

特に:

23 visible_relation_dependencies
24 unique_steps
25 map_dependencies_b
26 injective_reason

の前後で

  premise_before_root
  premise_after_root

がどこで変化するかを確認する。

また root direct premises も表示し、
pi3^2 が root premise として保持されているか確認する。

production code
===============

変更なし。

test code
=========

変更なし。

pytest
======

実行しない。

全体テスト
==========

実行しない。
