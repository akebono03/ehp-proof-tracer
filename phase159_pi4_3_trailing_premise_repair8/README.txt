Phase 159 pi4_3 trailing-premise repair8

変更対象
========

production:
- toda_group_proof_narrative_contribution_renderer.py
  - _contribution_insertion_indices()

new test:
- tests/test_phase159_pi4_3_trailing_premise_order.py

import:
- 変更なし

監査結果
========

pi4_3:

  pi3^2 = Z{eta2}

contribution は

  placement=AT_PROVIDER_ANCHOR
  provider_anchor=True
  provider_anchor_index=192
  conclusion_index=144

だった。

既存規則は AT_PROVIDER_ANCHOR について
provider_anchor_index を無条件に採用するため、
explanatory prerequisite が argument conclusion より後ろへ配置された。

修正
====

AT_PROVIDER_ANCHOR の insertion index を

  provider anchor がない:
    conclusion_index

  provider anchor がある:
    min(provider_anchor_index, conclusion_index)

とする。

これにより:

- provider anchor が conclusion より前:
  従来位置を維持
- provider anchor が conclusion より後:
  conclusion を越えず、その直前へ配置

pi4_3 固有の n/k、rule-name、statement string による
production 分岐は追加しない。

repair5 境界
============

repair5 の connector ownership 規則も保持する。

standalone connector

  以上より,
  したがって,
  これより,
  これらより,

が conclusion の直前 paragraph の場合、
conclusion anchor を connector paragraph の先頭へ移す。

したがって provider contribution も
connector と conclusion の間へ割り込まず、
両者より前へ配置される。

テスト
======

新規:
1. provider anchor が conclusion 後でも insertion_index <= conclusion_index
2. contribution renderer で pi3^2 premise < pi4^3 conclusion
3. public Narrative で [R2] premise < 以上より final conclusion

既存:
- Phase 159 pi4_3 repair5 focused tests
- Phase 159 pi6_3 zero-map reason-order
- Phase 150 exactness reason
- Phase 157 dangling connector
- Phase 157 zero-map/use order

境界
====

- contribution ordering の role / placement 判定は変更しない。
- provider anchor helper 自体は変更しない。
- pi6_3 repair7 は変更しない。
- reason renderer は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。
