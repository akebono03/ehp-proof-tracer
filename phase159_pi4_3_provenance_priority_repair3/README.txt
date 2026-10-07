Phase 159 pi4_3 provenance-priority repair3

変更対象
========

変更:
- toda_group_proof_narrative_argument_body_renderer.py
  - render_toda_group_proof_narrative_argument_body_markdown()

新規:
- tests/test_phase159_pi4_3_provenance_priority.py

import の変更
=============
なし。

原因
====

repair2 により

  Toda pi_4^3 finite cyclic quotient calculation

は generator bridge

  eta_3 = E eta_2

を介して root conclusion と同じ group-structure semantic claim であるため、
redundant_direct_premise_step_ids に正しく入るようになった。

しかし body renderer の display_steps 選択には

  redundant でも block が preserve_provenance_block_ids に含まれれば表示する

という例外があり、監査では実際に

  redundant=True
  preserve=True

となった。

この例外により bare conclusion が復活し、

  pi_4^3 = Z/2{eta_3}
  以上より, pi_4^3 = Z/2{eta_3}

という重複が残っていた。

修正規則
========

group-structure semantic rule によって redundant direct premise と判定された step は、
provenance preservation より suppression を優先する。

ただし block 全体は削除しない。
同じ provenance block 内の non-redundant step は従来どおり表示する。

したがって今回の変更は

  redundant step を provenance exception で復活させない

だけであり、provenance preservation 自体を無効化するものではない。

テスト
======

新規テスト:
1. pi4_3 public proof で最終 group conclusion が1回だけである。
2. 「以上より, ...」の接続された最終結論を保持する。
3. non-redundant evidence
   - pi3^2 group structure
   - ker E
   - E surjectivity
   が引き続き public proof に残る。

既存 focused regression:
- tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py
- tests/test_phase143_59b_group_structure_duplicate_suppression.py
- tests/test_phase50_pi4_3_finite_cyclic.py
- tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========

proof body の pi4_3 group conclusion が

  以上より, pi_4^3 = Z/2{eta_3}.

の1回だけになること。

同時に non-redundant derivation evidence が残ること。

次 Phase との境界
=================

今回は pi4_3 で発見された
group-structure redundant direct premise と provenance preservation の
優先順位だけを修正する。

他の statement kind の semantic deduplication や
global public-Narrative deduplication には拡張しない。

全体テストは Phase 159 終了時まで実行しない。
