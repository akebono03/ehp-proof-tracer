from phase158_r5_5b_repair1k_pi6_tag_vs_plain_diagnosis.audit_phase158_r5_5b_repair1k import (
  main,
)


def test_phase158_r5_5b_repair1k_diagnosis_runs():
  assert main() == 0
