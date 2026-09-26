Phase 143-75AP R16

変更対象
========
1. toda_group_proof_narrative_argument_body_renderer.py
   - render_toda_group_proof_narrative_argument_body_markdown()
   - aggregate statement predicate import if not already present

2. tests/test_phase143_59b_group_structure_duplicate_suppression.py
   - test_phase143_59b_pi15_8_keeps_transported_semantic_decomposition()

3. tests/test_phase143_61b_direct_premise_narrative.py
   - test_phase143_61b_pi15_8_keeps_transported_and_final_group()

4. tests/test_phase143_61b_r_semantic_suppression_priority.py
   - test_phase143_61b_r_semantic_aggregate_survives_relocation()

実装内容
========
R13 は preserve_provenance_block_ids に含まれる block の全 step について
redundant/relocated suppression を解除していた。

R16 は解除対象を
is_toda_group_proof_aggregate_statement(proof_step.conclusion)
が真である semantic aggregate statement に限定する。

これにより:
- Toda515Sigma8TransportedDecompositionStatement は semantic statement として残る。
- pi_8^5 の通常 Relation である direct premise は従来どおり relocation され、
  argument 冒頭との二重表示を起こさない。
- context_hidden_step_ids は従来どおり優先される。

テスト仕様更新の理由
====================
Phase143-51B は同じ multi-argument Narrative に transported decomposition の表示を要求する。
旧 Phase143-59B/61B の3 assertion は同じ文字列の非表示を要求しており論理的に両立しない。

Phase134-24 は元来、
transported decomposition -> standard-order final group
の両方を表示することを仕様としているため、後半 Phase143 の semantic rendering
方針に合わせて旧 assertion を更新する。

今回変更しないもの
==================
- 数学的推論規則
- proof repository
- API
- group calculation
- Phase 144 以降の機能
- documentation files

focused pytest
==============
tests/test_phase143_51a_r_provenance_semantic_catalog.py
tests/test_phase143_51b_aggregate_statement_prose.py
tests/test_phase143_59b_group_structure_duplicate_suppression.py
tests/test_phase143_61b_direct_premise_narrative.py
tests/test_phase143_61b_r_semantic_suppression_priority.py
tests/test_phase134_24_pi15_8_narrative.py

完了条件
========
- transported decomposition が semantic LaTeX で表示される。
- internal rule-name fallback は表示されない。
- pi_8^5 relocated direct premise は1回だけ表示される。
- final group conclusion は維持される。
- focused regression が全通過する。

次 Phase との境界
=================
この修正は Phase143 の Narrative semantic rendering 整合性だけを扱う。
Phase144 の機能は含めない。
