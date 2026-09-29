from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_NAME = "TodaProp44SuspensionInjectiveStatement"


def _target_steps():
  result = []

  for n in range(2, 16):
    for k in range(0, 8):
      report = build_standard_toda_report(
        n=n,
        k=k,
      )
      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = (
        build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
      )
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )

      for node in presentation.nodes:
        step = node.proof_step
        if (
          type(step.conclusion).__name__
          == TARGET_NAME
        ):
          result.append(step)

  return tuple(result)


def test_phase143_75p_all_target_occurrences_render_semantically():
  steps = _target_steps()

  assert len(steps) == 55

  for step in steps:
    rendered = _render_group_proof_narrative_fact(
      step
    )
    assert rendered.startswith("$E: ")
    assert r" \hookrightarrow " in rendered
    assert rendered.endswith("$")
    assert rendered != step.inference_rule.name


def test_phase143_75p_both_rule_families_use_same_semantic_renderer():
  steps = _target_steps()

  rule_counts = Counter(
    step.inference_rule.name
    for step in steps
  )

  assert rule_counts == Counter(
    {
      (
        "Toda Proposition 5.3 n=4 "
        "Phase 48 injectivity bridge"
      ): 32,
      (
        "Toda Proposition 4.4 "
        "suspension injectivity"
      ): 23,
    }
  )

  for step in steps:
    rendered = _render_group_proof_narrative_fact(
      step
    )
    assert "Proposition" not in rendered
    assert "injectivity" not in rendered


def test_phase143_75p_concrete_map_uses_source_and_target_groups():
  steps = _target_steps()

  concrete = next(
    step
    for step in steps
    if (
      repr(step.conclusion.map.source_group)
      == (
        "TodaPrimaryGroup("
        "group_dimension=5, "
        "sphere_dimension=3)"
      )
      and repr(step.conclusion.map.target_group)
      == (
        "TodaPrimaryGroup("
        "group_dimension=6, "
        "sphere_dimension=4)"
      )
    )
  )

  rendered = _render_group_proof_narrative_fact(
    concrete
  )

  assert rendered == (
    r"$E: \pi_{5}^{3} "
    r"\hookrightarrow \pi_{6}^{4}$"
  )
