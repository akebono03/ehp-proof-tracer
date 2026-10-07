Phase 159 - pi_4^3 exactness-to-surjectivity unification repair1

原因
====
surjectivity reason sentence 自体は生成されているが、
public Narrative では後段の prose normalization により
末尾の standalone connector

  したがって,

が reason body から分離・正規化される。

そのため test が
  rendered.count(sentence) == 1
という完全 sentence 一致を要求すると stale expectation になる。

今回の変更
==========
test-only。

変更対象:
tests/test_phase159_pi4_3_exactness_surjectivity_unification.py

変更する関数:
test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector()

検証対象を full sentence ではなく public Narrative に残る reason body

  この完全性と pi_4^5=0 より,
  Im E = ker H = pi_4^3.

に変更する。

実装変更
========
なし。

完了条件
========
- surjectivity focused tests PASS
- pi_4^3 exactness prose tests PASS
- Phase 150 exactness-to-map-property regression PASS
- Phase 50 pi_4^3 exactness bridge PASS

全体テストは実行しない。
