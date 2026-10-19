Phase 165 final targeted check, not full pytest.
Production source is not modified.
1. Runs existing tests/test_phase165*.py test bodies.
2. Tries generic search for pi3^2, pi4^3, pi5^3 separately (100-second bound per target).
3. Saves per-target logs and report.json in phase165_r6_audit_results/final_targeted.
A COMPLETE result is not by itself a proof/provenance certification.
An incomplete group or failed test results in a nonzero exit code.
