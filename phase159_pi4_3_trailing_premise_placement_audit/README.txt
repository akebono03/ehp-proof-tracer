Phase 159 pi4_3 trailing premise placement audit

目的
====

stage audit で pi3^2 premise は
stage 01 contribution insertion から既に root conclusion の後ろにあり、
stage 23 visible relation dependencies でも前へ戻らないことが判明した。

次に contribution ordering / placement を確認する。

確認内容
========

pi4_3 の各 argument について:

- argument role
- conclusion
- local body blocks
- ordered contribution
- placement
- provider_anchor
- distance_to_conclusion
- provider_keys
- provider_anchor_index
- final insertion_index

特に

  pi3^2 = Z{eta2}

の contribution が

- AT_PROVIDER_ANCHOR
- BEFORE_ARGUMENT_CONCLUSION
- BEFORE_DEPENDENT_CONTRIBUTION

のどれになっているかを確認する。

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
