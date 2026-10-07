Phase 159 pi3_2 repair8 order regression audit

目的
====

repair8 後の actual public pi3_2 で

  H isomorphism
  ...
  H surjective
  H injective

の順となり、
単射・全射より前に同型が表示されている。

現行 GitHub の既存 Phase 159 test:

  tests/test_phase159_r1_2_pi3_2_narrative_repair.py

は

  injective < isomorphism
  surjective < isomorphism

を明示的に要求している。

したがってこれは public proof-order regression の可能性が高い。

確認内容
========

1. 既存 pi3_2 focused contract を実行する。
2. ordered contributions について
   - placement
   - provider_anchor
   - provider_anchor_index
   - insertion_index
   を表示する。
3. 次の各 stage で位置を記録する。
   - base
   - raw contribution insertion
   - full contribution renderer
   - actual public renderer

対象 statement
==============

- E: pi1^1 -> pi2^2 isomorphism
- Delta: pi3^3 -> pi1^1 zero
- H: pi3^2 -> pi3^3 surjective
- H: pi3^2 -> pi3^3 injective
- H: pi3^2 -> pi3^3 isomorphism

production code
===============

変更なし。

test code
=========

変更なし。

full suite
==========

実行しない。
