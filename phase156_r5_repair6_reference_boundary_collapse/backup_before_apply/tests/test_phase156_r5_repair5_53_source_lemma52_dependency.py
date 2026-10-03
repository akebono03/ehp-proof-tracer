from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
)


def _pi6_3_data(
  depth: int = 2,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  return presentation, sidecar, rendered


def test_phase156_r5_repair5_53_is_source_for_lemma52_specialization_consequences():
  rules = (
    toda_53_nu_prime_lemma52_hopf_inference_rule(),
    toda_53_nu_prime_lemma52_double_inference_rule(),
    toda_53_nu_prime_lemma52_membership_inference_rule(),
  )

  for rule in rules:
    reference = rule.literature_reference
    assert reference is not None
    assert reference.label == "Toda (5.3)"
    assert reference.locator == "(5.3)"


def test_phase156_r5_repair5_lemma52_remains_internal_reference_application():
  presentation, sidecar, rendered = _pi6_3_data()

  assert len(
    sidecar.reference_application_semantics
  ) == 1
  application = (
    sidecar.reference_application_semantics[
      0
    ]
  )
  assert application.reference.label == "Lemma 5.2"


def test_phase156_r5_repair5_reference_section_uses_53_not_lemma52():
  presentation, sidecar, rendered = _pi6_3_data()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert "(5.3)" in reference_part
  assert "Lemma 5.2.**" not in reference_part


def test_phase156_r5_repair5_body_places_53_membership_before_lemma52_application():
  presentation, sidecar, rendered = _pi6_3_data()
  body = "まず" + rendered.split(
    "まず",
    1,
  )[1]

  bracket = (
    "$\\nu' \\in "
    "\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$"
  )
  precondition = "$2\\eta_{3} = 0$"
  application = (
    "この前提条件のもとで, "
    "Lemma 5.2 の $\\beta$ を $\\nu'$ として適用する."
  )

  assert bracket in body
  assert precondition in body
  assert application in body
  assert body.index(
    bracket
  ) < body.index(
    precondition
  ) < body.index(
    application
  )
