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
  toda_53_eta3_twice_zero_inference_rule,
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


def test_phase156_r5_repair3_eta3_twice_zero_is_attributed_to_proposition51():
  rule = (
    toda_53_eta3_twice_zero_inference_rule()
  )
  reference = rule.literature_reference

  assert reference is not None
  assert reference.label == "Toda Proposition 5.1"
  assert reference.locator == "Proposition 5.1"


def test_phase156_r5_repair3_pi6_has_single_53_and_single_proposition51_header():
  rendered = _pi6_3_rendered()
  headers = re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    rendered,
  )

  assert headers.count(
    "(5.3)"
  ) == 1
  assert headers.count(
    "Lemma 5.2"
  ) == 0
  assert headers.count(
    "Proposition 5.1"
  ) == 0
  assert "(5.3) / Lemma 5.2" not in rendered


def test_phase156_r5_repair3_two_eta3_zero_is_not_under_53_header():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  sections = re.split(
    r"(?=\*\*\[R\d+\] )",
    reference_part,
  )
  source_53 = next(
    section
    for section in sections
    if re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      section,
    )
  )
  proposition51 = next(
    section
    for section in sections
    if re.search(
      r"\*\*\[R\d+\] Proposition 5\.1\.\*\*",
      section,
    )
  )

  assert "2\\eta_{3} = 0" not in source_53
  assert "2\\eta_{3} = 0" in proposition51
