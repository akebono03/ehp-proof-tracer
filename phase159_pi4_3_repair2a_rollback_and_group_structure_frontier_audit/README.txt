Phase 159 — pi_4^3 repair 2a
Rollback overbroad repair2 and audit group-structure frontier
=============================================================

Why
---
The previous repair2 restored an older Phase 144 R15 rule that protected
second-level premises for every NarrativeArgument role.

Current Phase 144 R25 tests establish a later contract:
- ESTABLISH_ORDER does not generally protect second-level premises.
- ESTABLISH_DEFINITION does protect its second-level frontier.

The broad repair therefore caused regressions in:
- eta-family internal-definition hiding,
- pi_6^3 transition chains,
- Proposition 4.4 reference exposure.

Action
------
1. Restore the current production frontier helper exactly.
2. Remove the failed Phase 159 repair2 test file.
3. Verify the existing frontier contracts.
4. Audit ESTABLISH_GROUP_STRUCTURE specifically for:
   - pi_4^3
   - pi_6^3

No new production frontier rule is introduced in this package.

Files
-----
Production file restored:
  toda_group_proof_narrative_argument_multi_renderer.py

Removed if present:
  tests/test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py

Audit output:
  audit_output/summary.txt

Repository-wide pytest is not run.
