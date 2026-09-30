from phase148_rc2_4_repair_r5_two_group_exposure_path_audit.audit_phase148_rc2_4_repair_r5 import (
  CASES,
  _build_case,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


def test_phase150_rc4_7a_regression_repair_keeps_one_exactness_phrase_for_pi10_4_and_pi12_5():
  for label, n, k in CASES:
    (
      _presentation,
      _closure,
      _sidecar,
      _blocks,
      _arguments,
      rendered,
    ) = _build_case(
      label,
      n,
      k,
    )

    assert (
      rendered.count(
        "は完全である"
      )
      + rendered.count(
        r"\text{ is exact}"
      )
      == 1
    )


def test_phase150_rc4_7a_regression_repair_low_level_multi_argument_renderer_starts_with_argument():
  report = build_standard_toda_report(
    n=8,
    k=7,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(
    group_result
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  closure = build_toda_group_proof_narrative_semantic_closure_presentation(
    presentation
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    closure
  )
  blocks = build_toda_group_proof_narrative_blocks(
    closure,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    closure,
    blocks,
    semantic_sidecar=sidecar,
  )

  rendered = render_toda_group_proof_narrative_multi_argument_markdown(
    closure,
    blocks,
    sidecar,
    arguments,
  )

  assert "使用する結果を先にまとめる." not in rendered
  assert "**[R1]" not in rendered
  assert "$\\pi_{15}^{8}" in rendered
  assert "$\\sigma'''$ を定める." in rendered
