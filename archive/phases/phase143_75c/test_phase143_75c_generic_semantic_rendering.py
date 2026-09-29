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
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
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


def test_phase143_75c_renders_toda45_isomorphism_semantically():
  proof_step = _find_production_step(
    n=4,
    k=1,
    statement_type=Toda45IsomorphismStatement,
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    "$E^{"
  )
  assert r"\xrightarrow{\cong}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75c_renders_hopf_isomorphism_semantically():
  proof_step = _find_production_step(
    n=2,
    k=1,
    statement_type=(
      TodaHopfInvariantIsomorphismStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    "$H: "
  )
  assert r"\xrightarrow{\cong}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75c_renders_prop44_second_summand_semantically():
  proof_step = _find_production_step(
    n=2,
    k=2,
    statement_type=(
      TodaProp44SecondSummandRestrictionStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert r"\mapsto" in rendered
  assert r"\eta_{2}" in rendered
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
