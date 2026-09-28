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
  Toda58WhiteheadSquareUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
)


def _find_production_step(
  *,
  n,
  k,
  statement_type,
  predicate=None,
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

  for node in presentation.nodes:
    proof_step = node.proof_step
    if not isinstance(
      proof_step.conclusion,
      statement_type,
    ):
      continue
    if (
      predicate is None
      or predicate(
        proof_step.conclusion
      )
    ):
      return proof_step

  raise AssertionError(
    "target production step was not found"
  )


def test_phase143_75i_renders_pi32_whitehead_square_semantically():
  proof_step = _find_production_step(
    n=3,
    k=1,
    statement_type=(
      TodaPi32WhiteheadSquareUpToSignStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    rendered
    == r"$[\iota_{2}, \iota_{2}] = \pm 2\eta_{2}$"
  )
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75i_renders_prop27_whitehead_argument_semantically():
  proof_step = _find_production_step(
    n=3,
    k=1,
    statement_type=(
      TodaProp27HopfInvariantUpToSignStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    rendered
    == (
      r"$H([\iota_{2}, \iota_{2}])"
      r" = \pm 2\iota_{3}$"
    )
  )
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75i_renders_prop27_map_application_semantically():
  proof_step = _find_production_step(
    n=6,
    k=5,
    statement_type=(
      TodaProp27HopfInvariantUpToSignStatement
    ),
    predicate=lambda statement: (
      type(
        statement.argument
      ).__name__
      == "MapApplication"
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert rendered.startswith(
    r"$H(\Delta\left("
  )
  assert r" = \pm " in rendered
  assert rendered.endswith("$")
  assert (
    proof_step.inference_rule.name
    not in rendered
  )


def test_phase143_75i_renders_58_whitehead_square_semantically():
  proof_step = _find_production_step(
    n=5,
    k=4,
    statement_type=(
      Toda58WhiteheadSquareUpToSignStatement
    ),
  )

  rendered = _render_group_proof_narrative_fact(
    proof_step
  )

  assert (
    rendered
    == (
      r"$[\iota_{4}, \iota_{4}]"
      r" = \pm 2\nu_{4} - E\nu'$"
    )
  )
  assert (
    proof_step.inference_rule.name
    not in rendered
  )
