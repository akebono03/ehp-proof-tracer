from phase158_r5_5b_repair1i_pi6_chain_presence_diagnosis.audit_phase158_r5_5b_repair1i import (
  main,
)


def test_phase158_r5_5b_repair1i_diagnosis_runs():
  assert main() == 0
