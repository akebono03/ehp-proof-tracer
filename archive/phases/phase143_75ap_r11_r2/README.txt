Phase 143-75AP R11-R2

R11 failure
===========
R11 stopped before modifying production code because its patcher expected
one exact post-R10 body-renderer signature string.

R11-R2 replaces that brittle exact-signature match with AST-based function
location and narrow source edits.

変更対象
========
1. toda_group_proof_narrative_argument_multi_renderer.py
   import:
   - TodaGroupProofNarrativeTransitionRole

   function:
   - render_toda_group_proof_narrative_multi_argument_markdown()

2. toda_group_proof_narrative_argument_body_renderer.py
   function:
   - render_toda_group_proof_narrative_argument_body_markdown()

新規クラス・新規関数
====================
なし。

テスト変更
==========
なし。

Docs変更
========
なし。

実装内容
========
argument-level DERIVATION transition の source_blocks の identity を
body renderer に渡す。

body renderer は該当 block だけ provenance-only suppression を解除する。

SUPPORT / CALCULATION_CHAIN は対象外。
pi_15^8 専用条件は追加しない。
R10 の step-level preserve_provenance_step_ids はそのまま維持する。

変更後 import 部分
==================
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)

focused pytest
==============
pytest -q ^
  tests/test_phase143_51a_r_provenance_semantic_catalog.py ^
  tests/test_phase143_51b_aggregate_statement_prose.py ^
  tests/test_phase134_24_pi15_8_narrative.py

完了条件
========
- provenance-only rule name が再表示されない。
- pi_15^8 transported decomposition が semantic statement として表示される。
- pi_15^8 Narrative の既存回帰が通る。
- full pytest はまだ実行しない。

次 Phase との境界
=================
R11-R2 は既存 DERIVATION transition の source block と Narrative 表示の
接続だけを修正する。

新規推論規則、statement type、transition role、Web UI、
clickable theorem reference は追加しない。
