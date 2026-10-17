Phase 165 R12-R3: common registry-to-backward-search proof chaining.
Extract into the repository root and run run.ps1.
No production source files are overwritten. No Toda-specific adapter is added.
Three added tests verify a 2-level inference chain, missing-premise failure,
and R12-R2 automatic registration. Tests use synthetic GIVEN fixture steps
and do NOT establish pi_4^3 or the correctness of any Toda source.
Full pytest is not executed.
