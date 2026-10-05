Phase 158-R5-5b repair1l — preserve transition-source calculation chain

原因
----
repair1k で確認:

- equation (1): tagged, present
- equation (2): tagged, present
- connector "(1) と (2) より,": present
- equation (3): plain only
- order statement が equation (3) より前

body renderer の relocation logic を確認すると、
direct_derivation_support_steps / direct_derivation_premises のうち

- conclusion block 内にない
- incoming transition を持たない
- provenance-only でない

step を conclusion 側へ relocation する。

しかし calculation transition の source step は通常 incoming transition を持たない。

そのため equation (1),(2) が relocation され、
target equation (3) は元の calculation block に残り、
local calculation chain が分断される。

修正方針
--------
step transition の source になっている ProofStep は relocation しない。

具体的には:

transition_source_step_ids = {
  id(source_step)
  for source_steps in sources_by_target_id.values()
  for source_step in source_steps
}

を作り、relocatable 判定から除外する。

これは群番号や statement type に依存しない一般則。

変更対象
--------
Production:
- toda_group_proof_narrative_argument_body_renderer.py
  - _relocatable_toda_group_proof_narrative_direct_derivation_premises()

import:
- 変更なし

Tests:
- 新規・変更なし
- 既存 canonical tests を利用

実行 pytest
-----------
1. Phase 148 depth2 calculation-chain restoration
2. Phase 156 canonical connector/local-order
3. Phase 156 relation-side normalization
4. Phase 157 reflexive-equality suppression
5. Phase 149 local-body ordering regression
6. R5-5b focused ordering
7. Phase 150 directly affected route contracts

repository-wide pytest:
実行しない。

完了条件
--------
1. equation (1),(2),(3) が1つの calculation chain として連続する。
2. equation (3) に tag(3) が復元する。
3. equation (3) が ord(eta_3^3)=2 より前。
4. true rendered reflexive equality は非表示。
5. pi_7^4 / pi_15^8 premise-before-target ordering を維持。
6. group-specific special case を追加しない。
7. full pytest は Phase 158 最後まで実行しない。
