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


TARGET_NAMES = {
  "TodaProp53FiniteDimensionalStatement",
  "TodaProp58FiniteDimensionalStatement",
  "TodaProp59FiniteDimensionalStatement",
  "TodaProp511NuSquaredFiniteDimensionalStatement",
}


def _target_facts():
  facts = {}

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
        statement = (
          node.proof_step.conclusion
        )
        name = type(statement).__name__
        if (
          name in TARGET_NAMES
          and name not in facts
        ):
          facts[name] = (
            _render_group_proof_narrative_fact(
              node.proof_step
            )
          )

      if len(facts) == len(TARGET_NAMES):
        return facts

  return facts


def test_phase143_75m_all_four_types_render_semantically():
  facts = _target_facts()

  assert set(facts) == TARGET_NAMES

  for name, rendered in facts.items():
    assert "=" in rendered
    assert name not in rendered
    assert "finite-dimensional integration" not in rendered


def test_phase143_75m_prop53_renders_range_semantically():
  rendered = _target_facts()[
    "TodaProp53FiniteDimensionalStatement"
  ]

  assert r"\ge 5" in rendered
  assert r"\mathbb{Z}/2" in rendered


def test_phase143_75m_prop58_renders_zero_semantically():
  rendered = _target_facts()[
    "TodaProp58FiniteDimensionalStatement"
  ]

  assert " = 0" in rendered
  assert r"\ge 6" in rendered


def test_phase143_75m_prop59_renders_free_group_semantically():
  rendered = _target_facts()[
    "TodaProp59FiniteDimensionalStatement"
  ]

  assert r"\mathbb{Z}" in rendered
  assert r"\ge 7" in rendered


def test_phase143_75m_prop511_renders_nu_squared_range():
  rendered = _target_facts()[
    "TodaProp511NuSquaredFiniteDimensionalStatement"
  ]

  assert r"\ge 9" in rendered
  assert r"\mathbb{Z}/2" in rendered
