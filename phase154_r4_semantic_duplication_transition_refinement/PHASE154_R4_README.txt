Phase 154-R4 — Semantic duplication / transition refinement

方針
----
R3 で検出した重複を機械的に全削除しない。

同一の数式や事実が異なる Argument で必要な場合があるため、
今回は upstream cause が明確な

  FINAL_RESULT_DERIVATION

の汎用理由文だけを対象とする。

この理由文は現在、

  以上で得た群構造、生成元、および写像に関する結果を合わせると、

という同一文を複数の結論の直前に挿入できる。
二回目以降は既存の transition connector が結論への接続を担当するため、
同一汎用理由文を再挿入しない。

変更対象
--------
toda_group_proof_narrative_reason_renderer.py

変更関数
--------
insert_toda_group_proof_narrative_reason_prose()

import の変更
-------------
なし。

変更後関数全文
--------------
def insert_toda_group_proof_narrative_reason_prose(
  markdown: str,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")
  if not isinstance(
    reason_sidecar,
    TodaGroupProofNarrativeReasonSidecar,
  ):
    raise TypeError(
      "reason_sidecar must be a "
      "TodaGroupProofNarrativeReasonSidecar"
    )

  rendered = markdown
  emitted_final_result_sentences = set()

  for reason in reason_sidecar.reasons:
    sentence = render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    if sentence is None:
      continue

    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_RESULT_DERIVATION
    ):
      if sentence in emitted_final_result_sentences:
        continue

      emitted_final_result_sentences.add(
        sentence
      )

    insertion_index = (
      _toda_group_proof_narrative_reason_insertion_index(
        rendered,
        reason,
        reason_sidecar,
      )
    )
    if insertion_index is None:
      continue

    prefix = sentence + "\n\n"
    if rendered[
      max(0, insertion_index - len(prefix)):
      insertion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )

  return rendered


新規テスト
----------
tests/test_phase154_r4_semantic_duplication_transition_refinement.py

テスト全文
----------
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


FINAL_RESULT_SENTENCE = (
  "以上で得た群構造、生成元、および写像に関する結果を合わせると、"
)


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _render_group(
  n: int,
  k: int,
) -> str:
  return render_toda_group_proof_narrative_markdown(
    _presentation(
      n,
      k,
    )
  )


def test_phase154_r4_repeated_final_result_reason_is_emitted_at_most_once():
  for n, k in (
    (3, 3),
    (4, 6),
    (9, 7),
  ):
    rendered = _render_group(
      n,
      k,
    )

    assert (
      rendered.count(
        FINAL_RESULT_SENTENCE
      )
      <= 1
    )


def test_phase154_r4_pi10_4_keeps_final_group_conclusion():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in rendered
  )


def test_phase154_r4_pi16_9_keeps_final_group_conclusion():
  rendered = _render_group(
    9,
    7,
  )

  assert (
    r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}"
    in rendered
  )


def test_phase154_r4_reason_insertion_is_deterministic_after_deduplication():
  raw_presentation = _presentation(
    4,
    6,
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  markdown = (
    FINAL_RESULT_SENTENCE
    + "\n\n"
    + r"$A = 0$"
    + "\n\n"
    + r"$B = 0$"
  )

  first = insert_toda_group_proof_narrative_reason_prose(
    markdown,
    reason_sidecar,
  )
  second = insert_toda_group_proof_narrative_reason_prose(
    markdown,
    reason_sidecar,
  )

  assert first == second


R4 で触れないもの
-----------------
- [R1] / [R2] の数学的役割説明
- "また、[R1]" → "まず、[R2]" の Reference sequence
  これは Reference linkage と不可分なので R5 へ残す。
- punctuation normalization
- 一般的な全行 deduplication
- Test Suite Consolidation

実行する pytest
---------------
- tests/test_phase154_r4_semantic_duplication_transition_refinement.py
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase150_rc4_7b_production_repair.py

全体テストは実行しない。

完了条件
--------
1. pi6_3 / pi10_4 / pi16_9 で FINAL_RESULT_DERIVATION の同一汎用理由文が 1 回以下になる。
2. 最終群結論を維持する。
3. R2 の internal fallback 修正を維持する。
4. transition connector の既存 contract を壊さない。
5. focused tests が PASS。
6. representative re-audit で残る exact duplicate を確認し、
   R4 Fix が必要か、R5/R6 に送るかを判断できる。

次 Phase 境界
------------
R4 の focused re-audit を見て、
残る duplicate が実際の semantic defect なら R4 Fix1。
Reference-only の接続問題なら R5。
句読点だけなら R6。
