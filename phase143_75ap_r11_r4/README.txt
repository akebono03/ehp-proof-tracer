Phase 143-75AP R11-R4

This patch is based on the local source audit produced after R11-R3.

変更対象
========
1. toda_group_proof_narrative_argument_multi_renderer.py
   import:
   - TodaGroupProofNarrativeTransitionRole を追加

   function:
   - render_toda_group_proof_narrative_multi_argument_markdown()

2. toda_group_proof_narrative_argument_body_renderer.py
   function:
   - render_toda_group_proof_narrative_argument_body_markdown()

変更後 import 部分
==================
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)

新規クラス・新規関数
====================
なし。

テスト変更
==========
なし。

実装
====
multi renderer:
- transition.role == DERIVATION の場合だけ
  transition.source_blocks の identity を収集。
- body renderer へ preserve_provenance_block_ids として渡す。

body renderer:
- 現行の direct_derivation_premises / context_hidden_step_ids API を維持。
- preserve_provenance_block_ids を optional argument として追加。
- 指定された block のみ suppress_provenance_only=False。
- R10 の preserve_provenance_step_ids は維持。

pi_15^8 専用条件、新しい数学規則、新しい statement type は追加しない。

focused pytest
==============
pytest -q ^
  tests/test_phase143_51a_r_provenance_semantic_catalog.py ^
  tests/test_phase143_51b_aggregate_statement_prose.py ^
  tests/test_phase134_24_pi15_8_narrative.py

完了条件
========
- 内部 provenance rule 名が Narrative に出ない。
- transported decomposition が semantic statement として出る。
- pi_15^8 Narrative 回帰が通る。

次 Phase との境界
=================
この修正は既存 argument-level DERIVATION source と既存 semantic renderer
の接続のみを扱う。新規推論、Web UI、clickable reference は扱わない。
