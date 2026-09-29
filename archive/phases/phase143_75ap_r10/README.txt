Phase 143-75AP R10

変更対象
========
1. toda_group_proof_generic_narrative_renderer.py
   - _render_generic_narrative_proof_block()

2. toda_group_proof_narrative_argument_body_renderer.py
   - render_toda_group_proof_narrative_argument_body_markdown()

import 変更
===========
なし。

目的
====
Phase 143 の generic multi-argument Narrative では provenance-only step を
抑制している。しかし、その step が DERIVATION transition の数学的 source
でもある場合、first-class semantic statement まで本文から消えていた。

R10 は provenance suppression 自体を解除しない。
既存の step_derivation_sources_by_target_id から DERIVATION source step の
identity だけを集め、それらに限って provenance-only suppression を
免除する。

このため π_15^8 専用条件は追加しない。

変更後の _render_generic_narrative_proof_block
===============================================
def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  show_dependency_labels: bool = True,
  suppress_provenance_only: bool = False,
  preserve_provenance_step_ids: (
    frozenset[int]
    | None
  ) = None,
) -> tuple[
  str,
  ...,
]:
  if not isinstance(
    show_dependency_labels,
    bool,
  ):
    raise TypeError(
      "show_dependency_labels must be a bool"
    )

  if not isinstance(
    suppress_provenance_only,
    bool,
  ):
    raise TypeError(
      "suppress_provenance_only must be a bool"
    )

  if (
    preserve_provenance_step_ids is not None
    and not isinstance(
      preserve_provenance_step_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "preserve_provenance_step_ids must be "
      "a frozenset or None"
    )

  if preserve_provenance_step_ids is None:
    preserve_provenance_step_ids = frozenset()

  for step_id in preserve_provenance_step_ids:
    if (
      not isinstance(
        step_id,
        int,
      )
      or isinstance(
        step_id,
        bool,
      )
    ):
      raise TypeError(
        "preserve_provenance_step_ids must "
        "contain only integers"
      )

  block = blocks[
    block_index
  ]

  if show_dependency_labels:
    dependency_labels = (
      _generic_narrative_dependency_labels(
        presentation,
        blocks,
        block_index,
      )
    )
  else:
    dependency_labels = ()

  lines = []

  if dependency_labels:
    sentence_lead = (
      _generic_narrative_dependency_sentence_lead(
        dependency_labels
      )
    )
    lines.append(
      sentence_lead
    )
    lines.append(
      ""
    )

  for proof_step in block.steps:
    if (
      suppress_provenance_only
      and id(
        proof_step
      ) not in preserve_provenance_step_ids
      and _is_generic_narrative_provenance_only_statement(
        proof_step.conclusion
      )
    ):
      continue

    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

  if lines:
    lines.pop()

  return tuple(
    lines
  )

render_toda_group_proof_narrative_argument_body_markdown
=========================================================
この関数は大きいため、R10 では既存関数全体を保持し、
次の2箇所だけを機械的に置換する。

既存の
step_derivation_sources_by_target_id = (
  _step_derivation_sources_by_target_id(
    presentation,
    blocks,
  )
)

の直後に以下を追加する。

derivation_source_step_ids = frozenset(
  id(
    source_step
  )
  for source_steps in (
    step_derivation_sources_by_target_id.values()
  )
  for source_step in source_steps
)

そして既存の _render_generic_narrative_proof_block 呼び出しを以下にする。

block_lines = tuple(
  _render_generic_narrative_proof_block(
    presentation,
    render_blocks,
    block_index,
    show_dependency_labels=False,
    suppress_provenance_only=True,
    preserve_provenance_step_ids=(
      derivation_source_step_ids
    ),
  )
)

テスト
======
pytest -q ^
  tests/test_phase143_51a_r_provenance_semantic_catalog.py ^
  tests/test_phase143_51b_aggregate_statement_prose.py ^
  tests/test_phase134_24_pi15_8_narrative.py

完了条件
========
- 51A-R が provenance rule-name fallback を再表示しない。
- 51B で transported decomposition の semantic statement
  pi_15^8 ≅ Z/8{E sigma'} ⊕ Z{sigma_8}
  が表示される。
- 既存 pi_15^8 Narrative 回帰が通る。
- full pytest はまだ実行しない。

次 Phase との境界
=================
R10 は DERIVATION source semantic statement の表示保持だけを扱う。
新しい数学的推論、statement type、transition role、Web UI、
将来 Phase の clickable theorem reference は追加しない。
