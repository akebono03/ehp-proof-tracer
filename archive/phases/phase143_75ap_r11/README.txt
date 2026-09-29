Phase 143-75AP R11

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

新規クラス・新規関数
====================
なし。

数学的規則の追加
================
なし。

目的
====
R10 では step-level derivation source のみ provenance suppression から
保護したが、pi_15^8 の transported decomposition は argument-level
DERIVATION transition の source block であり、その step-level map には
入っていなかった。

R11 は既存の argument-level transition を利用する。

transition.role == DERIVATION の場合だけ、

  transition.source_blocks

の identity を body renderer に渡す。

body renderer は、その block に限って

  suppress_provenance_only=False

として generic semantic statement を表示する。

SUPPORT / CALCULATION_CHAIN は従来どおり suppression する。

したがって pi_15^8 専用条件は追加しない。

変更後 import 部分
==================
既存の narrative transitions import を次の形にする。

from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)

その他の import は変更しない。

変更後
render_toda_group_proof_narrative_argument_body_markdown
========================================================
既存関数全体の処理を維持したまま、末尾の optional argument に

  preserve_provenance_block_ids: (
    frozenset[int]
    | None
  ) = None

を追加する。

None は空 frozenset に正規化し、int identity のみ許可する。

non-exact block の generic renderer 呼び出しは次の条件になる。

  suppress_provenance_only=(
    id(block) not in preserve_provenance_block_ids
  )

R10 で追加した preserve_provenance_step_ids は維持する。

変更後
render_toda_group_proof_narrative_multi_argument_markdown
=========================================================
既存 transition 取得後に次を計算する。

derivation_source_block_ids = (
  frozenset()
  if (
    transition is None
    or transition.role
    is not TodaGroupProofNarrativeTransitionRole.DERIVATION
  )
  else frozenset(
    id(source_block)
    for source_block in transition.source_blocks
  )
)

そして body renderer に

  preserve_provenance_block_ids=(
    derivation_source_block_ids
  )

を渡す。

focused tests
=============
pytest -q ^
  tests/test_phase143_51a_r_provenance_semantic_catalog.py ^
  tests/test_phase143_51b_aggregate_statement_prose.py ^
  tests/test_phase134_24_pi15_8_narrative.py

完了条件
========
- provenance-only rule name が再表示されない。
- transported decomposition が semantic statement として表示される。
- 表示契約は

  pi_15^8 ≅ Z/8{E sigma'} ⊕ Z{sigma_8}

  となる。
- 既存 pi_15^8 Narrative テストが通る。
- full pytest はまだ実行しない。

次 Phase との境界
=================
R11 は既存 DERIVATION transition の source block を Narrative 表示へ
接続するだけである。

新しい推論規則、statement type、transition role、Web UI、
clickable theorem reference、他 stem の機能追加は行わない。
