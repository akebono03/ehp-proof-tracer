Phase 159 pi6_3 exactness reason contract audit

目的
====

Phase 159 pi4_3 repair5 の focused tests は 7/7 PASS。

Phase 157 regression では、pi6_3 の旧 exactness reason

  この完全性と $Δ=0$ より,
  $\ker E=\operatorname{Im}Δ=0$.

を期待して失敗した。

直前の stage audit では、reason は消失しておらず、
reason renderer 自体が現在

  完全性より, $E: pi5^2 -> pi6^3$ は単射.

を返していることが判明した。

この audit では、
production を旧文へ戻すべきか、
既存テストを stale expectation として更新すべきか
を判断するため、ローカル契約を確認する。

確認内容
========

- current local render_toda_group_proof_narrative_reason_sentence() 全文
- pi6_3 EXACTNESS_TO_MAP_PROPERTY の実際の sentence
- public pi6_3 body の injectivity 周辺
- tests 内の旧文契約の出現箇所
- tests 内の簡潔文契約の出現箇所
- reason renderer の git diff
- Phase 150 / Phase 157 関連テストの git diff

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
