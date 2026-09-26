Phase 143-75AP R16-R2

変更対象
========
実装:
- toda_group_proof_narrative_argument_body_renderer.py
  - render_toda_group_proof_narrative_argument_body_markdown()

テスト:
- tests/test_phase143_59b_group_structure_duplicate_suppression.py
  - test_phase143_59b_pi15_8_keeps_transported_semantic_decomposition()
- tests/test_phase143_61b_direct_premise_narrative.py
  - test_phase143_61b_pi15_8_keeps_transported_and_final_group()
- tests/test_phase143_61b_r_semantic_suppression_priority.py
  - test_phase143_61b_r_semantic_aggregate_survives_relocation()

import
======
変更なし。
既存の
is_toda_group_proof_narrative_provenance_only_statement
を利用する。

実装修正
========
R13:
preserve_provenance_block_ids に含まれる block では、全 step の
redundant / relocated suppression を解除していた。

R16-R2:
同じ block 内でも、
is_toda_group_proof_narrative_provenance_only_statement(
  proof_step.conclusion
)
が真である step だけ suppression を解除する。

したがって:
- pi_15^8 transported decomposition:
  provenance-only semantic statement として保持。
- pi_8^5 の 2 nu_5 = E^2 nu':
  通常 Relation なので従来の relocation を維持し、二重表示しない。
- context_hidden_step_ids:
  従来どおり最優先で維持。

テスト期待値更新
================
Phase143-51B は multi-argument Narrative に transported decomposition の
semantic LaTeX 表示を要求する。
旧59B/61Bの3テストは同じ出力に非表示を要求しており、現在仕様と矛盾する。

Phase134-24 も transported decomposition と standard-order final group の
両方を順に表示することを要求しているため、旧3テストを現在仕様へ合わせる。

今回変更しないもの
==================
- 数学規則
- proof repository
- public API
- group calculation
- Phase144以降の機能
- documentation

focused pytest
==============
- Phase143-51A
- Phase143-51B
- Phase143-59B
- Phase143-61B
- Phase143-61B-R
- Phase134-24 pi15^8 Narrative

完了条件
========
1. pi_8^5 direct premise が1回だけ表示される。
2. pi_8^5 の premise 順序が復元される。
3. pi_15^8 transported decomposition が semantic LaTeX で表示される。
4. pi_15^8 final group conclusion も維持される。
5. internal rule-name fallback は表示されない。
6. focused regression が全通過する。

次Phaseとの境界
===============
Phase143 の semantic Narrative 整合性修正のみ。
Phase144 の機能は含めない。
