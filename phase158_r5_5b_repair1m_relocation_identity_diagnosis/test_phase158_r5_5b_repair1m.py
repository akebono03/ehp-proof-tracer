from phase158_r5_5b_repair1m_relocation_identity_diagnosis.audit_phase158_r5_5b_repair1m import (
  main,
)


def test_phase158_r5_5b_repair1m_diagnosis_runs():
  assert main() == 0
