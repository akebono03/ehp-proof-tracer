from pathlib import Path

from hopf_rules import (
  toda_prop22_right_inference_rule,
)
from tests.test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)


def test_phase157_r20_prop22_is_first_class_literature_provenance():
  data = build_phase65_3_data()
  rule = data["prop22_rule"]

  assert rule.literature_reference is not None
  assert (
    rule.literature_reference.locator
    == "Proposition 2.2"
  )


def test_phase157_r20_equation57_depends_on_actual_prop22_step():
  data = build_phase65_3_data()

  assert (
    data["prop22_step"]
    in data["equation57_step"].premises
  )
  assert (
    data["prop22_step"]
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 2.2"
  )


def test_phase157_r20_contribution_renderer_has_no_pi6_target_specialization():
  source = Path(
    "toda_group_proof_narrative_contribution_renderer.py"
  ).read_text(
    encoding="utf-8"
  )

  assert "_phase157_r19_" not in source
  assert (
    "filter_phase157_r3_pi6_3_reference_entries"
    not in source
  )
  assert "is_pi6_3" not in source


def test_phase157_r20_reference_selection_has_no_pi6_root_specialization():
  source = Path(
    "toda_group_proof_narrative_references.py"
  ).read_text(
    encoding="utf-8"
  )

  assert "_phase157_r3_is_pi6_3_root" not in source
  assert (
    "filter_phase157_r3_pi6_3_reference_entries"
    not in source
  )
