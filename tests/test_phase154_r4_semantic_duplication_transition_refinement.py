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
