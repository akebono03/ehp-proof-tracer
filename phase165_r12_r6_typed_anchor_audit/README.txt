Phase 165 R12-R6 (read-only real typed witness binding)

Changes: only this new audit package; no production Python files are patched.
Entry: powershell -ExecutionPolicy Bypass -File .\phase165_r12_r6_typed_anchor_audit\run.ps1

Checks whether the installed R12-R2 quotient rule can bind its map, domain and
source_generator using actual linked, fixed, typed GIVEN statements from the
production shared statement bridge. Does not synthesize witnesses.

A generated GoalExpansion is not a ProofStep. A zero count means no eligible
source anchor was available through the inspected fixed-witness interface;
it is not a proof that the group claim is false.

Full pytest intentionally NOT run. Next R12-R7 (only if appropriate) may
address verified source typing or generic search binding gaps; do not add a
pi4^3-only adapter or assume a desired target as a premise.
