from phase158_r5_5a_repair3b_lightweight_ordering_diagnosis.audit_phase158_r5_5a_repair3b import (
  MAX_DEPTH,
  diagnose_target,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def test_phase158_r5_5a_repair3b_pi7_4_uses_actual_public_depth2_scope():
  view = (
    build_standard_web_group_proof_view(
      4,
      3,
      max_depth=MAX_DEPTH,
      mode="narrative",
    )
  )

  assert view.mode == "narrative"
  assert view.max_depth == 2
  assert view.rendered_lines


def test_phase158_r5_5a_repair3b_pi15_8_uses_actual_public_depth2_scope():
  view = (
    build_standard_web_group_proof_view(
      8,
      7,
      max_depth=MAX_DEPTH,
      mode="narrative",
    )
  )

  assert view.mode == "narrative"
  assert view.max_depth == 2
  assert view.rendered_lines


def test_phase158_r5_5a_repair3b_diagnosis_is_lightweight_and_structured():
  report = diagnose_target(
    "pi7_4",
    4,
    3,
  )

  assert "PUBLIC BODY" in report
  assert "SEMANTIC BLOCKS" in report
  assert "GENERIC BLOCK PROOF ORDER" in report
  assert "LIGHTWEIGHT NARRATIVE ARGUMENTS" in report
  assert "PRESENTATION EDGES WITH BLOCK OWNERSHIP" in report

  assert "TodaGroupProofNarrativeArgument(" not in report
