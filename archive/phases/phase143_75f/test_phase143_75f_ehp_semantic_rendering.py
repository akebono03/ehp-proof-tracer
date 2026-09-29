from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


def _find_production_step(
  *,
  n,
  k,
  statement_type,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=7,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      statement_type,
    )
  )


def test_phase143_75f_renders_delta_surjective_semantically():
  proof_step = _find_production_step(
    n=3,
    k=5,
    statement_type=TodaDeltaSurjectiveStatement,
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\Delta:" in rendered
  assert r"\twoheadrightarrow" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75f_renders_suspension_kernel_semantically():
  proof_step = _find_production_step(
    n=3,
    k=1,
    statement_type=(
      TodaSuspensionKernelFreeCyclicStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\ker\left(E:" in rendered
  assert r"\mathbb{Z}\{" in rendered
  assert r"\eta_{2}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75f_renders_delta_image_semantically():
  proof_step = _find_production_step(
    n=3,
    k=1,
    statement_type=(
      TodaDeltaImageFreeCyclicStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    r"\operatorname{Im}\left(\Delta:"
    in rendered
  )
  assert r"\mathbb{Z}\{" in rendered
  assert r"\eta_{2}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75f_renders_delta_kernel_semantically():
  proof_step = _find_production_step(
    n=6,
    k=5,
    statement_type=(
      TodaDeltaKernelFreeCyclicStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\ker\left(\Delta:" in rendered
  assert r"\mathbb{Z}\{" in rendered
  assert r"\iota_{11}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
