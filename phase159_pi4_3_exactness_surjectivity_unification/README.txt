Phase 159 - pi_4^3 exactness-to-surjectivity unification

目的
====
pi_4^3 の

  pi_3^2 --E--> pi_4^3 --H--> pi_4^5

という完全列と pi_4^5 = 0 から E の全射性を導いているにもかかわらず、
Narrative では「これより, E は全射」とだけ表示され、完全性の使用理由が
pi_6^3 の exactness prose と統一されていなかった。

現行 provenance
===============
TodaSuspensionSurjectiveStatement の直接前提は

- TodaPrimaryGroupZeroStatement
- TodaProp42ExactnessStatement

であり、proof data に必要な provenance は既に保持されている。

実装方針
========
既存 EXACTNESS_TO_MAP_PROPERTY を拡張し、

injective:
  Delta = 0 + Delta-E exactness -> E injective

surjective:
  right group = 0 + E-H exactness -> E surjective

を同じ typed reason kind として扱う。

pi_4^3 や eta_2 の hard-code は追加しない。

変更対象
========
toda_group_proof_narrative_reasons.py

import 変更:
- TodaPrimaryGroupZeroStatement
- TodaSuspensionSurjectiveStatement

変更:
_exactness_to_map_property_reason()

toda_group_proof_narrative_reason_renderer.py

import 変更:
- TodaSuspensionInjectiveStatement
- TodaSuspensionSurjectiveStatement
- render_toda_primary_group_latex

変更:
render_toda_group_proof_narrative_reason_sentence()

追加:
_normalize_exactness_to_map_property_reason_prose()

変更:
insert_toda_group_proof_narrative_reason_prose()

tests/test_phase159_pi4_3_exactness_surjectivity_unification.py

新規 focused tests 3件。

期待する prose
===============
[R1]より, pi_4^5 = 0.

この完全性と pi_4^5 = 0 より,
Im E = ker H = pi_4^3.
したがって,
E: pi_3^2 -> pi_4^3 は全射.

完了条件
========
- surjectivity が EXACTNESS_TO_MAP_PROPERTY として構築される。
- zero right group と E-H exactness が typed premises として保持される。
- 「これより, この完全性と」の二重 connector が出ない。
- pi_6^3 の既存 injectivity exactness reason を壊さない。
- pi_4^3 kernel exactness reason を壊さない。
- Phase 50 exactness bridge を壊さない。

Phase 境界
==========
- Reference selection は変更しない。
- equation numbering は変更しない。
- pi_4^3 の群計算そのものは変更しない。
- 他の map property reason は先取りしない。
- repository-wide tests は Phase 159 終了時まで実行しない。
