Phase 159 - pi_6^3 post-normalizer duplicate source audit

目的
====
runtime binding audit により、direct public renderer は
Phase158 public normalization の後に次の3関数を通ることが判明した。

1. _phase159_r1_7c_r4_normalize_public_map_property_prose()
2. _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()
3. _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions()

normalizer 出力では E:pi_5^2->pi_6^3 は単射. は1回だが、
direct public 最終出力では2回になる。

監査内容
========
baseline から順に上記3関数を1つずつ適用し、
各段階の対象文 occurrence count を表示する。

さらに3関数の inspect.getsource() を出力し、
重複を生む実装箇所を特定する。

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。
