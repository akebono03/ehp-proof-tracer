# Phase 165 R57-R8 selector signature fix

This overlay corrects the R57-R8 installer to accept the existing R55 API `registered_group_goal_candidates(bridge, *, n: int, k: int)`. The original installer incorrectly looked for `n` and `k` only among positional arguments. The mathematical specialization, shared inference rules, and Web code remain unchanged.

Extract the ZIP at the repository root, then execute `phase165_r57_r8_selector_signature_fix/run.ps1`. The runner installs the corrected installer into the previously extracted R57-R8 package, runs a signature regression check, installs R57-R8, and runs only the R57-R8 and R57-R7 targeted tests.
