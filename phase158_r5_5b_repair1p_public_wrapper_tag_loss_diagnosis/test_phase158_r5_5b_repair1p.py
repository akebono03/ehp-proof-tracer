from phase158_r5_5b_repair1p_public_wrapper_tag_loss_diagnosis.audit_phase158_r5_5b_repair1p import (
  main,
)


def test_phase158_r5_5b_repair1p_diagnosis_runs():
  assert main() == 0
