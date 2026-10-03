import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
)


def _pi6_3_rendered() -> str:
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
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase156_r5_repair2_lemma52_rules_have_explicit_lemma52_attribution():
  rules = (
    toda_53_nu_prime_lemma52_hopf_inference_rule(),
    toda_53_nu_prime_lemma52_double_inference_rule(),
    toda_53_nu_prime_lemma52_membership_inference_rule(),
  )

  for rule in rules:
    reference = rule.literature_reference
    assert reference is not None
    assert reference.label == "Toda Lemma 5.2"
    assert reference.locator == "Lemma 5.2"


def test_phase156_r5_repair2_bracket_specialization_remains_53_only():
  rule = (
    toda_53_nu_prime_bracket_specialization_inference_rule()
  )
  reference = rule.literature_reference

  assert reference is not None
  assert reference.label == "Toda (5.3)"
  assert reference.locator == "(5.3)"


def test_phase156_r5_repair2_pi6_reference_headers_separate_53_and_lemma52():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]
  headers = re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    reference_part,
  )

  assert "(5.3) / Lemma 5.2" not in reference_part
  assert headers.count(
    "(5.3)"
  ) == 1
  assert headers.count(
    "Lemma 5.2"
  ) == 1


def test_phase156_r5_repair2_pi6_body_still_records_lemma52_application():
  rendered = _pi6_3_rendered()

  assert "Lemma 5.2 を適用" in rendered
