Phase 162 pi_5^3 focused integration audit

This test verifies that Phase 161 R5 reconstructs the E isomorphism proof step
from independently provided premises, and that the reconstructed step can be
consumed by the existing Phase 59 bridge/transport inference rules to derive
the group structure pi_5^3 = Z/2{eta_3 o eta_4}.

This is not a goal-only general backward proof search. It deliberately takes
Phase 59 initial premises for E, the already derived pi_4^2 step, and eta
definition roots as inputs. It does not modify production code or add a renderer.

Unzip into the repository root and run:
  powershell -ExecutionPolicy Bypass -File .\phase162_pi5_3_integration_audit\run_phase162_pi5_3_integration_audit.ps1

No full test suite is invoked.
